import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const base='http://127.0.0.1:4173';
const errors=[];
await fs.mkdir('qa',{recursive:true});
try{
 for(const mobile of [false,true]){
  const context=await browser.newContext({viewport:{width:mobile?360:1440,height:mobile?800:1000},isMobile:mobile,hasTouch:mobile});
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  for(const lang of ['en','ru','zh']){
   const prefix=lang==='en'?'/':`/${lang}/`;
   await page.goto(base+prefix);
   await page.waitForSelector('html.motion-ready');
   await page.waitForTimeout(2100);
   assert.equal(await page.locator('.pin-spacer').count(),mobile?0:2);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(!mobile){
    await page.waitForSelector('.has-scene');
    for(const [y,screen]of [[180,0],[470,1],[800,2],[1160,3]]){
     await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);
     await page.waitForFunction(s=>document.querySelector('#phone-stage').dataset.renderedScreen===String(s),screen);
     assert.equal(await page.locator('.phone-chapter.active').count(),1);
    }
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await page.locator('.hero-copy').hover();
    await page.waitForSelector('.photo-ripple');
    await page.screenshot({path:`qa/r4-${lang}-hero.png`});
    await page.locator('.nav .brand').hover();
    await page.waitForSelector('.photo-ripple',{state:'detached'});
   }
   await page.locator('.navlinks a[href$="#faq"]').evaluate(el=>el.click());
   await page.waitForFunction(()=>Math.abs(document.querySelector('#faq').getBoundingClientRect().top-90)<12);
   assert.equal(new URL(page.url()).hash,'#faq');
   await page.goto(base+prefix+'sample.html');
   await page.waitForSelector('html.motion-ready');
   await page.locator('.report-nav a[href="#red-flags"]').click();
   await page.waitForFunction(()=>Math.abs(document.querySelector('#red-flags').getBoundingClientRect().top-90)<14);
   assert(await page.locator('#red-flags').evaluate(el=>el.open));
   await page.locator('.report-nav a[href="#verdict"]').click();
   await page.waitForFunction(()=>document.querySelector('.score b').textContent==='55');
   await page.waitForTimeout(1600);
   assert.equal(await page.locator('.score-fill').evaluate(el=>getComputedStyle(el).strokeDasharray),'55px, 100px');
   await page.locator('.report-nav a[href="#nhtsa"]').click();
   await page.waitForFunction(()=>document.querySelector('[data-count="1825"]').textContent==='1,825');
   await page.locator('.bar-chart').scrollIntoViewIfNeeded();
   await page.waitForTimeout(1600);
   assert(await page.locator('.bar-track span').first().evaluate(el=>getComputedStyle(el).transform==='matrix(1, 0, 0, 1, 0, 0)'));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.screenshot({path:`qa/r4-${lang}-${mobile?'mobile':'desktop'}-sample.png`,fullPage:true});
   await page.emulateMedia({reducedMotion:'reduce'});
   await page.waitForSelector('html.motion-ready',{state:'detached'});
   assert.equal(await page.locator('.pin-spacer,.photo-ripple').count(),0);
   assert.equal(await page.locator('.motion-word').count(),0);
   await page.waitForFunction(()=>document.querySelector('[data-count="1825"]').textContent==='1,825');
   await page.emulateMedia({reducedMotion:'no-preference'});
   await page.waitForSelector('html.motion-ready');
  }
  await page.goto(base+'/ru/#features');await page.waitForSelector('html.motion-ready');
  await page.waitForFunction(()=>Math.abs(document.querySelector('#features').getBoundingClientRect().top-90)<14);
  await page.goto(base+'/ru/sample.html#red-flags');await page.waitForSelector('html.motion-ready');
  await page.waitForFunction(()=>Math.abs(document.querySelector('#red-flags').getBoundingClientRect().top-90)<14);
  assert(await page.locator('#red-flags').evaluate(el=>el.open));
  await context.close();
 }
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await context.newPage();const requests=[];
 page.on('request',r=>requests.push(r.url()));
 await page.goto(base+'/ru/');await page.waitForTimeout(1300);
 assert(!requests.some(u=>/gsap|ScrollTrigger|lenis|photo-effect/.test(u)));
 assert.equal(await page.locator('.has-scene,.pin-spacer').count(),0);
 await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForSelector('html.motion-ready');
 await page.waitForSelector('.has-scene');
 await page.locator('.hero-copy').hover();await page.waitForSelector('.photo-ripple');
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.waitForSelector('html.motion-ready',{state:'detached'});
 assert.equal(await page.locator('.has-scene,.pin-spacer,.photo-ripple').count(),0);
 assert((await page.locator('.phone-fallback').getAttribute('src')).endsWith('/phone.webp'));
 await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForSelector('html.motion-ready');
 await page.setViewportSize({width:360,height:800});await page.waitForTimeout(500);
 assert.equal(await page.locator('.pin-spacer').count(),0);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('PASS: en/ru/zh normal motion desktop/mobile, four rendered screens, pin, hover WebGL, anchors, sticky report nav, counters/bars/ring, dynamic reduced motion and responsive cleanup.');
}finally{await browser.close();}
