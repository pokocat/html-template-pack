#!/usr/bin/env node
/**
 * deploy.mjs — 一键发布图库到线上。
 *
 * 重建 gallery.html，然后上传 gallery.html 和 screenshots/ 到服务器。
 * 纯静态站，传完即生效，不用 reload nginx。
 *
 * 用法：node scripts/deploy.mjs
 */
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const KEY = join(homedir(), "dev", "aliyun", "aiartist.pem");
const HOST = "ecs-user@47.98.162.120";
const REMOTE = "/opt/gallery/";

function run(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: "inherit" });
  if (r.status !== 0) {
    console.error(`${cmd} 退出码 ${r.status}`);
    process.exit(r.status ?? 1);
  }
}

run("node", [join(ROOT, "scripts", "build-gallery.mjs")]);
run("scp", ["-i", KEY, join(ROOT, "gallery.html"), `${HOST}:${REMOTE}`]);
run("scp", ["-i", KEY, "-r", join(ROOT, "screenshots"), `${HOST}:${REMOTE}`]);

console.log("发布完成 → https://gallery.aibuzz.cn");
