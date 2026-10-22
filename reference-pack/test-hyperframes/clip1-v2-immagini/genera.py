# Genera index.html. Le immagini Kling vanno in assets/k/ con i nomi di PROMPT-KLING.md
import sys
G = {'B':["11110","10001","10001","11110","10001","10001","11110"],'E':["11111","10000","10000","11110","10000","10000","11111"],
 'L':["10000","10000","10000","10000","10000","10000","11111"],'U':["10001","10001","10001","10001","10001","10001","01110"],
 'G':["01110","10001","10000","10111","10001","10001","01110"],'A':["01110","10001","10001","11111","10001","10001","10001"]}
def dm(word,p,r,col,cls):
    w=len(word)*6*p-p; s=f'<svg width="{w}" height="{7*p}" viewBox="0 0 {w} {7*p}">'
    for i,ch in enumerate(word):
        s+=f'<g class="{cls}">'+''.join(f'<circle cx="{i*6*p+x*p+p/2}" cy="{y*p+p/2}" r="{r}" fill="{col}"/>' for y,row in enumerate(G[ch]) for x,c in enumerate(row) if c=='1')+'</g>'
    return s+'</svg>'
labels=['01 VETRO','02 BOBINA','03 SCHEDA','04 BATTERIA']
html=f'''<!doctype html><html lang="it"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/js/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#050506}}
#root{{width:1080px;height:1920px;position:relative;font-family:"Space Mono",monospace;color:#fff}}
.full{{position:absolute;inset:0}}
.img{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}}
#xr{{clip-path:inset(0 0 100% 0)}}
#scan{{position:absolute;left:0;top:0;width:1080px;height:140px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.25) 70%,#fff);mix-blend-mode:screen}}
#ex .bg{{background:radial-gradient(ellipse at 50% 45%,#18181b,#050506 70%)}}
.st{{position:absolute;left:190px;width:700px;height:350px;object-fit:contain}}
.lab{{position:absolute;left:640px;font-size:28px;letter-spacing:.08em;opacity:0;white-space:nowrap}}
.lab i{{display:inline-block;width:60px;height:2px;background:#fff;vertical-align:middle;margin-right:14px}}
#flash .fill{{background:#fff;opacity:0}}
#title{{position:absolute;left:137px;top:1080px}}
#tag{{position:absolute;left:0;width:1080px;top:1250px;text-align:center;font-family:Inter,sans-serif;font-size:46px;font-weight:500;color:#111}}
#tag span{{display:inline-block;opacity:0;margin:0 7px}}
#sweep{{position:absolute;left:-400px;top:0;width:300px;height:1920px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.35),rgba(255,255,255,0));mix-blend-mode:screen}}
#grain{{position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;opacity:.12;mix-blend-mode:overlay}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="7" data-width="1080" data-height="1920">
 <div id="s1" class="clip full" data-start="0" data-duration="1.75" data-track-index="0" data-track-kind="graphics" data-layout-allow-overlap>
  <div id="cam1" class="full"><img id="ph" class="img" src="assets/k/ang1.png" data-var-src="ang1"/><img id="xr" class="img" src="assets/k/xray.png" data-var-src="xray"/></div>
  <div id="scan"></div>
 </div>
 <div id="s2" class="clip full" data-start="1.75" data-duration="0.5" data-track-index="1" data-track-kind="graphics" data-layout-allow-overlap data-layout-allow-overflow>
  <img id="a2" class="img" src="assets/k/ang2.png" data-var-src="ang2"/><img id="a3" class="img" src="assets/k/ang3.png" data-var-src="ang3"/>
 </div>
 <div id="ex" class="clip full" data-start="2.25" data-duration="1.55" data-track-index="2" data-track-kind="graphics" data-layout-allow-overlap data-layout-allow-overflow>
  <div class="bg full"></div>
  <div id="stack" class="full">{''.join(f'<img id="st{i}" class="st" src="assets/k/strato{i+1}.png" data-var-src="strato{i+1}"/>' for i in range(4))}</div>
  {''.join(f'<div class="lab" id="lab{i}"><i></i>{t}</div>' for i,t in enumerate(labels))}
 </div>
 <div id="s4" class="clip full" data-start="3.8" data-duration="3.2" data-track-index="3" data-track-kind="graphics" data-layout-allow-overlap data-layout-allow-overflow>
  <div id="cam4" class="full"><img id="fo" class="img" src="assets/k/foto.png" data-var-src="foto"/></div>
  <div id="sweep"></div>
  <div id="title">{dm("BELUGA",23,7.2,"#111","tl")}</div>
  <div id="tag"><span>Vedi</span><span>attraverso.</span></div>
 </div>
 <div id="flash" class="clip full" data-start="3.7" data-duration="0.5" data-track-index="4" data-track-kind="graphics"><div class="fill full"></div></div>
 <div id="fx" class="clip full" data-start="0" data-duration="7" data-track-index="5" data-track-kind="graphics" data-layout-allow-overflow>
  <svg id="grain" viewBox="0 0 1200 2040"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1.6 -.3"/></filter><rect width="1200" height="2040" filter="url(#n)"/></svg>
 </div>
 <audio id="a_g" class="clip" src="assets/sfx/glitch-1.mp3" data-start="0" data-track-index="10" data-volume="0.5"></audio>
 <audio id="a_w1" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="1.7" data-track-index="11" data-volume="0.9"></audio>
 <audio id="a_w2" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="1.97" data-track-index="12" data-volume="0.9"></audio>
 <audio id="a_w3" class="clip" src="assets/sfx/whoosh.mp3" data-start="2.2" data-track-index="13" data-volume="1"></audio>
 <audio id="a_p" class="clip" src="assets/sfx/ping.mp3" data-start="2.7" data-track-index="14" data-volume="0.35"></audio>
 <audio id="a_i" class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="3.72" data-track-index="15" data-volume="1"></audio>
 <audio id="a_k" class="clip" src="assets/sfx/key-press.mp3" data-start="4.5" data-track-index="16" data-volume="0.5"></audio>
</div>
<script>
const tl=gsap.timeline({{paused:true}});
// S1: foto -> raggi X con la linea di scansione
tl.fromTo("#cam1",{{scale:1.0}},{{scale:1.08,duration:1.75,ease:"none"}},0);
tl.fromTo("#xr",{{clipPath:"inset(0% 0% 100% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:1.3,ease:"power1.inOut"}},0.05);
tl.fromTo("#scan",{{y:-140}},{{y:1920,duration:1.3,ease:"power1.inOut"}},0.05);
[0.8,0.85,0.9,0.95].forEach((t,i)=>tl.set("#cam1",{{x:[16,-24,10,0][i]}},t));
// finta rotazione: whip tra 3 angoli, taglio sul picco di blur
tl.to("#cam1",{{x:-500,filter:"blur(18px)",duration:.12,ease:"power3.in"}},1.63);
tl.fromTo("#a2",{{x:500,filter:"blur(18px)"}},{{x:0,filter:"blur(0px)",duration:.14,ease:"power3.out"}},1.75);
tl.to("#a2",{{x:-500,filter:"blur(18px)",duration:.1,ease:"power3.in"}},1.9);
tl.fromTo("#a3",{{opacity:0}},{{opacity:0}},1.75);
tl.fromTo("#a3",{{opacity:1,x:500,filter:"blur(18px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.14,ease:"power3.out"}},2.0);
tl.to("#a3",{{scale:1.6,filter:"blur(14px)",opacity:0,duration:.12,ease:"power3.in"}},2.13);
// esploso: strati ritagliati in 2.5D
const ys=[1250,1010,770,530];
[0,1,2,3].forEach(i=>{{gsap.set("#st"+i,{{top:780}});
 tl.fromTo("#st"+i,{{y:0,scale:.9,filter:"blur(10px)"}},{{y:ys[i]-780,scale:1,filter:"blur(0px)",duration:.8,ease:"expo.out"}},2.25+i*.05);
 gsap.set("#lab"+i,{{top:ys[i]+150}});
 tl.fromTo("#lab"+i,{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.25,ease:"power4.out"}},2.6+i*.07);}});
tl.fromTo("#stack",{{rotation:-4}},{{rotation:2,duration:1.5,ease:"none"}},2.25);
tl.to(".lab",{{opacity:0,duration:.1}},3.45);
[0,1,2,3].forEach(i=>tl.to("#st"+i,{{y:0,duration:.3,ease:"power3.in"}},3.42));
tl.fromTo("#flash .fill",{{opacity:0}},{{opacity:1,duration:.08,ease:"none"}},3.7);
tl.to("#flash .fill",{{opacity:0,duration:.4,ease:"power2.out"}},3.8);
// packshot
tl.fromTo("#cam4",{{scale:1.3,filter:"blur(16px)"}},{{scale:1.04,filter:"blur(0px)",duration:.9,ease:"expo.out"}},3.8);
tl.to("#cam4",{{scale:1,duration:2.3,ease:"none"}},4.7);
tl.fromTo("#sweep",{{x:0}},{{x:1700,duration:1.3,ease:"power2.inOut"}},4.1);
tl.fromTo(".tl",{{opacity:0}},{{opacity:1,duration:.04,stagger:.06,ease:"none"}},4.5);
tl.fromTo("#tag span",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.15,stagger:.08,ease:"power4.out"}},4.9);
for(let f=0;f<84;f++) tl.set("#grain",{{x:((f*37)%60)-30,y:((f*53)%60)-30}},f/12);
window.__timelines["main"]=tl;
tl.seek(0);
</script></body></html>'''
open(sys.argv[1] if len(sys.argv)>1 else 'index.html','w').write(html)
