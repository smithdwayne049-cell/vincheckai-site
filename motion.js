// Shared deferred entry. The complete static presentation survives a failed load.
let started = false;
export function enhance() {
  if (started) return;
  started = true;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let engine;
  let gentle;
  let stopGentle;
  async function launch() {
    if (reduced.matches) {
      gentle = await import('./gentle-motion.js');
      if (reduced.matches && !stopGentle) stopGentle = gentle.startGentle();
      return;
    }
    stopGentle?.(); stopGentle = undefined;
    if (engine) return;
    try {
      engine = await import('./motion-engine.js');
      await engine.startMotion();
    } catch { /* Keep all HTML visible if an optional library fails. */ }
  }
  function schedule() {
    if ('requestIdleCallback' in window) requestIdleCallback(launch, {timeout:1200});
    else setTimeout(launch, 100);
  }
  // GSAP reverts synchronously on preference changes; start gentle effects afterward.
  reduced.addEventListener('change', () => setTimeout(launch, 0));
  if (document.readyState === 'complete') schedule();
  else addEventListener('load', schedule, {once:true});
}
