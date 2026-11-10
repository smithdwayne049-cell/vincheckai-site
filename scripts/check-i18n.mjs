import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const base='http://127.0.0.1:4173';
const languages=['en','ru','de','es','fr','it','pt','tr','ko','zh'];
const route=(lang,report=false)=>`/${lang==='en'?'':lang+'/'}${report?'sample.html':''}`;
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors=[];
await fs.mkdir('qa',{recursive:true});
try {
  for (const width of [360,1440]) {
    const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:'reduce'});
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(e.message));
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
    for(const lang of languages)for(const report of [false,true]){
      const url=base+route(lang,report);
      assert.equal((await page.goto(url)).status(),200);
      await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.locator('html').getAttribute('lang'),lang);
      assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),'https://vincheckai.com'+route(lang,report));
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Overflow: ${url} at ${width}`);
      const title=await page.title(); assert(title);
      for(const selector of ['meta[property="og:title"]','meta[name="twitter:title"]'])assert.equal(await page.locator(selector).getAttribute('content'),title);
      const alternates=page.locator('link[rel="alternate"][hreflang]');assert.equal(await alternates.count(),11);
      for(const alt of [...languages,'x-default']){
        assert.equal(await page.locator(`link[hreflang="${alt}"]`).getAttribute('href'),'https://vincheckai.com'+route(alt==='x-default'?'en':alt,report));
      }
      const hl=lang==='zh'?'zh-CN':lang==='pt'?'pt-BR':lang;
      for(const href of await page.locator('a[href^="https://play.google.com/"]').evaluateAll(a=>a.map(x=>x.href)))assert.equal(new URL(href).searchParams.get('hl'),hl);
      const source=JSON.parse(await fs.readFile(`i18n/${lang}.json`,'utf8'));
      const content=await page.locator('body').textContent();
      assert(!content.includes('ZXQ')&&!content.includes('�'),`Bad translation token in ${url}`);
      if(report){
        const snapshot=JSON.parse(await fs.readFile('data/sample_report_ford_escape_2018.json','utf8'));
        for(const value of Object.values(snapshot.ai).flat())if(typeof value==='string'&&value!=='caution')assert(content.includes(source[value]||value),`Missing AI report translation: ${lang} ${value}`);
        await page.waitForFunction(()=>document.querySelector('.score b').textContent==='55');
        if(lang!=='en')assert(content.includes(source['(official NHTSA text, English)']));
      }else{
        const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
        const app=schema['@graph'].find(x=>x['@type']==='SoftwareApplication');
        assert.equal(app.inLanguage,lang);assert.equal(new URL(app.downloadUrl).searchParams.get('hl'),hl);
        const faq=schema['@graph'].find(x=>x['@type']==='FAQPage');
        assert.equal(faq.mainEntity.length,4);
        for(const q of faq.mainEntity){assert(content.includes(q.name));assert(content.includes(q.acceptedAnswer.text));}
        assert.equal(await page.locator('.has-scene').count(),0);
      }
      for(const image of await page.locator('img').all()){
        const response=await context.request.get(new URL(await image.getAttribute('src'),url).href);assert(response.ok());
      }
      // Native disclosure is keyboard accessible; each alternate retains page type.
      await page.locator('.language-switcher summary').click();
      assert(await page.locator('.language-switcher nav').isVisible());
      assert.equal(await page.locator('.language-switcher a').count(),10);
      for(const target of languages){
        const a=page.locator(`.language-switcher a[lang="${target}"]`);
        assert.equal(new URL(await a.getAttribute('href'),url).pathname,route(target,report));
      }
      await page.locator('.language-switcher a[lang="en"]').click();
      assert.equal(new URL(page.url()).pathname,route('en',report));
      if(['de','ru','zh'].includes(lang)){
        await page.goto(url);
        for(const img of await page.locator('img').all()){
          await img.scrollIntoViewIfNeeded();await img.evaluate(el=>el.decode());
        }
        await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
        await page.screenshot({path:`qa/i18n-${lang}-${width}-${report?'sample':'home'}.png`,fullPage:true});
        await page.screenshot({path:`qa/i18n-${lang}-${width}-${report?'sample':'home'}-top.png`});
      }
    }
    await context.close();
  }
  // The shared module must also render its phone texture from a nested language URL.
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.goto(base+'/de/');
  await page.waitForFunction(()=>document.querySelector('#phone-stage')?.classList.contains('has-scene'),null,{timeout:15000});
  await context.close();
  assert.deepEqual(errors,[]);
  const xml=await fs.readFile('sitemap.xml','utf8');
  assert.equal((xml.match(/<url>/g)||[]).length,40);
  assert.equal((xml.match(/xhtml:link/g)||[]).length,440);
  console.log('PASS: 20 localized pages at 360px and 1440px, metadata, reciprocal hreflang, sitemap, full AI translations, FAQ/schema consistency, switcher navigation, Play locales, images, reduced motion, nested 3D, no browser errors.');
}finally{await browser.close();}
