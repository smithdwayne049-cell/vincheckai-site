import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:4173';
await fs.mkdir('qa',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const issues=[];
try {
  for(const config of [{name:'desktop',viewport:{width:1440,height:1000}},{name:'mobile',viewport:{width:360,height:800},isMobile:true,deviceScaleFactor:2},{name:'reduced',viewport:{width:360,height:800},reducedMotion:'reduce'}]){
    const context=await browser.newContext(config);
    const page=await context.newPage();
    page.on('pageerror',error=>issues.push(`${config.name}: ${error.message}`));
    page.on('console',message=>{if(message.type()==='error')issues.push(`${config.name}: ${message.text()}`);});
    for(const route of ['/', '/sample.html','/404.html']){
      const response=await page.goto(base+route);assert.equal(response.status(),200);
      await page.waitForTimeout(route==='/'?2200:100);
      assert(await page.locator('h1').count()===1);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${config.name} overflow ${route}`);
      assert(await page.locator('meta[name="description"]').getAttribute('content'));
      for(const img of await page.locator('img').all()){
        if(await img.getAttribute('loading')==='lazy'){
          const asset=await context.request.get(new URL(await img.getAttribute('src'),page.url()).href);assert(asset.ok(),'Missing lazy image');
          await img.scrollIntoViewIfNeeded();
          await img.evaluate(el=>el.decode());
        }else assert(await img.evaluate(el=>el.complete&&el.naturalWidth>0),'Broken image');
        if(!await img.evaluate(el=>el.closest('.cinema')))assert(await img.evaluate(el=>Math.abs((el.clientWidth/el.clientHeight)/(el.naturalWidth/el.naturalHeight)-1)<.08),'Distorted image');
      }
      if(route==='/'){
        await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
        await page.waitForTimeout(250);
        if(config.name==='reduced')assert.equal(await page.locator('.has-scene').count(),0);
        else {
          // The mobile phone deliberately waits until 70% visible before loading.
          await page.locator('#phone-stage').scrollIntoViewIfNeeded();
          await page.waitForFunction(()=>document.querySelector('#phone-stage').classList.contains('has-scene'),{timeout:10000});
          await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
        }
        await page.screenshot({path:`qa/${config.name}-hero.png`});
        await page.screenshot({path:`qa/${config.name}-full.png`,fullPage:true});
        await page.locator('#faq').scrollIntoViewIfNeeded();
        await page.locator('summary').first().click();assert(await page.locator('details').first().getAttribute('open')!==null);
        const schemas=await page.locator('script[type="application/ld+json"]').allTextContents();for(const raw of schemas)JSON.parse(raw);
      }
      if(route==='/sample.html'){
        const source=JSON.parse(await fs.readFile('data/sample_report_ford_escape_2018.json','utf8'));
        await page.locator('.disclosure').evaluateAll(els=>els.forEach(el=>el.open=true));
        // Revision 4 counters finish after entering the viewport.
        await page.locator('[data-count="1825"]').scrollIntoViewIfNeeded();
        await page.waitForFunction(()=>document.querySelector('[data-count="1825"]').textContent==='1,825');
        const text=await page.locator('main').innerText();
        const safety=JSON.parse(await fs.readFile('data/nhtsa_ford_escape_2018.json','utf8'));
        assert.equal(await page.locator('.recall').count(),safety.recalls.results.length);
        assert(text.includes(safety.complaints.results.length.toLocaleString('en-US')));
        assert(text.includes('not this specific VIN'));
        if(config.name==='mobile'){await page.locator('#red-flags summary').click();assert.equal(await page.locator('#red-flags').getAttribute('open'),null);await page.locator('.report-nav a[href="#red-flags"]').click();assert.notEqual(await page.locator('#red-flags').getAttribute('open'),null);}
        for(const value of Object.values(source.ai).flat()){
          if(typeof value==='string')assert(text.toLowerCase().includes(value.toLowerCase()),`Missing report text: ${value}`);
        }
        await page.screenshot({path:`qa/${config.name}-sample.png`,fullPage:true});
      }
      for(const link of await page.locator('a[href]').all()){
        const href=await link.getAttribute('href');
        if(href.startsWith('http'))continue;
        const url=new URL(href,page.url());
        const res=await context.request.get(url.href);assert(res.ok(),`Broken link ${href}`);
      }
    }
    await context.close();
  }
  const context=await browser.newContext({viewport:{width:360,height:800}});
  await context.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(type.startsWith('webgl'))return null;return original.call(this,type,...args);};});
  const page=await context.newPage();await page.goto(base);await page.waitForTimeout(1800);
  assert.equal(await page.locator('.has-scene').count(),0);assert(await page.locator('.phone-fallback').isVisible());
  await context.close();
  assert.deepEqual(issues,[],'Browser errors');
  console.log('PASS: desktop 1440px, mobile 360px, reduced motion, no WebGL, complete report data, images, links, FAQ, SEO and no browser errors.');
}finally{await browser.close();}
