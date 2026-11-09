// No continuous render loop, smooth scrolling, pinning, parallax or GPU scene.
export function startGentle() {
  document.documentElement.classList.add('gentle-ready');
  const animations = new Set();
  const frames = new Set();
  const originals = new Map();
  function animate(el, keys, duration = 950, delay = 0) {
    const animation = el.animate(keys, {duration, delay, easing:'ease-out'});
    animations.add(animation);
    animation.onfinish = () => animations.delete(animation);
  }
  const observer = new IntersectionObserver(entries => {
    for (const {target:el, isIntersecting} of entries) {
      if (!isIntersecting) continue;
      observer.unobserve(el);
      el.dataset.gentleSeen = 'true';
      if (el.matches('[data-count]')) {
        const original = el.textContent;
        originals.set(el, original);
        const start = performance.now();
        const total = Number(el.dataset.count);
        const frame = now => {
          const progress = Math.min(1, (now-start)/1200);
          el.textContent = progress === 1 ? original : Math.round(total*(1-(1-progress)**3)).toLocaleString(document.documentElement.lang);
          if (progress < 1) {
            const id = requestAnimationFrame(t => { frames.delete(id); frame(t); });
            frames.add(id);
          }
        };
        frame(start);
      } else if (el.matches('.score-fill')) {
        animate(el, [{strokeDasharray:'0 100'}, {strokeDasharray:'55 100'}], 1300);
      } else if (el.matches('.bar-track span')) {
        animate(el, [{opacity:.25, filter:'brightness(.6)'}, {opacity:1, filter:'brightness(1)'}]);
      } else {
        const index = [...el.parentElement.children].indexOf(el);
        animate(el, [{opacity:.4, transform:'translateY(10px)'}, {opacity:1, transform:'translateY(0)'}], 1000, (index%3)*70);
      }
    }
  }, {threshold:.08});
  document.querySelectorAll('h1,h2,.hero .actions,.feature,.step,.report-card,[data-count],.score-fill,.bar-track span').forEach(el=>observer.observe(el));
  return () => {
    observer.disconnect(); animations.forEach(a=>a.cancel()); frames.forEach(cancelAnimationFrame);
    originals.forEach((text, el)=>{el.textContent=text;});
    document.querySelectorAll('[data-gentle-seen]').forEach(el=>delete el.dataset.gentleSeen);
    document.documentElement.classList.remove('gentle-ready');
  };
}
