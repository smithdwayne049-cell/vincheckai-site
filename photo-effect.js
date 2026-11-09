// A single transient desktop hover surface. The original image is always below it.
import * as THREE from './assets/vendor/three.module.min.js';
let cleanup;
let generation=0;
export function disposePhoto(){generation++;cleanup?.();cleanup=undefined;}
export async function showPhoto(section,event){
  disposePhoto();
  const request=generation;
  const picture=section.querySelector('.cinema');
  const image=picture?.querySelector('img');
  if(!image||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  const canvas=document.createElement('canvas');
  const context=canvas.getContext('webgl2',{alpha:true,antialias:false,failIfMajorPerformanceCaveat:true,powerPreference:'low-power'});
  if(!context)return;
  let renderer,texture,geometry,material,frame=0,observer,resizeObserver;
  let disposed=false;
  const stop=()=>{
    if(disposed)return;disposed=true;cancelAnimationFrame(frame);
    section.removeEventListener('pointermove',move);section.removeEventListener('pointerleave',disposePhoto);
    document.removeEventListener('visibilitychange',hidden);
    observer?.disconnect();resizeObserver?.disconnect();
    canvas.remove();texture?.dispose();geometry?.dispose();material?.dispose();renderer?.dispose();
    context.getExtension('WEBGL_lose_context')?.loseContext();
  };
  cleanup=stop;
  const mouse=new THREE.Vector2(.5,.5);
  function move(e){const r=picture.getBoundingClientRect();mouse.set((e.clientX-r.left)/r.width,1-(e.clientY-r.top)/r.height);}
  function hidden(){if(document.hidden)disposePhoto();}
  try{
    renderer=new THREE.WebGLRenderer({canvas,context,alpha:true,antialias:false});
    renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
    texture=await new THREE.TextureLoader().loadAsync(image.currentSrc||image.src);
    if(disposed||request!==generation||!section.matches(':hover')){texture.dispose();stop();return;}
    texture.colorSpace=THREE.SRGBColorSpace;
    geometry=new THREE.PlaneGeometry(2,2);
    material=new THREE.ShaderMaterial({uniforms:{photo:{value:texture},time:{value:0},mouse:{value:mouse},ratio:{value:new THREE.Vector2(1,1)},amount:{value:0}},
      vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}',
      fragmentShader:`uniform sampler2D photo;uniform float time;uniform float amount;uniform vec2 mouse;uniform vec2 ratio;varying vec2 vUv;
      void main(){vec2 uv=(vUv-.5)*ratio+.5;vec2 delta=vUv-mouse;float d=length(delta);float wave=sin(d*32.-time*3.)*exp(-d*5.)*amount;
      vec2 shift=normalize(delta+vec2(.0001))*wave;vec2 p=clamp(uv+shift,vec2(.002),vec2(.998));
      vec4 col=texture2D(photo,p);col.r=texture2D(photo,clamp(p+shift*.28,vec2(.002),vec2(.998))).r;col.b=texture2D(photo,clamp(p-shift*.28,vec2(.002),vec2(.998))).b;gl_FragColor=col;
      #include <colorspace_fragment>
      }`});
    const scene=new THREE.Scene();scene.add(new THREE.Mesh(geometry,material));
    const camera=new THREE.Camera();
    const resize=()=>{
      if(disposed)return;
      const w=picture.clientWidth,h=picture.clientHeight;
      if(!w||!h)return;
      renderer.setSize(w,h,false);
      const aspect=texture.image.width/texture.image.height,view=w/h;
      material.uniforms.ratio.value.set(Math.min(1,view/aspect),Math.min(1,aspect/view));
    };
    canvas.className='photo-ripple';canvas.setAttribute('aria-hidden','true');picture.append(canvas);
    move(event);resize();
    resizeObserver=new ResizeObserver(resize);resizeObserver.observe(picture);
    section.addEventListener('pointermove',move,{passive:true});section.addEventListener('pointerleave',disposePhoto);
    document.addEventListener('visibilitychange',hidden);
    observer=new IntersectionObserver(([e])=>{if(!e.isIntersecting)disposePhoto();});observer.observe(section);
    const start=performance.now();
    const render=now=>{
      if(disposed)return;
      material.uniforms.time.value=(now-start)/1000;
      material.uniforms.amount.value=Math.min(.006,(now-start)/100000);
      renderer.render(scene,camera);frame=requestAnimationFrame(render);
    };
    frame=requestAnimationFrame(render);
  }catch{stop();}
}
