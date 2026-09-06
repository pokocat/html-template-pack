---
version: alpha
name: Me Economy
description: "一套近黑画布上的个人商业趋势洞察提案。霓虹粉到紫的渐变（#ff3fa4 → #ff7ad9 → #c069ff）承担全部大标题与强调，青绿（#00e5a8）只作次级点缀与箭头；深灰面板与标签块沉在底层，黑白摄影穿插其中压出灰度层次。标题中英双语并用：中文用 Noto Sans SC 出语义，Montserrat 900 超粗大写英文散落在页眉、边角与背景水印里做节奏。装饰语汇克制——背景超大水印字、粉色圆形编号、青绿短横线、渐变字，不堆砌图形。"

colors:
  bg: "#0c0c0e"
  panel: "#151517"
  chip: "#222226"
  pink: "#ff3fa4"
  pink2: "#ff7ad9"
  violet: "#c069ff"
  teal: "#00e5a8"
  muted: "#a6a6ae"
  dim: "#64646c"
  line: "rgba(255,255,255,.13)"

color-aliases:
  accent: pink
  secondary: teal
  gradient: "pink → pink2 → violet"

typography:
  display:
    fontFamily: "Montserrat, Helvetica Neue, Arial, sans-serif"
    fontWeight: 900
    lineHeight: 0.92-1.16
    letterSpacing: "-0.03em 至 0.02em"
  body:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontWeight: 400-700
    lineHeight: 1.5-1.7
  micro:
    fontFamily: "Montserrat, Helvetica Neue, Arial, sans-serif"
    fontWeight: 600-800
    size: "8-30px"
    letterSpacing: "0.12-0.34em 大写"

spacing:
  left-gutter: "64-120px"
  top-zone: "42px（页眉 logo / nav / badge）"
  section-gap: "26-60px"
  card-radius: "10-16px"

decorations:
  - 背景超大水印字（Montserrat 900，白色 3%-6% 透明度，如 ME ECONOMY / BRAND / NO.01）
  - 渐变粉字（.grad，background-clip: text）
  - 页面顶部通栏页眉：左 logo + 中五项目录 + 右描边粉徽章
  - 圆形描边编号（封面目录 01-05）
  - 青绿短横线（章节过渡 kicker 前导）
  - 深灰 panel / chip 标签块，强调项「hot」用粉描边 + 粉底
  - 黑白摄影（grayscale + contrast），多用于封面与生活场景页
  - 侧边白色竖条 / 底栏浅色「formula / band」块做明暗反差

slides:
  - 01 封面 Contents：右竖幅黑白照片 + 超大幅渐变 Contents + 五项目录 + 底部导语
  - 02 章节过渡：CHAPTER 01 / 我经济超大标题
  - 03 公司越来越小：左大标题 + 右上英英引言 + 下「过去创业 vs 个人经济」标签对比
  - 04 不是没有公司：左竖幅照片 + 右下大标题 + 白色侧条公式
  - 05 过去开店 vs 现在建系统：左右两列对照 + 中央 VS 圆
  - 06 数据：13,000 万 / 30,000 万两组超大数据 + 底部导语
  - 07 成为自己的品牌：居中超大标题 + 英文 + 人群标签
  - 08 超级个体：大标题 + 过去/未来经济结构对比链
  - 09 能力 Able：超大「能力」+ 曲线 + 右侧 Market 强调
  - 10 六大能力模型：半圆辐射图 + 六节点能力标签
  - 11 越专业越不被替代：标题 + 服务标签 + 底部浅色市场栏
  - 12 越靠近生活越稳定：标题 + 获客流程 + 2×2 生活场景照片
  - 13 小步验证持续迭代：标题 + 七步流程 + 两张照片
  - 14 五步进阶法：标题 + 五卡片 + 底部公式栏
  - 15 新时代个人价值：超大标题 + 去组织化/专业化等标签
---