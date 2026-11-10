import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:4173';
const langs=['en','ru','de','es','fr','it','pt','tr','ko','zh'];
const route=(lang,page='')=>`/${lang==='en'?'':lang+'/'}${page}`;
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors=[];
await fs.mkdir('qa',{recursive:true});
try {
  // Real public API responses, then replayed to avoid repeating identical API calls.
  const live=await browser.newPage();
  live.on('pageerror',e=>errors.push(e.message));
  const responses={};
  for(const vin of ['1FMCU9HD3JUA50412','WVWZZZ1KZAW000000']){
    await live.goto(base+'/decode.html');
    await live.locator('input').fill(vin);
    const response=live.waitForResponse(r=>r.url().startsWith('https://vpic.nhtsa.dot.gov/'),{timeout:30000});
    await live.locator('button[type=submit]').click();
    const r=await response;assert(r.ok());responses[vin]=await r.json();
    await live.waitForFunction(()=>!document.querySelector('button[type=submit]').disabled);
    if(vin.startsWith('1FM')){
      const result=await live.locator('.vin-output').innerText();
      assert(result.includes('FORD')&&result.includes('Escape')&&result.includes('2018'));
    }else assert(await live.locator('.vin-output a[href^="https://play.google.com/"]').count());
  }
  await fs.writeFile('qa/r7-live-vpic.json',JSON.stringify(responses,null,2));
  await live.close();
  for(const width of [360,1440]){
    const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:'reduce'});
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(e.message));
    page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('net::ERR_FAILED'))errors.push(m.text());});
    let requests=0;
    await page.route('https://vpic.nhtsa.dot.gov/**',async r=>{
      requests++;
      const vin=r.request().url().split('/DecodeVinValues/')[1].split('?')[0];
      assert(responses[vin]);
      await r.fulfill({json:responses[vin]});
    });
    for(const lang of langs)for(const file of ['decode.html','pricing.html']){
      const url=base+route(lang,file);
      assert.equal((await page.goto(url)).status(),200);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${url} overflow at ${width}`);
      assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://vincheckai.com'+route(lang,file));
      assert.equal(await page.locator('link[hreflang]').count(),11);
      for(const alt of [...langs,'x-default'])assert.equal(await page.locator(`link[hreflang="${alt}"]`).getAttribute('href'),'https://vincheckai.com'+route(alt==='x-default'?'en':alt,file));
      for(const href of await page.locator('a[href^="https://play.google.com/"]').evaluateAll(els=>els.map(el=>el.href)))assert.equal(new URL(href).searchParams.get('hl'),lang==='zh'?'zh-CN':lang==='pt'?'pt-BR':lang);
      assert.equal(await page.locator('.navlinks a[href="decode.html"]').count(),1);
      assert.equal(await page.locator('.navlinks a[href="pricing.html"]').count(),1);
      assert(await page.locator('.navlinks a[href="decode.html"]').isVisible());
      assert(await page.locator('.navlinks a[href="pricing.html"]').isVisible());
      for(const a of await page.locator('.language-switcher a').all())assert(new URL(await a.getAttribute('href'),url).pathname.endsWith(file));
      if(file==='pricing.html'){
        const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
        assert.deepEqual(schema['@graph'].map(p=>p.offers.price),['3.99','5.99']);
        assert(schema['@graph'].every(p=>p.offers.priceCurrency==='USD'));
      }
      if(!['en','ru','zh'].includes(lang))continue;
      if(file==='decode.html'){
        for(const invalid of ['123','1FMCU9HD3JUA5041Q','1FMCU9HD3JUA5041I','1FMCU9HD3JUA5041O','1FMCU9HD3JUA5041!']){
          const before=requests;
          await page.locator('input').fill(invalid);
          await page.locator('button[type=submit]').click();
          assert.equal(requests,before);
          assert.equal(await page.locator('input').getAttribute('aria-invalid'),'true');
          assert(await page.locator('.vin-status').innerText());
        }
        await page.locator('input').fill('1fmcu9hd3jua50412');
        assert.equal(await page.locator('input').inputValue(),'1FMCU9HD3JUA50412');
        await page.locator('button[type=submit]').click();
        await page.waitForFunction(()=>!document.querySelector('button[type=submit]').disabled);
        assert.equal(await page.locator('.vin-output dd').count(),9);
        assert((await page.locator('.vin-output').innerText()).includes('Escape'));
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
        await page.screenshot({path:`qa/r7-${lang}-${width}-decode.png`,fullPage:true});
        await page.reload();assert.equal(await page.locator('input').inputValue(),'1FMCU9HD3JUA50412');
        await page.locator('input').fill('WVWZZZ1KZAW000000');
        await page.locator('button[type=submit]').click();
        await page.waitForFunction(()=>!document.querySelector('button[type=submit]').disabled);
        assert.equal(await page.locator('.vin-output dd').count(),0);
        assert.equal(await page.locator('.vin-output a').count(),1);
      }else await page.screenshot({path:`qa/r7-${lang}-${width}-pricing.png`,fullPage:true});
    }
    // Home input, locked report preview, and Google Play action after a real decode.
    for(const lang of ['en','ru','zh']){
      await page.goto(base+route(lang));
      assert.equal(await page.locator('.hero .vin-form').count(),1);
      await page.locator('input').fill('1FMCU9HD3JUA50412');
      await page.locator('button[type=submit]').click();
      await page.waitForFunction(()=>!document.querySelector('button[type=submit]').disabled);
      assert.equal(await page.locator('.vin-output .locked-report').count(),1);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      await page.screenshot({path:`qa/r7-${lang}-${width}-home.png`,fullPage:true});
    }
    await context.close();
  }
  const page=await browser.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/decode.html');
  // A real network failure, followed by a successful retry.
  await page.route('https://vpic.nhtsa.dot.gov/**',r=>r.abort());
  await page.locator('input').fill('1FMCU9HD3JUA50412');
  await page.locator('button[type=submit]').click();
  await page.waitForFunction(()=>document.querySelector('button[type=submit]').textContent==='Retry');
  assert(await page.locator('.vin-status').innerText());
  await page.unroute('https://vpic.nhtsa.dot.gov/**');
  await page.route('https://vpic.nhtsa.dot.gov/**',r=>r.fulfill({json:responses['1FMCU9HD3JUA50412']}));
  await page.locator('button[type=submit]').click();
  await page.waitForFunction(()=>document.querySelector('button[type=submit]').textContent==='Decode VIN');
  // API error with an otherwise usable make/model must not show partial data.
  await page.unroute('https://vpic.nhtsa.dot.gov/**');
  await page.route('https://vpic.nhtsa.dot.gov/**',r=>r.fulfill({json:{Results:[{Make:'FORD',Model:'Escape',ErrorCode:'0, 5'}]}}));
  await page.locator('button[type=submit]').click();
  await page.waitForFunction(()=>!document.querySelector('button[type=submit]').disabled);
  assert.equal(await page.locator('.vin-output dd').count(),0);
  await page.close();
  assert.deepEqual(errors,[]);
  const sitemap=await fs.readFile('sitemap.xml','utf8');
  assert.equal((sitemap.match(/<loc>/g)||[]).length,40);
  console.log('Revision 7 passed: live Ford/European VINs, validation, retry, API errors, all 40 new page/viewport combinations, en/ru/zh results and homepage.');
} finally {await browser.close();}
