#!/usr/bin/env python3
"""
measure-slide.py — 模板提取时的逐页校对工具。

从原图(小红书长图/带投影的整版图)里裁出真正的幻灯片区域并归一化到 1920×1080，
和模板的截图做 50% 叠加对照，或用量化的色块掩码测出文字/色块的位置与尺寸。

用法（在仓库根目录运行）：
  # 1. 先把原图裁成归一化幻灯片（去掉投影边）
  #    按亮度剖切出内容边界 → 保持 16:9 → resize 到 1920×1080
  python3 scripts/measure-slide.py crop <原图.png> [-o out.png]
      # 不传 -o 时在 /tmp/measure/<basename> 下生成同名文件

  # 2. 让 shot.mjs 截模板某一页，再和归一化原图 50% 叠加
  node scripts/shot.mjs <slug> <n> --out /tmp/measure/shots
  python3 scripts/measure-slide.py blend <原图.png>  <slug> <n> -o blend.png
      # blend 会自己调 shot.mjs 截图，也可先用上一步截好

  # 3. 测文字/色块：打印指定竖带区里每一"行块"的 y 范围和行内 x 范围
  python3 scripts/measure-slide.py measure <png> --x 100 900 --y 200 950 --mask blue
      # --mask 指定颜色掩码：blue 用蓝底白字的默认规则，也可手动给阈值

依赖：numpy + Pillow；截图依赖 Chrome + scripts/shot.mjs。
"""
import argparse
import os
import subprocess
import sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(ROOT, "scripts", "shot.mjs")


