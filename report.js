import {enhance} from './motion.js';
enhance();
const mobile=matchMedia('(max-width:700px)');
const panels=[...document.querySelectorAll('.disclosure')];
function disclosures(){for(const p of panels)p.open=!mobile.matches;}
disclosures();mobile.addEventListener('change',disclosures);
const links=[...document.querySelectorAll('.report-nav a')];
const observer=new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){for(const a of links)a.classList.toggle('active',a.hash==='#'+e.target.id);}}},{rootMargin:'-65px 0px -55% 0px'});
for(const a of links){const target=document.querySelector(a.hash);if(target){observer.observe(target);a.addEventListener('click',()=>{if(target.tagName==='DETAILS')target.open=true;});}}
