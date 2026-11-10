// Private app dictionaries are read only at build time, never copied to public assets.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {chromium} from '@playwright/test';
import {execFileSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const copy=JSON.parse(await fs.readFile(path.join(root,'scripts/phone-copy.json'),'utf8'));
const out=path.join(root,'qa/phone-screens');await fs.mkdir(out,{recursive:true});
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const shapes={back:'<path d="m14 6-6 6 6 6M8 12h12"/>',search:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',camera:'<path d="M3 7h4l2-3h6l2 3h4v14H3Z"/><circle cx="12" cy="13" r="4"/>',scan:'<path d="M3 8V3h5m8 0h5v5M3 16v5h5m8 0h5v-5M7 7h3v3H7Zm7 0h3v3h-3ZM7 14h3v3H7Zm7 0h3v3h-3Z"/>',history:'<path d="M4 8a9 9 0 1 1-1 8M4 3v5H0m12-2v7l4 2"/>',money:'<rect x="3" y="5" width="16" height="12" rx="2" fill="currentColor" stroke="none"/><circle cx="11" cy="11" r="3" fill="#29345a" stroke="none"/><path d="M7 21h16V9"/>',mileage:'<path d="M3 18a9 9 0 1 1 18 0ZM12 14l5-6"/>',shield:'<path d="m12 2 9 4v7c0 6-9 10-9 10S3 19 3 13V6Z"/>',flag:'<circle cx="12" cy="12" r="8"/><path d="M12 7v6m0 4h.01"/>',trophy:'<path d="M7 3h10v7a5 5 0 0 1-10 0ZM7 5H3v4c0 3 4 4 5 4m9-8h4v4c0 3-4 4-5 4m-4 2v5m-5 1h10"/>'};
const svg=n=>`<svg viewBox="0 0 24 24">${shapes[n]}</svg>`;
const icon=n=>`<span class="icon">${svg(n)}</span>`;
const browser=await chromium.launch({channel:'chrome',headless:true});
const fit=[];
try{
 const page=await browser.newPage({viewport:{width:1080,height:2340},deviceScaleFactor:1});
 for(const lang of Object.keys(copy)){
  const d=JSON.parse(await fs.readFile(path.join(root,`data/app_strings/${lang}.json`),'utf8'));
  const t=k=>{if(!d[k])throw Error(`Missing app label ${lang}:${k}`);return esc(d[k]);};
  const bar=key=>`<header class="bar"><span class="back">${svg('back')}</span><span class="bar-title" data-fit>${t(key)}</span></header>`;
  const heading=(key,n)=>`<h2 class="card-title">${icon(n)}<span data-fit>${t(key)}</span></h2>`;
  const market=`<section class="card spec-market">${heading('report_market_value_title','money')}<p class="value">EUR 15,400</p><p class="muted">${t('report_market_value_caveat')}</p></section>`;
  const profile=[['make','Skoda'],['model','Octavia'],['year','2019'],['body','Wagon'],['cylinders','4'],['fuel','Gasoline'],['transmission','Automatic (7-speed DSG)'],['country','Czech Republic'],['vin','TMBJG7NE5K0284716']];
  const card=(key,n,accent,lines)=>`<section class="card flag-card" style="--accent:${accent}">${heading(key,n)}<ul>${lines.map(v=>`<li>${esc(v)}</li>`).join('')}</ul></section>`;
  const pair=values=>`<div class="pair">${values.map((v,i)=>`<div class="mini"><h3>${i?'2018 Mercedes-Benz C 220d':'2018 BMW 320d'}</h3><p>${v}</p></div>`).join('')}</div>`;
  const screens={
   scan:`<div class="scan-head"><span class="scan-logo">${svg('scan')}</span><div class="scan-brand"><strong data-fit>${t('vin_title').toLocaleUpperCase(lang)}</strong><small>AI · NHTSA · Supabase</small></div><span class="history">${svg('history')}</span></div><div class="scan-panel"><div class="field-label" data-fit>● ${t('vin_field_label').toLocaleUpperCase(lang)}</div><div class="vin-entry"><span class="hash">#</span><span class="vin-number">TMBJG7NE5K0284716</span><span class="camera">${svg('camera')}</span><span class="clear">×</span></div><div class="underline"></div><div class="field-hints"><span data-fit>${t('vin_char_count').replace('{}','17')}</span><span data-fit>${t('vin_no_ioq_hint')}</span></div></div><div class="decode-button">${svg('search')}<span data-fit>${t('vin_decode').toLocaleUpperCase(lang)}</span></div><p class="empty" data-fit>${t('vin_decoder_empty_hint')}</p>`,
   specs:bar('report_title')+`<div class="content"><section class="card profile"><h1 data-fit>${t('report_vehicle_profile_title')}</h1><dl class="specs">${profile.map(([k,v])=>`<dt data-fit>${t('report_label_'+k)}</dt><dd class="${k==='vin'?'vin':''}">${esc(v).replace('7-speed DSG','7-speed<br>DSG')}</dd>`).join('')}</dl></section>${market}<section class="card" style="--accent:#00b9ff">${heading('report_mileage_history_title','mileage')}</section></div>`,
   flags:bar('report_title')+`<div class="content flag-content">${card('report_red_flags_title','flag','#ff5e77',copy[lang].slice(0,2))}${card('report_what_to_check_title','search','#5f91ff',copy[lang].slice(2,5))}${card('report_negotiation_leverage_title','money','#39da73',copy[lang].slice(5,8))}</div>`,
   compare:bar('compare_report_title')+`<div class="content compare-content"><div class="cars">${['A','B'].map((v,i)=>`<section class="car ${i?'b':''}"><span class="letter">${v}</span><div class="year">2018</div><strong>${i?'Mercedes-Benz':'BMW'}</strong><div class="model">${i?'C 220d':'320d'}</div><p>${t('report_label_body')}: <b>Sedan</b></p><p>${t('report_label_fuel')}: <b>Diesel</b></p><p>${t('report_label_country')}: <b>Germany</b></p></section>`).join('')}</div><section class="card comparison"><div class="result-title">${icon('trophy')}<span data-fit>${t('compare_result_header').toLocaleUpperCase(lang)}</span><span class="badge">${t('common_level_high').toLocaleUpperCase(lang)}</span></div><div class="result-body"><div class="winner"><span class="trophy">${svg('trophy')}</span><div><small>${t('compare_winner_label').toLocaleUpperCase(lang)}</small>${t('common_vehicle_a')} — 2018 BMW 320d</div></div><p>${esc(copy[lang][8])}</p></div></section><section class="card">${heading('report_market_value_title','money')}${pair(['EUR 21,300','EUR 22,800'])}</section><section class="card">${heading('report_stolen_check_title','shield')}${pair([t('report_stolen_check_unavailable_region'),t('report_stolen_check_unavailable_region')])}</section></div>`
  };
  for(const [name,body] of Object.entries(screens)){
   const file=path.join(out,`${lang}-${name}.html`);
   await fs.writeFile(file,`<!doctype html><html lang="${lang}"><meta charset="utf-8"><link rel="stylesheet" href="../../scripts/phone-screen.css"><body><main class="screen ${name}" lang="${lang}">${body}</main></body></html>`);
   await page.goto(pathToFileURL(file).href);await page.evaluate(()=>document.fonts.ready);
   // Fit only single-line labels. Body copy wraps naturally and cards grow with it.
   const sizes=await page.evaluate(()=>[...document.querySelectorAll('[data-fit]')].map(el=>{
    const initial=parseFloat(getComputedStyle(el).fontSize);let size=initial;
    while(el.scrollWidth>el.clientWidth+1&&size>initial*.70){size-=.25;el.style.fontSize=size+'px';}
    return {text:el.textContent,size,overflow:el.scrollWidth>el.clientWidth+1};
   }));
   if(sizes.some(x=>x.overflow))throw Error(`${lang}/${name}: overflowing label ${JSON.stringify(sizes)}`);
   fit.push({lang,name,labels:sizes});
   await page.screenshot({path:path.join(out,`${lang}-${name}.png`)});
  }
 }
 await fs.writeFile(path.join(out,'fit.json'),JSON.stringify(fit,null,2));
}finally{await browser.close();}
execFileSync('python',[path.join(root,'scripts/compress-phone-screens.py')],{stdio:'inherit'});
