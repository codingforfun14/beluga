// Render di una libreria di clip (HTML con window.drawFrame(t)) in mp4.
// Uso: node render.mjs <file.html> <out.mp4> [fps] [config.json] [--scene N]
// - La pagina dichiara window.W, window.H (default 1280x720), window.TOTAL, window.D, window.N.
// - config.json (opzionale) viene iniettato come window.CONFIG prima del caricamento:
//   testi, colori, font e durata si cambiano senza toccare il codice della clip.
// - --scene N renderizza solo la scena N (1 = prima).
import { createRequire } from 'module';
import { spawn } from 'child_process';
import { readFileSync } from 'fs';
import { resolve } from 'path';
// playwright installato nel progetto o globalmente (NODE_PATH)
const { chromium } = await import('playwright').catch(() => createRequire(import.meta.url)('playwright'));
const args = process.argv.slice(2);
const si = args.indexOf('--scene'); const scene = si >= 0 ? +args.splice(si, 2)[1] : 0;
const [html, out, fpsArg, cfgPath] = args; const fps = +fpsArg || 30;
const cfg = cfgPath ? readFileSync(cfgPath, 'utf8') : 'null';
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1920, height: 1920 } });
await pg.addInitScript(c => { window.CONFIG = JSON.parse(c); }, cfg);
await pg.goto('file://' + resolve(html)); await pg.evaluate(() => document.fonts.ready);
await pg.evaluate(async () => { for (const f of document.fonts) { try { await f.load(); } catch {} } });
const { total, D, W, H } = await pg.evaluate(() => ({ total: window.TOTAL, D: window.D, W: window.W || 1280, H: window.H || 720 }));
const t0 = scene ? (scene - 1) * D : 0, dur = scene ? D : total, n = Math.round(dur * fps);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-r', String(fps), '-i', '-', '-vf', `scale=${W}:${H}`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out]);
for (let i = 0; i < n; i++) {
  const d = await pg.evaluate(t => { drawFrame(t); return document.getElementById('c').toDataURL('image/jpeg', .92); }, t0 + i / fps);
  if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('frames', n, `${W}x${H}`);
