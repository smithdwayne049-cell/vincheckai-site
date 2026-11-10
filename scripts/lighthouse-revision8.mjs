import lighthouse from 'lighthouse';
import {launch} from 'chrome-launcher';
import fs from 'node:fs/promises';
const chrome=await launch({chromeFlags:['--headless=new','--no-sandbox','--disable-gpu']});
try{
 for(const lang of ['en','ru','de','zh']){
  const {lhr,report}=await lighthouse(`http://127.0.0.1:4173/${lang==='en'?'':lang+'/'}`,{
   port:chrome.port,output:'json',onlyCategories:['performance','accessibility','best-practices','seo']
  });
  await fs.writeFile(`qa/lighthouse-r8-${lang}.json`,report);
  console.log(lang,JSON.stringify(Object.fromEntries(Object.entries(lhr.categories).map(([k,v])=>[k,Math.round(v.score*100)]))));
  if(lhr.categories.performance.score<.85)process.exitCode=1;
 }
}finally{
 // Windows can retain Chrome's temporary profile after the audits have ended.
 await Promise.race([chrome.kill(),new Promise(resolve=>setTimeout(resolve,5000))]);
 process.exit(process.exitCode || 0);
}