# ─── 幻灯片边界检测 ───────────────────────────────────────────────
# 原图四周常带投影，直接量会整体偏移。这里按亮度剖切出"内容实际所在"的矩形，
# 左侧/上界取内容起点，右侧取中行亮度骤降的黑边，再按 16:9 推断下边界。
def slide_box(gray):
    h, w = gray.shape
    colmid = gray[h // 3 : 2 * h // 3, :]
    rowmid = gray[:, w // 3 : 2 * w // 3]
    colnon = np.nonzero((colmid < 250).mean(axis=0) > 0.5)[0]
    rownon = np.nonzero((rowmid < 250).mean(axis=1) > 0.5)[0]
    if not len(colnon) or not len(rownon):
        return (0, 0, w - 1, h - 1)
    left = int(colnon.min()) + 1
    top = int(rownon.min()) + 1
    row = gray[h // 2, :]
    right = w - 1
    for x in range(w - 5, w // 2, -1):
        if row[x] < 60:
            right = x - 2
            break
    width = right - left
    height = int(round(width * 9 / 16))
    return (left, top, left + width, top + height)


def normalize(img):
    """把任意尺寸原图裁成 1920×1080 的归一化幻灯片。已归一化的图原样返回。"""
    img = img.convert("RGB")
    if img.size == (1920, 1080):
        return img
    a = np.asarray(img.convert("L")).astype(int)
    img = img.crop(slide_box(a)).resize((1920, 1080))
    return img


# ─── 颜色掩码 ─────────────────────────────────────────────────────
def mask_blue(arr, b_min=120, b_r=40, g_delta=20, r_min=0):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    return (b > b_min) & (b - r > b_r) & (g < b - g_delta) & (r > r_min)


MASKS = {
    "blue": mask_blue,
}


def bands(proj, thr):
    """把 1D 投影序列按大于阈值切成区段，返回 [(start, end), ...]。"""
    out = []
    s = None
    for i, v in enumerate(proj):
        if v > thr and s is None:
            s = i
        elif v <= thr and s is not None:
            out.append((s, i))
            s = None
    if s is not None:
        out.append((s, len(proj)))
    return out


def merge_close(runs, gap):
    merged = []
    for s, e in runs:
        if merged and s - merged[-1][1] < gap:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [(s, e) for s, e in merged]


# ─── 子命令：crop ─────────────────────────────────────────────────
def cmd_crop(args):
    img = normalize(Image.open(args.input))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        img.save(args.out)
        print(f"✓ {args.out}")
    else:
        base = os.path.join("/tmp/measure", os.path.basename(args.input))
        os.makedirs("/tmp/measure", exist_ok=True)
        img.save(base)
        print(f"✓ {base}")


# ─── 子命令：blend ────────────────────────────────────────────────
def cmd_blend(args):
    nodec = subprocess.run(
        ["node", SHOT, args.slug, str(args.n), "--out", "/tmp/measure/shots"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if nodec.returncode != 0:
        sys.exit(f"shot.mjs 失败：{nodec.stderr or nodec.stdout}")
    shot_path = f"/tmp/measure/shots/{args.slug}-{args.n}.png"
    orig = normalize(Image.open(args.input))
    shot = Image.open(shot_path).convert("RGB")
    blend = Image.blend(shot, orig, 0.5)
    blend.save(args.out)
    print(f"✓ blend: {args.out}")
    if args.print_box:
        a = np.asarray(Image.open(args.input).convert("L")).astype(int)
        print("  original slide box:", slide_box(a))


# ─── 子命令：measure ──────────────────────────────────────────────
def cmd_measure(args):
    mfun = MASKS.get(args.mask, mask_blue)
    img = normalize(Image.open(args.input))
    params = {k: getattr(args, k) for k in ("b_min", "b_r", "g_delta", "r_min")}
    m = mfun(np.asarray(img).astype(int), **params)
    x0, x1 = args.x
    y0, y1 = args.y
    sub = m[y0:y1, x0:x1]
    print(f"== {args.input} region x[{x0}:{x1}] y[{y0}:{y1}] ==")
    for s, e in bands(sub.sum(axis=1), 2):
        if e - s < 4:
            continue
        line = m[y0 + s : y0 + e, x0:x1]
        ys, xs = np.nonzero(line)
        print(f"  y[{y0+s}:{y0+e}] x[{xs.min()+x0}:{xs.max()+x0}]")
    # 若同一区域内有多列（如网格/统计栏），再按列打印
    for cs, ce in bands(sub.sum(axis=0), 3):
        if ce - cs < 30:
            continue
        col = m[y0:y1, x0 + cs : x0 + ce]
        blocks = []
        for rs, re in bands(col.sum(axis=1), 1):
            if re - rs < 5:
                continue
            blocks.append((rs, re))
        if len(blocks) <= 1:
            continue
        print(f"  column x[{x0+cs}:{x0+ce}] blocks(y):",
              [(a, b) for a, b in merge_close(blocks, 14)])


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("crop", help="原图裁出归一化幻灯片")
    c.add_argument("input")
    c.add_argument("-o", "--out", default="")
    c.set_defaults(fn=cmd_crop)

    b = sub.add_parser("blend", help="原图与模板截图 50% 叠加")
    b.add_argument("input")
    b.add_argument("slug")
    b.add_argument("n", type=int)
    b.add_argument("-o", "--out", default="/tmp/measure/blend.png")
    b.add_argument("--print-box", action="store_true", help="顺带打印原图幻灯片边界")
    b.set_defaults(fn=cmd_blend)

    m = sub.add_parser("measure", help="打印竖带区文字/色块的行段与列段")
    m.add_argument("input")
    m.add_argument("--mask", choices=list(MASKS) + ["custom"], default="blue")
    m.add_argument("--x", nargs=2, type=int, default=[0, 1920], metavar=("X0", "X1"))
    m.add_argument("--y", nargs=2, type=int, default=[0, 1080], metavar=("Y0", "Y1"))
    for name, default in (("b_min", 120), ("b_r", 40), ("g_delta", 20), ("r_min", 0)):
        m.add_argument(f"--{name}", type=int, default=default)
    m.set_defaults(fn=cmd_measure)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()