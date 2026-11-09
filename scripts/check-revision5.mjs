import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
await fs.mkdir('qa',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors=[];
const base='http://127.0.0.1:4173';
try {
 for(const mode of ['reduce','no-preference'])for(const width of [360,1440]){
  const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:mode});
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  for(const lang of ['en','ru','zh']){
   const prefix=lang==='en'?'/':`/${lang}/`;
   await page.goto(base+prefix);
   await page.waitForSelector(`html.${mode==='reduce'?'gentle-ready':'motion-ready'}`);
   const text=await page.locator('body').textContent();
   assert(!/NMVTIS|Carfax|official title|accident history|salvage|lien history/i.test(text));
   assert.equal(await page.locator('.features>.feature').count(),5);
   assert.equal(await page.locator('.assistant-feature').count(),1);
   assert.equal(await page.locator('.footer-notice').count(),1);
   const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
   assert.equal(schema['@graph'].find(s=>s['@type']==='FAQPage').mainEntity.length,4);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(mode==='reduce'){
    assert.equal(await page.locator('.has-scene,.pin-spacer').count(),0);
    // Gentle motion really runs, even with Windows Animation effects disabled.
    await page.waitForFunction(()=>document.querySelector('h1').getAnimations().some(a=>a.playState==='running'));
    assert(await page.locator('h1').evaluate(el=>{
     const a=el.getAnimations()[0];return a.effect.getKeyframes().every(k=>!k.transform||Math.abs(new DOMMatrixReadOnly(k.transform).m42)<=12);
    }));
   }else if(width===1440){
    const triggers=await page.evaluate(()=>window.ScrollTrigger.getAll().filter(t=>t.pin).map(t=>({start:t.start,end:t.end})));
    assert.equal(triggers.length,2);
    await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),triggers[1].start+50);
    await page.waitForTimeout(1000);
    const before=await page.locator('.features').evaluate(el=>new DOMMatrixReadOnly(getComputedStyle(el).transform).m41);
    await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),triggers[1].end-10);
    await page.waitForTimeout(1200);
    const after=await page.locator('.features').evaluate(el=>new DOMMatrixReadOnly(getComputedStyle(el).transform).m41);
    assert(after<before-700,'Horizontal track must travel across all five cards');
    const last=await page.locator('.features>.feature').last().boundingBox();
    assert(last.x>=0&&last.x+last.width<=1442,'Last chapter must be fully visible');
    await page.screenshot({path:`qa/r5-${lang}-horizontal.png`});
   }else assert.equal(await page.locator('.pin-spacer').count(),0);
   await page.locator('.kinetic').scrollIntoViewIfNeeded();
   await page.waitForTimeout(1200);
   await page.screenshot({path:`qa/r5-${lang}-${width}-${mode}-kinetic.png`});
   await page.goto(base+prefix+'sample.html');
   await page.waitForSelector(`html.${mode==='reduce'?'gentle-ready':'motion-ready'}`);
   await page.waitForFunction(()=>document.querySelector('.score b').textContent==='55');
   await page.waitForTimeout(1500);
   assert.equal(await page.locator('.score-fill').evaluate(el=>getComputedStyle(el).strokeDasharray),'55px, 100px');
   await page.locator('#nhtsa').scrollIntoViewIfNeeded();
   await page.waitForFunction(()=>document.querySelector('[data-count="1825"]').textContent==='1,825');
   await page.locator('.bar-chart').scrollIntoViewIfNeeded();
   await page.waitForTimeout(1700);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.screenshot({path:`qa/r5-${lang}-${width}-${mode}-sample.png`,fullPage:true});
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('PASS Revision 5: en/ru/zh × both motion modes × 360/1440px; gentle movement ≤12px, five-card horizontal travel, native mobile flow, counters/ring, FAQ/schema and neutral copy, no console errors.');
} finally {await browser.close();}
