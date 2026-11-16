import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:4173';
const langs=['en','ru','de','es','fr','it','pt','tr','ko','zh'];
const files=['ford','toyota','chevrolet','honda','nissan'].map(b=>`${b}-vin-decoder.html`).concat('vin-check-no-subscription.html');
const path=(lang,file)=>`/${lang==='en'?'':lang+'/'}${file}`;
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors=[];
await fs.mkdir('qa',{recursive:true});
try {
  // Fetch one real public response, then reuse it for all locales and brand shells.
  const live=await browser.newPage();
  await live.goto(base+'/ford-vin-decoder.html');
  await live.locator('input').fill('1FMCU9HD3JUA50412');
  const response=live.waitForResponse(r=>r.url().startsWith('https://vpic.nhtsa.dot.gov/'),{timeout:30000});
  await live.locator('button[type=submit]').click();
  const r=await response;assert(r.ok());const data=await r.json();
  await fs.writeFile('qa/r9-live-vpic.json',JSON.stringify(data,null,2));
  await live.waitForFunction(()=>document.querySelector('.vin-output').textContent.includes('Escape'));
  await live.close();
  const titles=new Set(), descriptions=new Set();
  for(const width of [360,1440]){
    const context=await browser.newContext({viewport:{width,height:1000}});
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(e.message));
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
    await page.route('https://vpic.nhtsa.dot.gov/**',r=>r.fulfill({json:data}));
    for(const lang of langs)for(const file of files){
      const url=base+path(lang,file);
      assert.equal((await page.goto(url)).status(),200);
      assert.equal(await page.locator('html').getAttribute('lang'),lang);
      assert.equal(await page.locator('h1').count(),1);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),url);
      const title=await page.title(), desc=await page.locator('meta[name=description]').getAttribute('content');
      assert(title.length<=60,`${url} title ${title.length}`);
      assert(desc.length<=155,`${url} description ${desc.length}`);
      if(width===360){assert(!titles.has(title),`Duplicate title ${title}`);titles.add(title);assert(!descriptions.has(desc),`Duplicate description ${desc}`);descriptions.add(desc);}
      const canonical='https://vincheckai.com'+path(lang,file);
      assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),canonical);
      assert.equal(await page.locator('meta[property="og:url"]').getAttribute('content'),canonical);
      for(const key of ['og:title','twitter:title'])assert.equal(await page.locator(`meta[${key.startsWith('og:')?'property':'name'}="${key}"]`).getAttribute('content'),title);
      assert.equal(await page.locator('link[hreflang]').count(),11);
      for(const alt of [...langs,'x-default'])assert.equal(await page.locator(`link[hreflang="${alt}"]`).getAttribute('href'),'https://vincheckai.com'+path(alt==='x-default'?'en':alt,file));
      const schemas=await page.locator('script[type="application/ld+json"]').evaluateAll(els=>els.map(el=>JSON.parse(el.textContent)));
      assert.equal(schemas[0]['@type'],'WebPage');assert.equal(schemas[0].name,title);
      for(const href of await page.locator('a[href^="https://play.google.com/"]').evaluateAll(els=>els.map(el=>el.href)))assert.equal(new URL(href).searchParams.get('hl'),lang==='zh'?'zh-CN':lang==='pt'?'pt-BR':lang);
      assert.equal(await page.locator('.brand-decoder-links a').count(),6);
      for(const href of await page.locator('.brand-decoder-links a').evaluateAll(els=>els.map(el=>el.href)))assert(new URL(href).pathname.startsWith(path(lang,'')));
      for(const href of await page.locator('.language-switcher a').evaluateAll(els=>els.map(el=>el.href)))assert(href.endsWith(file));
      if(file.includes('-vin-decoder')){
        const faq=schemas.find(s=>s['@type']==='FAQPage');assert.equal(faq.mainEntity.length,3);
        const visible=await page.locator('main details').evaluateAll(els=>els.map(el=>({q:el.querySelector('summary').textContent,a:el.querySelector('p').textContent})));
        assert.deepEqual(faq.mainEntity.map(q=>({q:q.name,a:q.acceptedAnswer.text})),visible);
        if(['en','ru','pt','zh'].includes(lang)){
          await page.locator('input').fill('invalid');await page.locator('button[type=submit]').click();
          assert.equal(await page.locator('input').getAttribute('aria-invalid'),'true');
          await page.locator('input').fill('1fmcu9hd3jua50412');await page.locator('button[type=submit]').click();
          await page.waitForFunction(()=>document.querySelector('.vin-output').textContent.includes('Escape'));
          const output=await page.locator('.vin-output').innerText();assert(output.includes('FORD')&&output.includes('2018'));
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
        }
      }else assert.equal(await page.locator('main a[href="decode.html"]').count(),1);
      if(['en','ru','pt','zh'].includes(lang)&&['ford-vin-decoder.html','vin-check-no-subscription.html'].includes(file))await page.screenshot({path:`qa/r9-${lang}-${width}-${file}.png`,fullPage:true});
    }
    await context.close();
  }
  const xml=await fs.readFile('sitemap.xml','utf8');
  assert.equal((xml.match(/<url>/g)||[]).length,100);assert.equal((xml.match(/xhtml:link/g)||[]).length,1100);
  for(const lang of langs)for(const file of files)assert(xml.includes(`<loc>https://vincheckai.com${path(lang,file)}</loc>`));
  assert.deepEqual(errors,[]);
  console.log('PASS: 60 pages at 360/1440px, localized SEO/schema/footer/switcher, live vPIC and all five brand decoders in en/ru/pt/zh, valid sitemap, no overflow or browser errors.');
}finally{await browser.close();}
