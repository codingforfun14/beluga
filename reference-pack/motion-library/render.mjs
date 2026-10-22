import { chromium } from 'playwright';
import { spawn } from 'child_process';
const [,, html, out, fpsArg] = process.argv; const fps = +fpsArg || 30;
const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
await pg.goto('file://' + html); await pg.evaluate(() => document.fonts.ready);
await pg.evaluate(async () => { for (const f of ['Anton','InterX','Grotesk','Archivo','Marker','Serif','Unbounded']) await document.fonts.load(`800 40px ${f}`).catch(()=>{}); await document.fonts.load('200 40px InterX'); await document.fonts.load('500 40px InterX'); });
const total = await pg.evaluate(() => window.TOTAL); const n = Math.round(total * fps);
const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-r',String(fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out]);
for (let i = 0; i < n; i++) { const d = await pg.evaluate(t => { drawFrame(t); return document.getElementById('c').toDataURL('image/jpeg', .92); }, i / fps); ff.stdin.write(Buffer.from(d.split(',')[1], 'base64')); }
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('frames', n);
