import sys, math
out=sys.argv[1]
SKY,TEAL,DEEP,CREAM,GREEN="#6CB4D8","#23566B","#163E4E","#F4ECD6","#3DAA7C"
cx,cy,R=540,800,300
wires=''.join(f'<ellipse class="wire" pathLength="1" cx="{cx}" cy="{cy}" rx="{rx}" ry="{R}" />' for rx in (300,210,110,30))
wires+=''.join(f'<ellipse class="wire" pathLength="1" cx="{cx}" cy="{cy+dy}" rx="{int(math.sqrt(R*R-dy*dy))}" ry="{int(math.sqrt(R*R-dy*dy)*.18)}" />' for dy in (-200,-90,30,150,240))
waves=''.join(f'<path d="M{cx-R} {cy+40+i*44} q37 -14 75 0 t75 0 t75 0 t75 0 t75 0 t75 0 t75 0 t75 0" stroke="{SKY}" stroke-width="3" fill="none" opacity=".45"/>' for i in range(6))
weeds=''.join(f'<path d="M{x} {cy+R-30} q-14 -{h/2} 0 -{h} q14 -{h/3} 0 -{h*1.3}" stroke="{GREEN}" stroke-width="10" stroke-linecap="round" fill="none"/>' for x,h in ((420,60),(452,90),(640,70),(690,110)))
def drops(prefix, n):
    return ''.join(f'<circle id="{prefix}{i}" cx="0" cy="0" r="{8+(i*7)%12}" fill="{CREAM}"/>' for i in range(n))
