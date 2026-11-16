import lighthouse from 'lighthouse';
import {launch} from 'chrome-launcher';
import fs from 'node:fs/promises';
const chrome=await launch({chromeFlags:['--headless=new','--no-sandbox','--disable-gpu']});
try {
  await fs.mkdir('qa',{recursive:true});
  for(const [name,path] of [['ford','ford-vin-decoder.html'],['pt-subscription','pt/vin-check-no-subscription.html']]){
    const {lhr,report}=await lighthouse(`http://127.0.0.1:4173/${path}`,{port:chrome.port,output:'json',onlyCategories:['performance','accessibility','best-practices','seo']});
    await fs.writeFile(`qa/lighthouse-r9-${name}.json`,report);
    console.log(path,JSON.stringify(Object.fromEntries(Object.entries(lhr.categories).map(([k,v])=>[k,Math.round(v.score*100)]))));
    if(lhr.categories.performance.score<.85)process.exitCode=1;
  }
} finally {
  await Promise.race([chrome.kill(),new Promise(resolve=>setTimeout(resolve,5000))]);
  process.exit(process.exitCode||0);
}
