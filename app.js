import {phoneAsset} from './phone-assets.js';
const stage = document.querySelector('#phone-stage');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const weak = (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) || navigator.connection?.saveData;
let sceneCleanup;
let starting = false;
async function startScene() {
  if (!stage || reduced.matches || weak || document.hidden || starting || sceneCleanup) return;
  starting = true;
  // Probe support before downloading the 3D library. The HTML phone is always available.
  const probe = document.createElement('canvas');
  const context = probe.getContext('webgl2', {failIfMajorPerformanceCaveat:true});
  if (!context) {starting=false;return;}
  context.getExtension('WEBGL_lose_context')?.loseContext();
  try {
    const THREE = await import('./assets/vendor/three.module.min.js');
    if (reduced.matches) return;
    const canvas = stage.querySelector('canvas');
    const renderer = new THREE.WebGLRenderer({canvas, alpha:true, antialias:true, powerPreference:'low-power'});
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(39, 1, .1, 100);
    camera.position.set(0, 0, 9.4);
    scene.add(new THREE.AmbientLight(0xe6d6ff, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 4); key.position.set(3, 5, 6); scene.add(key);
    const pink = new THREE.PointLight(0xff00cc, 25, 20); pink.position.set(-4, 1, 3); scene.add(pink);
    const violet = new THREE.PointLight(0x9977ff, 30, 20); violet.position.set(4, -2, 2); scene.add(violet);
    const phone = new THREE.Group(); scene.add(phone);
    const shape = new THREE.Shape();
    const w=2.42, h=5.02, r=.34;
    shape.moveTo(-w/2+r,-h/2); shape.lineTo(w/2-r,-h/2);
    shape.quadraticCurveTo(w/2,-h/2,w/2,-h/2+r); shape.lineTo(w/2,h/2-r);
    shape.quadraticCurveTo(w/2,h/2,w/2-r,h/2); shape.lineTo(-w/2+r,h/2);
    shape.quadraticCurveTo(-w/2,h/2,-w/2,h/2-r); shape.lineTo(-w/2,-h/2+r);
    shape.quadraticCurveTo(-w/2,-h/2,-w/2+r,-h/2);
    const body = new THREE.Mesh(new THREE.ExtrudeGeometry(shape,{depth:.13, bevelEnabled:true, bevelSegments:3, steps:1, bevelSize:.045, bevelThickness:.045, curveSegments:12}),new THREE.MeshStandardMaterial({color:0x443d50,metalness:.85,roughness:.23}));
    phone.add(body);
    const texture = await new THREE.TextureLoader().loadAsync(phoneAsset());
    const textures = new Map([[0,texture]]);
    const pendingTextures = new Set();
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(),4);
    const front = new THREE.Mesh(new THREE.PlaneGeometry(2.43,5.022),new THREE.MeshBasicMaterial({map:texture,transparent:true,depthWrite:false}));
    front.position.z=.184; phone.add(front);
    const buttonMaterial = new THREE.MeshStandardMaterial({color:0x887d9e, metalness:.9, roughness:.2});
    for (const [x,y,len] of [[1.24,.65,.52],[-1.24,.9,.3],[-1.24,.4,.3]]) {
      const button = new THREE.Mesh(new THREE.BoxGeometry(.04,len,.1),buttonMaterial);
      button.position.set(x,y,.05); phone.add(button);
    }
    // A small, fixed particle field adds depth without large transparent surfaces.
    const positions = new Float32Array(54*3);
    for(let i=0;i<54;i++){positions[i*3]=Math.sin(i*71.23)*5; positions[i*3+1]=Math.cos(i*24.8)*4; positions[i*3+2]=-1-Math.abs(Math.sin(i))*3;}
    const particlesGeometry = new THREE.BufferGeometry();
    particlesGeometry.setAttribute('position',new THREE.BufferAttribute(positions,3));
    const particles = new THREE.Points(particlesGeometry,new THREE.PointsMaterial({color:0xb488ea,size:.017,transparent:true,opacity:.65}));scene.add(particles);
    let visible = false, disposed = false, frame = 0, pointerX=0, pointerY=0;
    const clock = new THREE.Clock();
    function resize(){if(disposed)return;const {width,height}=stage.getBoundingClientRect();renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();}
    const resizeObserver = new ResizeObserver(resize);resizeObserver.observe(stage);resize();
    function render(){
      // Also check at the frame boundary: browser media events can arrive after
      // ScrollTrigger has already reverted the pinned stage and resized it.
      if(reduced.matches){sceneCleanup?.();frame=0;return;}
      if(disposed||!visible||document.hidden){frame=0;return;}
      const time=clock.getElapsedTime();
      const scroll=stage.motion?.progress ?? Math.min(window.scrollY / innerHeight,1);
      const screen=stage.motion?.screen ?? 0;
      if(textures.has(screen)) {front.material.map=textures.get(screen);stage.dataset.renderedScreen=String(screen);}
      else if(!pendingTextures.has(screen)){
        pendingTextures.add(screen);
        new THREE.TextureLoader().loadAsync(phoneAsset(screen)).then(next=>{
          if(disposed){next.dispose();return;}
          next.colorSpace=THREE.SRGBColorSpace;next.anisotropy=texture.anisotropy;textures.set(screen,next);
        }).catch(()=>{});
      }
      phone.rotation.set(.035+pointerY*.06+Math.sin(scroll*Math.PI)*.12,-.26+pointerX*.13+Math.sin(scroll*Math.PI*2)*.72,-.12+scroll*.24);
      phone.position.set(Math.sin(scroll*Math.PI*2)*.2,Math.sin(time*.8)*.055+Math.sin(scroll*Math.PI)*.25,Math.sin(scroll*Math.PI)*.25);
      particles.rotation.z=time*.007;
      renderer.render(scene,camera); stage.classList.add('has-scene');
      frame=requestAnimationFrame(render);
    }
    function resume(){if(visible&&!document.hidden&&!frame&&!disposed)frame=requestAnimationFrame(render);}
    const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;resume();},{threshold:0});observer.observe(stage);
    const onPointer=(event)=>{const rect=stage.getBoundingClientRect();pointerX=(event.clientX-rect.left)/rect.width-.5;pointerY=(event.clientY-rect.top)/rect.height-.5;};
    stage.addEventListener('pointermove',onPointer,{passive:true});
    document.addEventListener('visibilitychange',resume);
    const contextLost=(event)=>{event.preventDefault();sceneCleanup?.();};
    canvas.addEventListener('webglcontextlost',contextLost);
    sceneCleanup=()=>{
      if(disposed)return;disposed=true;cancelAnimationFrame(frame);observer.disconnect();resizeObserver.disconnect();
      stage.classList.remove('has-scene');stage.removeEventListener('pointermove',onPointer);document.removeEventListener('visibilitychange',resume);canvas.removeEventListener('webglcontextlost',contextLost);
      scene.traverse(object=>{object.geometry?.dispose();if(object.material){for(const material of [object.material].flat())material.dispose();}});textures.forEach(t=>t.dispose());renderer.dispose();
      sceneCleanup=undefined;delete stage.dataset.renderedScreen;
    };
    if(reduced.matches)sceneCleanup();
  } catch {
    // Offline, unsupported WebGL and load failures retain the static phone.
    stage.classList.remove('has-scene');
  } finally {starting=false;}
}
reduced.addEventListener('change',()=>{if(reduced.matches){sceneCleanup?.();}else startScene();});
addEventListener('pagehide',()=>sceneCleanup?.(),{once:true});
// Build the GPU scene only when most of the phone can actually be seen.
// On small screens the first viewport uses the lightweight static phone.
if(stage){
  const startup=new IntersectionObserver(([entry])=>{
    if(entry.intersectionRatio<.7)return;
    startup.disconnect();
    const launch=()=>{if('requestIdleCallback' in window)requestIdleCallback(startScene,{timeout:2200});else setTimeout(startScene,300);};
    if(document.readyState==='complete')launch();else addEventListener('load',launch,{once:true});
  },{threshold:.7});
  startup.observe(stage);
}


import {enhance} from './motion.js';
enhance();
