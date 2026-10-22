import sys
out = sys.argv[1]
# 5x7 dot-matrix glyphs
G = {
 'B':["11110","10001","10001","11110","10001","10001","11110"],
 'E':["11111","10000","10000","11110","10000","10000","11111"],
 'L':["10000","10000","10000","10000","10000","10000","11111"],
 'U':["10001","10001","10001","10001","10001","10001","01110"],
 'G':["01110","10001","10000","10111","10001","10001","01110"],
 'A':["01110","10001","10001","11111","10001","10001","10001"],
}
def dm(word, pitch, r, color, cls, idp):
    w = len(word)*6*pitch - pitch; h = 7*pitch
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    for i,ch in enumerate(word):
        s += f'<g id="{idp}{i}" class="{cls}">'
        for y,row in enumerate(G[ch]):
            for x,c in enumerate(row):
                if c=='1': s += f'<circle cx="{i*6*pitch+x*pitch+pitch/2}" cy="{y*pitch+pitch/2}" r="{r}" fill="{color}"/>'
        s += '</g>'
    return s+'</svg>'

W,H = 520,1060
def svg(inner): return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" stroke="#fff" stroke-linecap="round">{inner}</svg>'
body = '<rect x="6" y="6" width="508" height="1048" rx="72" stroke-width="3"/>'
cam  = '<rect x="40" y="40" width="200" height="250" rx="54" stroke-width="2.5"/><circle cx="140" cy="110" r="50" stroke-width="2.5"/><circle cx="140" cy="110" r="28" stroke-width="1.5" opacity=".7"/><circle cx="140" cy="222" r="38" stroke-width="2.5"/><circle cx="140" cy="222" r="18" stroke-width="1.5" opacity=".7"/>'
L0 = svg(body + cam + '<rect x="20" y="20" width="480" height="1020" rx="60" stroke-width="1" opacity=".35"/>' + ''.join(f'<line x1="{300+i*18}" y1="90" x2="{300+i*18}" y2="150" stroke-width="5" opacity=".8"/>' for i in range(8)))
L1 = svg(''.join(f'<circle cx="260" cy="560" r="{40+i*16}" stroke-width="1.5" opacity="{.9-i*.08}"/>' for i in range(9)) + '<path d="M260 420 V330 H420 V180" stroke-width="10" opacity=".5"/><path d="M260 700 V860 H120" stroke-width="10" opacity=".5"/>')
L2 = svg('<path d="M40 60 H480 V400 H330 V460 H40 Z" stroke-width="2.5"/><rect x="290" y="150" width="120" height="120" rx="8" stroke-width="3"/><rect x="310" y="170" width="80" height="80" stroke-width="1" opacity=".6"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="9" stroke-width="2"/>' for x,y in [(60,80),(460,80),(460,380),(60,440),(300,420)]) + ''.join(f'<rect x="{80+i*36}" y="320" width="24" height="40" stroke-width="1.2" opacity=".7"/>' for i in range(5)) + '<path d="M40 900 H480 V1000 H40 Z" stroke-width="2"/><circle cx="260" cy="950" r="22" stroke-width="2"/>')
L3 = svg('<rect x="70" y="480" width="380" height="390" rx="26" stroke-width="3"/>' + ''.join(f'<line x1="90" y1="{520+i*40}" x2="430" y2="{520+i*40}" stroke-width="1" opacity=".35"/>' for i in range(9)) + '<rect x="200" y="460" width="120" height="24" rx="6" stroke-width="2"/>')
L4 = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect x="6" y="6" width="508" height="1048" rx="72" fill="rgba(255,255,255,.04)" stroke="#fff" stroke-width="2" opacity=".9"/><circle cx="260" cy="60" r="14" fill="none" stroke="#fff" stroke-width="2"/></svg>'
layers = [L0,L1,L2,L3,L4]
labels = ['01 VETRO','02 BOBINA','03 SCHEDA','04 BATTERIA','05 SCHERMO']

