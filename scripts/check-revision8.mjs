import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:4173';
const langs=['en','ru','de','es','fr','it','pt','tr','ko','zh'];
const route=lang=>lang==='en'?'/':`/${lang}/`;
const errors=[];
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 for(const lang of langs){
  for(const name of ['scan','specs','flags','compare','phone','phone-specs','phone-flags','phone-compare']){
   const file=`assets/web/screens/${lang}/${name}.webp`;
   assert((await fs.stat(file)).size<120000,`${file} exceeds budget`);
  }
 }
 for(const width of [360,1440]){
  const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:'reduce'});
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  for(const lang of langs){
   await page.goto(base+route(lang));
   const phone=page.locator('.phone-fallback');await phone.evaluate(el=>el.decode());
   assert((await phone.getAttribute('src')).endsWith(`/screens/${lang}/phone.webp`));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${lang}: overflow ${width}`);
   assert.equal(await page.locator('.has-scene').count(),0);
   for(const img of await page.locator('img[src*="/screens/"]').all()){
    assert((await img.getAttribute('src')).includes(`/screens/${lang}/`));
   }
   if(['en','ru','de','zh','ko'].includes(lang))await page.screenshot({path:`qa/r8-${lang}-${width}.png`});
  }
  await context.close();
 }
 // Observe actual network requests as the WebGL texture and fallback change together.
 for(const lang of ['en','ru','de','zh']){
  console.log(`Checking ${lang}: WebGL screens and reduced motion`);
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  const page=await context.newPage();const requests=[];
  page.on('request',r=>{if(r.url().includes('/screens/'))requests.push(r.url());});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.goto(base+route(lang));
  await page.waitForSelector('.has-scene');
  for(const [y,index] of [[180,0],[470,1],[800,2],[1160,3]]){
   await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);
   await page.waitForFunction(i=>document.querySelector('#phone-stage').dataset.renderedScreen===String(i),index);
   const name=['phone','phone-specs','phone-flags','phone-compare'][index];
   assert(requests.some(u=>u.endsWith(`/screens/${lang}/${name}.webp`)),`${lang}/${name} texture missing`);
   assert((await page.locator('.phone-fallback').getAttribute('src')).endsWith(`/screens/${lang}/${name}.webp`));
  }
  assert(requests.every(u=>u.includes(`/screens/${lang}/`)),`${lang} loaded another language`);
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.waitForSelector('.has-scene',{state:'detached'});
  assert((await page.locator('.phone-fallback').getAttribute('src')).endsWith(`/screens/${lang}/phone.webp`));
  await context.close();
 }
 for(const mode of ['weak','no-webgl']){
  const context=await browser.newContext({viewport:{width:360,height:800}});
  await context.addInitScript(mode=>{
   if(mode==='weak')Object.defineProperty(navigator,'hardwareConcurrency',{get:()=>2});
   else {const get=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type.startsWith('webgl')?null:get.call(this,type,...args);};}
  },mode);
  const page=await context.newPage();await page.goto(base+'/ru/');
  await page.waitForTimeout(1500);
  assert.equal(await page.locator('.has-scene').count(),0);
  assert(await page.locator('.phone-fallback').evaluate(el=>el.complete&&el.naturalWidth>0));
  await context.close();
 }
 // Check every Russian page, including text inside metadata and JSON-LD.
 for(const name of ['index','sample','decode','pricing']){
  const text=await fs.readFile(`ru/${name}.html`,'utf8');
  assert(!/(?:\bвы\b|Ваш|ваш|Проверьте|Попробуйте|решайте)/u.test(text),`Formal Russian in ${name}`);
 }
 assert.deepEqual(errors,[]);
 console.log('PASS: 80 assets <120 KB, 10 languages at 360/1440px, en/ru/de/zh four WebGL + fallback states, reduced motion cleanup, weak/no-WebGL fallback, Russian register, no console errors.');
}finally{await browser.close();}
