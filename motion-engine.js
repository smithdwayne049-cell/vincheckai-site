import {phoneAsset} from './phone-assets.js';
// Local exact-version libraries. All motion is scoped to the OS motion preference.
const vendor = new URL('./assets/vendor/', import.meta.url);
const weak = (navigator.deviceMemory && navigator.deviceMemory < 4) ||
  (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) || navigator.connection?.saveData;
let booted = false;
function script(name) {
  return new Promise((resolve, reject) => {
    const el = document.createElement('script');
    el.src = new URL(name, vendor).href;
    el.onload = resolve; el.onerror = reject; document.head.append(el);
  });
}

// Preserve real text, emphasis and line breaks; CJK uses locale word boundaries.
function splitWords(heading) {
  const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    const fragment = document.createDocumentFragment();
    const locale = document.documentElement.lang;
    const pieces = /^(zh|ko)$/.test(locale) && Intl.Segmenter
      ? [...new Intl.Segmenter(locale, {granularity:'word'}).segment(node.textContent)].map(x=>x.segment)
      : node.textContent.split(/(\s+)/);
    for (const piece of pieces) {
      if (!piece.trim()) fragment.append(document.createTextNode(piece));
      else { const word=document.createElement('span');word.className='motion-word';word.textContent=piece;fragment.append(word); }
    }
    node.replaceWith(fragment);
  }
}

