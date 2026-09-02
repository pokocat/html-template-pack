# 模板提取流程

把一个来源（小红书帖子、网页、设计图）蒸馏成库里一套模板的完整流程。
用户扔来一个链接或一组图，默认走完全流程，不用逐步确认。

## 铁律

- **必须拿到原图。** 没有原图就先去取（小红书用浏览器或下载工具取原图），绝不凭文字描述想象还原。
- **逐页对齐原图。** 配色、字体、装饰、间距都照原图来，不发挥。
- **文案用中文，简单、有高级感。** 模板元数据、页面文案都不写 AI 腔。

## 流程

### 1. 取原图

从链接里把帖子全部原图下载到本地临时目录，逐张看。数清总页数，这就是模板的页数。

### 2. 脚手架

```bash
node scripts/new-template.mjs <slug>
```

slug 小写连字符，如 `neon-ai-proposal`。会建好 `templates/<slug>/` 并拷入 `deck-stage.js`。

### 3. 写 template.html

1920×1080，一页一个 section，逐页还原原图。导航二选一：

- **vanilla JS**：`.slide` 元素 + `document` 上的 keydown 监听（参考 `templates/neon-ai-proposal/`）
- **deck-stage.js**：`<deck-stage>` 包裹，子元素即幻灯片（参考 `templates/pin-and-paper/`）

两种都响应方向键翻页，截图脚本依赖这一点。

### 4. 写 template.json

字段（全部中文）：

| 字段 | 说明 |
|---|---|
| `slug` | 必须和目录名一致 |
| `name` | 中文标题 |
| `tagline` | 一句话气质描述 |
| `mood` / `tone` | 情绪 / 语气形容词数组 |
| `occasion` | 适用场合数组 |
| `formality` | low / medium-low / medium / medium-high / high |
| `density` | 同上五档 |
| `scheme` | light / dark / mixed |
| `palette` / `typography` | 配色与字体系统（含 description） |
| `best_for` / `avoid_for` | 适合 / 不适合的场合，写感觉不写行业 |
| `slide_count` | 实际页数 |

### 5. 写 design.md

设计系统说明：配色、字体、装饰语汇、间距节奏。格式参考现有模板。

### 6. 逐页核对

用截图脚本逐页截，和原图对比，不一致就改，直到对齐：

```bash
node scripts/shot.mjs <slug> 1 2 3 ... --out /tmp/check
```

### 7. 生成展示截图

```bash
node scripts/shot.mjs <slug>
```

默认截三张：第 1 页、中间页、最后一页，输出 `screenshots/<slug>-<n>.png`（1920×1080）。

### 8. 重建索引和页面

```bash
node scripts/build-index.mjs && node scripts/build-gallery.mjs
```

### 9. 部署

```bash
scp -i ~/dev/aliyun/aiartist.pem gallery.html ecs-user@47.98.162.120:/opt/gallery/
scp -i ~/dev/aliyun/aiartist.pem -r screenshots ecs-user@47.98.162.120:/opt/gallery/
```

线上地址：https://gallery.aibuzz.cn（nginx 已配好，纯静态，不用 reload）。

### 10. 提交

```bash
git add -A && git commit -m "新增模板：<中文名>" && git push
```

## 常用命令速查

| 目的 | 命令 |
|---|---|
| 新建模板骨架 | `node scripts/new-template.mjs <slug>` |
| 截图（默认三张） | `node scripts/shot.mjs <slug>` |
| 截指定页 | `node scripts/shot.mjs <slug> 2 5 8 --out /tmp/x` |
| 重建索引 | `node scripts/build-index.mjs` |
| 重建图库页 | `node scripts/build-gallery.mjs` |
