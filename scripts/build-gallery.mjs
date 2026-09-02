#!/usr/bin/env node
/**
 * build-gallery.mjs — 生成 gallery.html
 *
 * 从 index.json（或各 template.json）+ screenshots/ 目录读取数据，
 * 注入 gallery.template.html 的 /*__TEMPLATE_DATA__* / 占位符，写出 gallery.html。
 *
 * 用法：node scripts/build-gallery.mjs
 */
import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const REPO_URL = "https://github.com/pokocat/html-template-pack";

const index = JSON.parse(readFileSync(join(ROOT, "index.json"), "utf8"));

// 按文件名的数字后缀自然排序 1,2,3,…,18
function numericSort(a, b) {
  const na = Number((a.match(/(\d+)(?=\.png$)/) || [])[0] || 0);
  const nb = Number((b.match(/(\d+)(?=\.png$)/) || [])[0] || 0);
  return na - nb;
}

const shotsDir = join(ROOT, "screenshots");
const allShots = existsSync(shotsDir) ? readdirSync(shotsDir) : [];
const bySlug = {};
for (const f of allShots) {
  const m = f.match(/^(.+)-(\d+)\.png$/);
  if (!m) continue;
  (bySlug[m[1]] ||= []).push(f);
}
for (const k of Object.keys(bySlug)) bySlug[k].sort(numericSort);

// 截图 URL 带 ?v=修改时间，重截同名图时浏览器缓存不会挡路
const templates = index.templates.map(t => ({
  ...t,
  shots: (bySlug[t.slug] || []).map(f =>
    `${f}?v=${Math.floor(statSync(join(shotsDir, f)).mtimeMs / 1000)}`)
}));

const data = { repo: REPO_URL, templates };
const marker = "/*__TEMPLATE_DATA__*/";

const src = readFileSync(join(__dirname, "gallery.template.html"), "utf8");
if (!src.includes(marker)) {
  console.error(`模板里找不到占位符 ${marker}`);
  process.exit(1);
}
const out = src.replace(marker, JSON.stringify(data));
const dst = join(ROOT, "gallery.html");
writeFileSync(dst, out, "utf8");

const withShots = templates.filter(t => t.shots.length).length;
console.log(`已生成 gallery.html：${templates.length} 套模板（其中 ${withShots} 套有截图）。`);