html = f'''<!doctype html>
<html lang="it"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/js/gsap.min.js"></script>
<style>
:root{{--ground:#050506;--ink:#ffffff;--paper:#e9e9e7;--dark:#0e0e10;--accent:#ff2a1f}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--ground)}}
#root{{width:1080px;height:1920px;position:relative;font-family:"Space Mono",monospace;color:var(--ink)}}
.full{{position:absolute;inset:0}}
#s1 .bg{{background:radial-gradient(ellipse at 50% 45%,#1a1a1d 0%,#050506 70%)}}
#stage{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#rig{{position:absolute;left:280px;top:400px;width:520px;height:1060px;transform-style:preserve-3d}}
.layer{{position:absolute;left:0;top:0;width:520px;height:1060px;filter:drop-shadow(0 0 6px rgba(255,255,255,.75)) drop-shadow(0 0 22px rgba(160,200,255,.35))}}
#scan{{position:absolute;left:0;top:0;width:1080px;height:160px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.22) 70%,rgba(255,255,255,.9) 100%);mix-blend-mode:screen}}
#vword{{position:absolute;left:96px;top:600px;transform-origin:0 0}}
.lab{{position:absolute;left:760px;font-size:28px;letter-spacing:.08em;color:#fff;opacity:0;white-space:nowrap}}
.lab i{{display:inline-block;width:60px;height:2px;background:#fff;vertical-align:middle;margin-right:14px}}
#count{{position:absolute;left:80px;top:220px;font-size:28px;letter-spacing:.12em;opacity:0}}
#flash .fill{{background:#fff;opacity:0}}
#s3 .bg{{background:radial-gradient(ellipse at 50% 35%,#f6f6f4 0%,#dcdcd9 80%)}}
#pack{{position:absolute;left:397px;top:300px;width:286px;height:583px}}
#pbody{{position:absolute;inset:0;border-radius:40px;background:linear-gradient(145deg,#2a2a2e,#0b0b0d 55%,#1b1b1e);box-shadow:0 60px 90px rgba(0,0,0,.35),0 0 0 2px #3a3a3f inset;overflow:hidden}}
#pcam{{position:absolute;left:22px;top:22px;width:110px;height:138px;border-radius:30px;background:#151518;box-shadow:0 0 0 2px #444 inset}}
#pcam b{{position:absolute;left:27px;width:56px;height:56px;border-radius:50%;background:radial-gradient(circle at 40% 40%,#3b4a5a,#06080a 60%);box-shadow:0 0 0 3px #555}}
#pled{{position:absolute;left:180px;top:60px;width:70px;height:6px;border-radius:3px;background:var(--accent)}}
#spec{{position:absolute;top:-200px;left:-300px;width:160px;height:1000px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.35),rgba(255,255,255,0));transform-origin:50% 50%}}
#title{{position:absolute;left:137px;top:1010px}}
#tag{{position:absolute;left:0;width:1080px;top:1190px;text-align:center;font-family:Inter,sans-serif;font-size:46px;font-weight:500;color:#111;letter-spacing:-.01em}}
#tag span{{display:inline-block;opacity:0;margin:0 7px}}
#grain{{position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;opacity:.13;mix-blend-mode:overlay;pointer-events:none}}
#vig{{background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%);pointer-events:none}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="7" data-width="1080" data-height="1920">
 <div id="s1" class="clip full" data-start="0" data-duration="3.8" data-track-index="0" data-track-kind="graphics" data-layout-allow-overflow data-layout-allow-overlap>
  <div class="bg full"></div>
  <div id="stage"><div id="rig">{''.join(f'<div class="layer" id="ly{i}">{l}</div>' for i,l in enumerate(layers))}</div></div>
  <div id="scan"></div>
  <div id="vword">{dm("BELUGA",14,4.2,"#fff","vl","v")}</div>
  <div id="count">X-RAY / 05 STRATI</div>
  {''.join(f'<div class="lab" id="lab{i}"><i></i>{t}</div>' for i,t in enumerate(labels))}
 </div>
 <div id="s3" class="clip full" data-start="3.8" data-duration="3.2" data-track-index="1" data-track-kind="graphics" data-layout-allow-overlap>
  <div class="bg full"></div>
  <div id="pack"><div id="pbody"><div id="pcam"><b style="top:14px"></b><b style="top:74px"></b></div><div id="pled"></div><div id="spec" data-layout-allow-overflow></div></div></div>
  <div id="title">{dm("BELUGA",23,7.2,"#111","tl","t")}</div>
  <div id="tag"><span>Vedi</span><span>attraverso.</span></div>
 </div>
 <div id="flash" class="clip full" data-start="3.7" data-duration="0.5" data-track-index="2" data-track-kind="graphics"><div class="fill full"></div></div>
 <div id="fx" class="clip full" data-start="0" data-duration="7" data-track-index="3" data-track-kind="graphics" data-layout-allow-overflow>
  <svg id="grain" viewBox="0 0 1200 2040"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1.6 -.3"/></filter><rect width="1200" height="2040" filter="url(#n)"/></svg>
  <div id="vig" class="full"></div>
 </div>
 <audio id="a_glitch" class="clip" src="assets/sfx/glitch-1.mp3" data-start="0" data-track-index="10" data-volume="0.55"></audio>
 <audio id="a_whoosh" class="clip" src="assets/sfx/whoosh.mp3" data-start="1.75" data-track-index="11" data-volume="1"></audio>
 <audio id="a_ping" class="clip" src="assets/sfx/ping.mp3" data-start="2.5" data-track-index="12" data-volume="0.35"></audio>
 <audio id="a_whoosh2" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="3.4" data-track-index="13" data-volume="0.9"></audio>
 <audio id="a_impact" class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="3.72" data-track-index="14" data-volume="1"></audio>
 <audio id="a_k1" class="clip" src="assets/sfx/key-press.mp3" data-start="4.5" data-track-index="15" data-volume="0.5"></audio>
 <audio id="a_k2" class="clip" src="assets/sfx/key-press.mp3" data-start="4.68" data-track-index="16" data-volume="0.5"></audio>
 <audio id="a_k3" class="clip" src="assets/sfx/key-press.mp3" data-start="4.86" data-track-index="17" data-volume="0.5"></audio>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
const layers = ["#ly0","#ly1","#ly2","#ly3","#ly4"];
// --- S1: X-ray, frame 0 already lit
gsap.set("#rig",{{transformPerspective:2600,transformOrigin:"50% 50%"}});
gsap.set("#vword",{{rotation:-90,y:520}});
gsap.set(".vl",{{opacity:.15}});
tl.fromTo("#stage",{{scale:1.0}},{{scale:1.07,duration:1.75,ease:"none"}},0);
tl.fromTo("#scan",{{y:300}},{{y:1500,duration:1.5,ease:"power1.inOut"}},0);
layers.forEach((l,i)=>tl.fromTo(l,{{opacity:.25}},{{opacity:1,duration:.12,ease:"none"}},0.25+i*0.22));
tl.to(".vl",{{opacity:1,duration:.05,stagger:.12,ease:"none"}},0.15);
// glitch jitter
[0.55,0.6,0.66,0.7].forEach((t,i)=>tl.set("#stage",{{x:[18,-26,10,0][i]}},t));
// --- fast tilt into exploded view with motion blur
tl.to("#rig",{{rotationX:58,rotationZ:-32,x:-110,y:40,duration:.85,ease:"expo.out"}},1.75);
layers.forEach((l,i)=>tl.to(l,{{z:(i-2)*170,duration:1.0,ease:"expo.out"}},1.8+i*0.045));
tl.fromTo("#stage",{{filter:"blur(0px)"}},{{filter:"blur(16px)",duration:.08,ease:"power2.in"}},1.75);
tl.to("#stage",{{filter:"blur(0px)",duration:.35,ease:"power3.out"}},1.83);
tl.to(["#scan",".vl"],{{opacity:0,duration:.2}},1.75);
tl.to("#rig",{{rotationZ:-38,duration:1.4,ease:"none"}},2.6);
tl.fromTo("#count",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.18,ease:"power4.out"}},2.3);
const ly = [1290,1110,930,750,570];
[0,1,2,3,4].forEach(i=>{{gsap.set("#lab"+i,{{top:ly[i]}}); tl.fromTo("#lab"+i,{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.25,ease:"power4.out"}},2.35+i*0.07);}});
// collapse and hit
tl.to(["#count",".lab"],{{opacity:0,duration:.12}},3.4);
layers.forEach((l,i)=>tl.to(l,{{z:0,duration:.32,ease:"power3.in"}},3.4));
tl.to("#rig",{{rotationX:0,rotationZ:0,x:0,y:0,scale:1.4,duration:.32,ease:"power3.in"}},3.4);
tl.to("#stage",{{filter:"blur(14px)",duration:.12,ease:"power2.in"}},3.6);
tl.fromTo("#flash .fill",{{opacity:0}},{{opacity:1,duration:.08,ease:"none"}},0.0);
tl.to("#flash .fill",{{opacity:0,duration:.4,ease:"power2.out"}},0.12);
// --- S3: packshot
tl.fromTo("#pack",{{scale:1.5,filter:"blur(20px)",rotation:-8}},{{scale:1,filter:"blur(0px)",rotation:0,duration:.9,ease:"expo.out"}},3.8);
tl.fromTo("#spec",{{x:-100,rotation:20}},{{x:700,rotation:20,duration:1.3,ease:"power2.inOut"}},4.2);
tl.to("#pack",{{y:-14,duration:3.2,ease:"none"}},4.6);
tl.fromTo(".tl",{{opacity:0}},{{opacity:1,duration:.04,stagger:.08,ease:"none"}},4.75);
tl.fromTo("#pled",{{opacity:.2}},{{opacity:1,duration:.05,repeat:5,yoyo:true,ease:"steps(1)"}},5.2);
tl.fromTo("#tag span",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.15,stagger:.08,ease:"power4.out"}},5.35);
// grain jitter (deterministic, stepped)
for(let f=0;f<7*12;f++) tl.set("#grain",{{x:((f*37)%60)-30,y:((f*53)%60)-30}},f/12);
tl.to("#vig",{{opacity:.25,duration:.3}},3.8);
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>'''
open(out,'w').write(html)
