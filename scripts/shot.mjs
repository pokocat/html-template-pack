#!/usr/bin/env node
/**
 * shot.mjs — 给模板截 1920×1080 的图，供图库展示。
 *
 * 用法：
 *   node scripts/shot.mjs <slug> [页码...] [--out 目录]
 *
 * 不传页码时默认截三张：第 1 页、中间页、最后一页。
 * 输出到 screenshots/<slug>-<页码>.png（--out 可覆盖目录）。
 *
 * 原理：生成一个临时 wrapper 页面，用 iframe 载入 template.html，
 * 向 iframe 派发 (n-1) 次 ArrowRight 键盘事件翻到第 n 页，
 * 再用 headless Chrome 截图。vanilla JS 翻页和 deck-stage.js
 * 两种导航机制都监听键盘事件，所以都适用。
 */
import { mkdirSync, writeFileSync, rmSync, existsSync, readFileSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const args = process.argv.slice(2);
const outIdx = args.indexOf("--out");
let outDir = join(ROOT, "screenshots");
if (outIdx !== -1) {
  outDir = resolve(args[outIdx + 1]);
  args.splice(outIdx, 2);
}

const slug = args[0];
if (!slug) {
  console.error("用法：node scripts/shot.mjs <slug> [页码...] [--out 目录]");
  process.exit(1);
}

const tplDir = join(ROOT, "templates", slug);
const tplHtml = join(tplDir, "template.html");
if (!existsSync(tplHtml)) {
  console.error(`找不到模板：templates/${slug}/template.html`);
  process.exit(1);
}

// 数幻灯片页数：优先 .slide，其次 deck-stage 的直接子元素
const html = readFileSync(tplHtml, "utf8");
let count = (html.match(/class="[^"]*\bslide\b[^"]*"/g) || []).length;
if (!count) {
  const m = html.match(/<deck-stage[\s\S]*?<\/deck-stage>/);
  if (m) count = (m[0].match(/<(section|div|article)\b/g) || []).length;
}
if (!count) count = 12;

let slides = args.slice(1).map(Number).filter(n => n >= 1);
if (!slides.length) {
  slides = [1, Math.ceil(count / 2), count];
}
slides = [...new Set(slides)].filter(n => n <= count);

mkdirSync(outDir, { recursive: true });

const tmpDir = join(ROOT, ".shot-tmp");
mkdirSync(tmpDir, { recursive: true });

function wrapperFor(n) {
  const rel = join("..", "templates", slug, "template.html");
  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  html,body{margin:0;padding:0;width:1920px;height:1080px;overflow:hidden}
  iframe{width:1920px;height:1080px;border:0;display:block}
</style></head>
<body>
<iframe id="f" src="${rel}"></iframe>
<script>
  const N = ${n};
  const f = document.getElementById('f');
  f.addEventListener('load', () => {
    const w = f.contentWindow;
    for (let k = 1; k < N; k++) {
      w.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true, cancelable: true }));
    }
  });
</script>
</body></html>`;
}

let failed = 0;
for (const n of slides) {
  const wrapper = join(tmpDir, `wrap-${slug}-${n}.html`);
  writeFileSync(wrapper, wrapperFor(n), "utf8");
  const out = join(outDir, `${slug}-${n}.png`);
  const r = spawnSync(CHROME, [
    "--headless=new",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--hide-scrollbars",
    "--force-device-scale-factor=1",
    "--window-size=1920,1080",
    "--virtual-time-budget=5000",
    `--screenshot=${out}`,
    "file://" + wrapper
  ], { stdio: "ignore" });
  if (r.status !== 0 || !existsSync(out)) {
    console.error(`第 ${n} 页截图失败`);
    failed++;
  } else {
    console.log(`✓ screenshots/${slug}-${n}.png`);
  }
}

rmSync(tmpDir, { recursive: true, force: true });
process.exit(failed ? 1 : 0);