ext=','.join(f'{i}px {i}px 0 {TEAL}' for i in range(1,23))
letters=''.join(f'<span class="ltr">{c}</span>' for c in "BELUGA")
words="dell'oceano è|ancora inesplorato."
lines=''.join('<div class="ln">'+''.join(f'<span class="w">{w}</span>' for w in l.split())+'</div>' for l in words.split('|'))
html=f'''<!doctype html><html lang="it"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/js/gsap.min.js"></script>
<style>
:root{{--sky:{SKY};--teal:{TEAL};--deep:{DEEP};--cream:{CREAM};--green:{GREEN}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--sky)}}
#root{{width:1080px;height:1920px;position:relative;font-family:Inter,sans-serif}}
.full{{position:absolute;inset:0}}
#s1 .bg{{background:var(--sky)}}
svg.lay{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible}}
.wire{{fill:none;stroke:var(--cream);stroke-width:3;stroke-dasharray:1;stroke-dashoffset:.5}}
#whale{{position:absolute;left:340px;top:850px;width:400px;height:200px}}
#word{{position:absolute;left:0;top:700px;width:1080px;text-align:center;font-family:"Archivo Black",sans-serif;font-size:172px;line-height:1;color:var(--cream);text-shadow:{ext}}}
#word .ltr{{display:inline-block;transform-origin:50% 80%}}
#blobsvg{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s4 .bg{{background:var(--teal)}}
#logo{{position:absolute;left:0;width:1080px;top:250px;text-align:center;font-family:"Archivo Black",sans-serif;font-size:44px;letter-spacing:.3em;color:var(--cream);opacity:0}}
#dialwrap{{position:absolute;left:290px;top:420px;width:500px;height:500px}}
#dshadow{{position:absolute;left:-70px;top:26px;width:500px;height:500px;border-radius:50%;background:var(--deep)}}
#dial{{position:absolute;inset:0;border-radius:50%;background:var(--teal);box-shadow:0 0 0 4px var(--sky) inset;overflow:hidden}}
#pie{{position:absolute;inset:0;border-radius:50%;--p:0;background:conic-gradient(var(--sky) calc(var(--p) * 1%), transparent 0)}}
#dial svg{{position:absolute;inset:0}}
#num{{position:absolute;left:0;width:500px;top:170px;text-align:center;font-family:Oswald,sans-serif;font-weight:400;font-size:150px;line-height:1;color:var(--deep)}}
#txt{{position:absolute;left:0;width:1080px;top:1030px;text-align:center;color:var(--cream);font-size:64px;font-weight:600;letter-spacing:-.02em;line-height:1.15}}
#txt .w{{display:inline-block;margin:0 9px;opacity:0}}
#src{{position:absolute;left:0;width:1080px;top:1230px;text-align:center;color:var(--sky);font-size:30px;font-family:"Space Mono",monospace;opacity:0}}
#grain{{position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;opacity:.10;mix-blend-mode:multiply}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="7" data-width="1080" data-height="1920">
 <div id="s1" class="clip full" data-start="0" data-duration="4.4" data-track-index="0" data-track-kind="graphics" data-layout-allow-overflow data-layout-allow-overlap>
  <div class="bg full"></div>
  <div id="win" class="full">
   <svg class="lay" id="back" viewBox="0 0 1080 1920"><circle id="ring" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{CREAM}" stroke-width="3" opacity="1"/></svg>
   <div id="whale"><svg width="400" height="200" viewBox="0 0 400 200">
    <path d="M380,110 C382,66 344,44 292,47 C250,50 220,62 180,70 C130,80 82,95 52,100 L14,68 C6,95 6,126 14,152 L52,120 C92,136 150,160 222,161 C302,163 378,152 380,110 Z" fill="{CREAM}"/>
    <path d="M222,161 C300,163 370,150 378,118 C340,140 280,150 222,150 C170,150 110,138 60,122 C100,140 160,160 222,161Z" fill="#D9CFB3"/>
    <path d="M250,148 C262,176 242,192 224,186 C228,170 233,160 242,151 Z" fill="{TEAL}"/>
    <circle cx="332" cy="96" r="6" fill="{TEAL}"/><path d="M350 118 q12 6 24 0" stroke="{TEAL}" stroke-width="3" fill="none" stroke-linecap="round"/>
   </svg></div>
   <svg class="lay" id="water" viewBox="0 0 1080 1920"><defs><clipPath id="half"><path d="M{cx-R},{cy} A{R},{R} 0 0,0 {cx+R},{cy} Z"/></clipPath></defs>
    <g id="sea" clip-path="url(#half)"><rect x="{cx-R}" y="{cy}" width="{2*R}" height="{R}" fill="{TEAL}"/>{waves}{weeds}</g>
    <path id="surf" d="M{cx-R} {cy} H{cx+R}" stroke="{CREAM}" stroke-width="4"/></svg>
   <svg class="lay" id="front" viewBox="0 0 1080 1920">{wires}<g id="dA">{drops("a",12)}</g><g id="dB">{drops("b",12)}</g></svg>
  </div>
  <div id="word">{letters}</div>
 </div>
 <div id="s4" class="clip full" data-start="3.75" data-duration="3.25" data-track-index="1" data-track-kind="graphics" data-layout-allow-overflow data-layout-allow-overlap>
  <svg id="blobsvg" viewBox="0 0 1080 1920"><defs><filter id="wob" x="-50%" y="-50%" width="200%" height="200%"><feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="2" seed="3"/><feDisplacementMap id="disp" in="SourceGraphic" scale="140"/></filter></defs>
   <circle id="blob" cx="540" cy="820" r="160" fill="{TEAL}" filter="url(#wob)"/></svg>
  <div id="logo">BELUGA</div>
  <div id="dialwrap"><div id="dshadow"></div><div id="dial"><div id="pie"></div>
   <svg viewBox="0 0 500 500">{''.join(f'<path d="M-20 {40+i*42} q31 -14 62 0 t62 0 t62 0 t62 0 t62 0 t62 0 t62 0 t62 0 t62 0" stroke="{CREAM}" stroke-width="2.5" fill="none" opacity=".35"/>' for i in range(11))}</svg>
   <div id="num">0%</div></div></div>
  <div id="txt">{lines}</div>
  <div id="src">FONTE: NOAA</div>
 </div>
 <div id="fx" class="clip full" data-start="0" data-duration="7" data-track-index="2" data-track-kind="graphics" data-layout-allow-overflow>
  <svg id="grain" viewBox="0 0 1200 2040"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="11"/><feColorMatrix values="0 0 0 0 .3  0 0 0 0 .3  0 0 0 0 .3  0 0 0 1.4 -.2"/></filter><rect width="1200" height="2040" filter="url(#n)"/></svg>
 </div>
 <audio id="a1" class="clip" src="assets/sfx/pop.mp3" data-start="0" data-track-index="10" data-volume="0.5"></audio>
 <audio id="a2" class="clip" src="assets/sfx/pop.mp3" data-start="0.9" data-track-index="11" data-volume="0.8"></audio>
 <audio id="a3" class="clip" src="assets/sfx/whoosh.mp3" data-start="1.15" data-track-index="12" data-volume="0.9"></audio>
 <audio id="a4" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="2.25" data-track-index="13" data-volume="0.9"></audio>
 <audio id="a5" class="clip" src="assets/sfx/impact-bass-2.mp3" data-start="2.45" data-track-index="14" data-volume="0.9"></audio>
 <audio id="a6" class="clip" src="assets/sfx/pop.mp3" data-start="2.85" data-track-index="15" data-volume="0.6"></audio>
 <audio id="a7" class="clip" src="assets/sfx/whoosh.mp3" data-start="3.7" data-track-index="16" data-volume="1"></audio>
 <audio id="a8" class="clip" src="assets/sfx/ping.mp3" data-start="5.85" data-track-index="17" data-volume="0.6"></audio>
</div>
<script>
const tl=gsap.timeline({{paused:true}});
// draw-on wire sphere (frame 0 already has strokes started)
tl.fromTo(".wire",{{strokeDashoffset:0.5}},{{strokeDashoffset:0,duration:.8,stagger:.05,ease:"power2.out"}},0);
tl.fromTo("#front",{{rotation:0}},{{rotation:12,transformOrigin:"540px 800px",duration:1.1,ease:"none"}},0);
tl.to(".wire",{{opacity:0,duration:.25,stagger:.02}},0.85);

tl.fromTo("#water",{{scale:0}},{{scale:1,transformOrigin:"540px 800px",duration:.55,ease:"back.out(1.6)"}},0.9);

// whale leap
gsap.set("#whale",{{x:-40,y:120,rotation:-62,opacity:0}});
tl.set("#whale",{{opacity:1}},1.1);
tl.to("#whale",{{x:200,duration:1.3,ease:"sine.inOut"}},1.15);
tl.to("#whale",{{y:-470,duration:.62,ease:"power2.out"}},1.15);
tl.to("#whale",{{y:160,duration:.62,ease:"power2.in"}},1.77);
tl.to("#whale",{{rotation:68,duration:1.24,ease:"sine.inOut"}},1.15);
tl.fromTo("#whale",{{filter:"blur(0px)"}},{{filter:"blur(7px)",duration:.08}},1.15);
tl.to("#whale",{{filter:"blur(0px)",duration:.4,ease:"power2.out"}},1.25);
tl.to("#whale",{{filter:"blur(8px)",duration:.3,ease:"power2.in"}},2.05);
function burst(p,t,x0,dir){{for(let i=0;i<12;i++){{const a=(-90+(i-5.5)*13)*Math.PI/180, sp=110+(i*37)%120;
 const el="#"+p+i; gsap.set(el,{{x:x0,y:800,scale:0}}); tl.to(el,{{scale:1,duration:.08}},t);
 tl.to(el,{{x:x0+Math.cos(a)*sp*1.6+dir*40,duration:.8,ease:"none"}},t);
 tl.to(el,{{y:800+Math.sin(a)*sp*1.8,duration:.35,ease:"power2.out"}},t);
 tl.to(el,{{y:860,scale:0,duration:.45,ease:"power2.in"}},t+.35);}}}}
burst("a",1.2,560,-1); burst("b",2.3,740,1);

// circle shrinks, word pops
tl.to("#win",{{scale:0,transformOrigin:"540px 800px",duration:.35,ease:"power3.in"}},2.45);
tl.fromTo("#word .ltr",{{scale:0,rotation:-25,y:90}},{{scale:1,rotation:0,y:0,duration:.6,stagger:.05,ease:"back.out(1.8)"}},2.8);
tl.to("#word",{{y:-20,duration:.9,ease:"none"}},3.0);
tl.to("#word .ltr",{{scale:0,rotation:20,duration:.25,stagger:.03,ease:"power3.in"}},3.72);
// liquid wipe
tl.fromTo("#blob",{{scale:0}},{{scale:9,svgOrigin:"540 820",duration:.65,ease:"power2.inOut"}},3.75);
tl.fromTo("#disp",{{attr:{{scale:160}}}},{{attr:{{scale:0}},duration:.8,ease:"power2.out"}},3.95);
// data scene
tl.fromTo("#dialwrap",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:.7,ease:"back.out(1.4)"}},4.25);
tl.fromTo("#logo",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.2,ease:"power4.out"}},4.4);
const c={{v:0}};
tl.to("#pie",{{"--p":80,duration:1.2,ease:"power2.inOut"}},4.65);
tl.to(c,{{v:80,duration:1.2,ease:"power2.inOut",onUpdate:()=>{{document.getElementById("num").textContent=Math.round(c.v)+"%";}}}},4.65);
tl.fromTo("#txt .w",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.15,stagger:.08,ease:"power4.out"}},4.85);
tl.fromTo("#src",{{opacity:0}},{{opacity:1,duration:.3}},5.4);
tl.fromTo("#dialwrap",{{y:0}},{{y:-12,duration:2,ease:"none"}},5.0);
for(let f=0;f<7*12;f++) tl.set("#grain",{{x:((f*37)%60)-30,y:((f*53)%60)-30}},f/12);
window.__timelines["main"]=tl;
tl.seek(0);
</script></body></html>'''
open(out,'w').write(html)
