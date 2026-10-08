// intro.html을 프레임 단위로 캡처해 ffmpeg로 MP4를 만든다.
// 사용법: node render.mjs [초=12] [fps=30]
import { createRequire } from 'module';
import { spawn } from 'child_process';
import { mkdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const DUR = Number(process.argv[2] || 12), FPS = Number(process.argv[3] || 30);
mkdirSync(path.join(dir, 'out'), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + path.join(dir, 'intro.html'));
await page.evaluate(() => document.fonts.ready);

const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', path.join(dir, 'out/video.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });

const total = Math.round(DUR * FPS);
for (let f = 0; f < total; f++) {
  await page.evaluate((t) => window.render(t), f / FPS);
  const buf = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  if (f % 30 === 0) process.stdout.write(`frame ${f}/${total}\n`);
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