export async function startMotion() {
  if (booted) return;
  booted = true;
  await script('gsap.min.js');
  await script('ScrollTrigger.min.js');
  const {default:Lenis} = await import(new URL('lenis.mjs',vendor).href);
  const {gsap,ScrollTrigger} = window;
  gsap.registerPlugin(ScrollTrigger);
  const media = gsap.matchMedia();
  const originalHeadings = new Map();
  let introPlayed = false;
  let firstSetup = true;
  media.add({motion:'(prefers-reduced-motion: no-preference)',desktop:'(min-width:1100px) and (min-height:760px) and (hover:hover) and (pointer:fine)',touch:'(pointer:coarse)'}, context => {
    if(!context.conditions.motion)return;
    const desktop=context.conditions.desktop && !weak;
    const touch=context.conditions.touch;
    const lenis=new Lenis({duration:.95,smoothWheel:!weak,syncTouch:false,anchors:false});
    lenis.on('scroll',ScrollTrigger.update);
    const tick=time=>lenis.raf(time*1000);
    gsap.ticker.add(tick);gsap.ticker.lagSmoothing(0);
    document.documentElement.classList.add('motion-ready');
    const anchorClick=event=>{
      const a=event.target.closest('a[href]');
      if(!a||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||a.target||a.hasAttribute('download'))return;
      const url=new URL(a.href,location.href);
      if(url.origin!==location.origin||url.pathname!==location.pathname||url.search!==location.search||!url.hash)return;
      let target;
      try{target=document.getElementById(decodeURIComponent(url.hash.slice(1)));}catch{return;}
      if(!target)return;
      event.preventDefault();
      if(target.matches('details'))target.open=true;
      if(target.closest('details'))target.closest('details').open=true;
      if(target.closest('.report-grid'))ScrollTrigger.refresh();
      history.pushState(null,'',url.hash);
      // Numeric coordinates avoid counting CSS scroll-padding and scroll-margin twice.
      // Reveal transforms must not shift the final anchor position.
      lenis.resize();
      const transform=getComputedStyle(target).transform;
      const revealY=transform==='none'?0:new DOMMatrixReadOnly(transform).m42;
      const destination=scrollY+target.getBoundingClientRect().top-revealY-90;
      lenis.scrollTo(destination,{onComplete:()=>{
        if(!target.hasAttribute('tabindex')){target.tabIndex=-1;target.addEventListener('blur',()=>target.removeAttribute('tabindex'),{once:true});}
        target.focus({preventScroll:true});
      }});
    };
    document.addEventListener('click',anchorClick);
    const hero=document.querySelector('.hero');
    const stage=document.querySelector('#phone-stage');
    document.querySelectorAll('h1,h2').forEach(h=>{
      if(!originalHeadings.has(h))originalHeadings.set(h,h.innerHTML);
      if(!h.querySelector('.motion-word'))splitWords(h);
    });
    if(!introPlayed&&scrollY<100){
      const title=document.querySelector('h1');
      const words=title?[...title.querySelectorAll('.motion-word')].filter(w=>!w.closest('em')):[];
      const intro=gsap.timeline({defaults:{ease:'power3.out'}});
      intro.from(words,{y:touch?14:30,opacity:.65,filter:touch?'none':'blur(5px)',duration:.65,stagger:.045});
      if(title?.querySelector('em'))intro.from(title.querySelector('em'),{opacity:.25,textShadow:'0 0 30px #ff00cc',duration:.65},'-=.2');
      intro.from(document.querySelectorAll('.hero .actions,.report-head .actions'),{y:16,opacity:.4,duration:.55},'-=.35');
      if(stage)intro.from(stage,{y:28,opacity:.4,duration:.8},'-=.4');
      introPlayed=true;
    }
    if(hero){
      gsap.fromTo(hero,{'--hero-zoom':1.04},{'--hero-zoom':1.12,duration:9,ease:'sine.out'});
      const chapters=[...document.querySelectorAll('.phone-chapter')];
      const progress={value:0};
      let fallbackScreen=0;
      const setPhone=()=>{
        const index=Math.min(3,Math.floor(progress.value*4));
        stage.motion={progress:progress.value,screen:index};
        stage.dataset.phoneProgress=progress.value.toFixed(3);stage.dataset.phoneScreen=String(index);
        if(index!==fallbackScreen){
          fallbackScreen=index;
          stage.querySelector('.phone-fallback').src=phoneAsset(index);
        }
        chapters.forEach((c,i)=>c.classList.toggle('active',i===index));
      };
      const heroScroll=gsap.timeline({scrollTrigger:{
        trigger:hero,start:'top top',end:desktop?'+=1100':'bottom top',
        pin:desktop,pinSpacing:true,scrub:desktop?.65:.3,invalidateOnRefresh:true,
      }});
      heroScroll.to(progress,{value:1,duration:1,ease:'none',onUpdate:setPhone},0);
      heroScroll.to(hero.querySelector('h1'),{scale:.86,opacity:.08,filter:'blur(10px)',transformOrigin:'left center',ease:'none',duration:.55},.45);
      setPhone();
    }
    const featureStage=document.querySelector('.features-stage');
    const track=featureStage?.querySelector('.features');
    if(desktop&&track){
      featureStage.classList.add('horizontal-features');
      const distance=()=>Math.max(0,track.scrollWidth-track.parentElement.clientWidth);
      gsap.to(track,{x:()=>-distance(),ease:'none',scrollTrigger:{trigger:featureStage,start:'top top',end:()=>`+=${distance()+400}`,pin:true,scrub:.7,invalidateOnRefresh:true}});
      gsap.from(track.children,{opacity:.35,y:24,stagger:.12,duration:.7,scrollTrigger:{trigger:featureStage,start:'top 85%',once:true}});
    }
    document.querySelectorAll('h2:not(.kinetic h2)').forEach(h=>{
      gsap.from(h.querySelectorAll('.motion-word'),{y:20,opacity:.25,duration:.65,stagger:.035,
        scrollTrigger:{trigger:h,start:'top 94%',once:true}});
    });
    document.querySelectorAll(`${desktop?'':'.features,'}.steps,.report-grid`).forEach(group=>{
      gsap.utils.toArray(group.children).forEach((card,i)=>{
        gsap.from(card,{y:touch?18:38,opacity:.35,duration:.65,delay:touch?0:(i%3)*.08,
          onComplete:()=>{card.style.removeProperty('transform');card.style.removeProperty('opacity');},
          scrollTrigger:{trigger:card,start:'top 96%',once:true,onEnter:()=>card.classList.add('edge-revealed')}});
      });
    });
    const kinetic=document.querySelector('.kinetic');
    if(kinetic){
      gsap.fromTo(kinetic.querySelectorAll('.motion-word'),{opacity:.3,color:'#8f7ba7',textShadow:'0 0 0px transparent'},
        {opacity:1,color:'#ffe5fa',textShadow:'0 0 28px #ff00cc88',stagger:1,ease:'none',
          scrollTrigger:{trigger:kinetic,start:'top 78%',end:'bottom 35%',scrub:.5}});
    }
    document.querySelectorAll('.cinema').forEach(photo=>{
      gsap.fromTo(photo,{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:1.3,ease:'power3.inOut',
        scrollTrigger:{trigger:photo.parentElement,start:'top 96%',once:true}});
    });
    const counters=[...document.querySelectorAll('[data-count]')];
    const originals=new Map(counters.map(el=>[el,el.textContent]));
    counters.forEach(el=>{
      const number={value:0};const total=Number(el.dataset.count);
      gsap.to(number,{value:total,duration:1.3,ease:'power2.out',scrollTrigger:{trigger:el,start:'top 96%',once:true},
        onStart:()=>{el.style.minWidth=`${el.offsetWidth}px`;},
        onUpdate:()=>{el.textContent=Math.round(number.value).toLocaleString(document.documentElement.lang);},
        onComplete:()=>{el.textContent=originals.get(el);}});
    });
    const ring=document.querySelector('.score-fill');
    if(ring)gsap.fromTo(ring,{strokeDasharray:'0 100'},{strokeDasharray:'55 100',duration:1.4,ease:'power2.out',scrollTrigger:{trigger:ring.closest('.score'),start:'top 96%',once:true}});
    document.querySelectorAll('.bar-track span').forEach((bar,i)=>gsap.from(bar,{scaleX:0,transformOrigin:'left',duration:1,delay:i*.06,ease:'power2.out',scrollTrigger:{trigger:bar,start:'top 97%',once:true}}));
    document.querySelectorAll('.cinematic').forEach(section=>{
      gsap.fromTo(section,{'--photo-y':'-12px'},{'--photo-y':'12px',ease:'none',scrollTrigger:{trigger:section,start:'top bottom',end:'bottom top',scrub:.5}});
    });
    const removeMagnet=[];
    if(!touch&&!weak)document.querySelectorAll('.play').forEach(button=>{
      const x=gsap.quickTo(button,'x',{duration:.35,ease:'power3.out'});
      const y=gsap.quickTo(button,'y',{duration:.35,ease:'power3.out'});
      const move=e=>{const r=button.getBoundingClientRect();x((e.clientX-r.left-r.width/2)*.13);y((e.clientY-r.top-r.height/2)*.2);};
      const leave=()=>{x(0);y(0);};
      button.addEventListener('pointermove',move);button.addEventListener('pointerleave',leave);
      removeMagnet.push(()=>{button.removeEventListener('pointermove',move);button.removeEventListener('pointerleave',leave);});
    });
    let distortion;let active=true;
    const hover=async event=>{
      if(!desktop||!active)return;
      const section=event.target.closest('.cinematic');
      if(!section||section.contains(event.relatedTarget))return;
      if(!distortion){try{distortion=await import('./photo-effect.js');}catch{return;}}
      if(active&&section.matches(':hover'))distortion.showPhoto(section,event);
    };
    document.addEventListener('pointerover',hover);
    const toggled=event=>{if(event.target.matches('details'))ScrollTrigger.refresh();};
    document.addEventListener('toggle',toggled,true);
    const refresh=()=>ScrollTrigger.refresh();addEventListener('load',refresh,{once:true});
    ScrollTrigger.refresh();
    // Native hash navigation precedes the deferred pin. Restore its target once
    // the new layout exists, including direct links to mobile report disclosures.
    if(firstSetup&&location.hash){
      let target;
      try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{}
      if(target){
        if(target.matches('details'))target.open=true;
        ScrollTrigger.refresh();lenis.resize();
        const transform=getComputedStyle(target).transform;
        const y=transform==='none'?0:new DOMMatrixReadOnly(transform).m42;
        lenis.scrollTo(scrollY+target.getBoundingClientRect().top-y-90,{immediate:true});
      }
    }
    firstSetup=false;
    return ()=>{
      active=false;distortion?.disposePhoto();
      document.removeEventListener('pointerover',hover);document.removeEventListener('toggle',toggled,true);removeEventListener('load',refresh);
      removeMagnet.forEach(remove=>remove());document.removeEventListener('click',anchorClick);
      gsap.ticker.remove(tick);lenis.destroy();document.documentElement.classList.remove('motion-ready');
      featureStage?.classList.remove('horizontal-features');
      for(const [h,html]of originalHeadings)h.innerHTML=html;
      counters.forEach(el=>{el.textContent=originals.get(el);el.style.removeProperty('min-width');});
      if(stage){delete stage.motion;delete stage.dataset.phoneScreen;delete stage.dataset.phoneProgress;stage.querySelector('.phone-fallback').src=phoneAsset();}
      document.querySelectorAll('.phone-chapter').forEach((c,i)=>c.classList.toggle('active',i===0));
    };
  });
}
