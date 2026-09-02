---
version: alpha
name: Silver Foil Pitch
description: "一套银箔压纹纸面上的商务 Pitch Deck。整版银色反光箔纸做底，只有一种正蓝（#2254c4）承担全部标题、正文、色块与线条；浅蓝（#d9e6f4）只出现在图表的次级柱形。Montserrat 一字体到底，大标题极粗极大、行距极紧，正文小而疏。装饰语汇极少：细蓝横线做页眉页脚分隔，蓝色实心色块做标签与卡片，没有任何多余点缀——层次全靠纸面反光和蓝色的尺度对比。"

colors:
  foil: "#cfcfcf"
  blue: "#2254c4"
  blue-body: "#3062ca"
  pale: "#d9e6f4"
  pie-grey: "#a9aeb6"
  pie-pale: "#dfe3e8"

color-aliases:
  accent: blue
  chart-secondary: pale

typography:
  display:
    fontFamily: "Montserrat, Helvetica Neue, Arial, sans-serif"
    fontWeight: 700
    lineHeight: 0.88-1.0
    letterSpacing: "0 至 -0.025em"
  body:
    fontFamily: "Montserrat, Helvetica Neue, Arial, sans-serif"
    fontWeight: 400
    lineHeight: 1.42-1.7
  micro:
    fontFamily: "Montserrat, Helvetica Neue, Arial, sans-serif"
    fontWeight: 600
    size: "12-20px"

spacing:
  left-gutter: "142-158px"
  top-zone: "72px（页眉 brand / date）"
  bottom-rule: "距底 10px 的 2px 蓝线"

decorations:
  - 银箔压纹纸底纹（assets/foil.png，整版 cover）
  - 页眉细蓝线（topline，右上 663px 宽 2px）
  - 页脚通栏 2px 蓝线（botline）
  - 蓝色实心色块：统计标签、产品卡片、图表标签条
  - 圆形实心图标（电话 / 定位 / 地球，白线描边细节）
  - 封面标题下 4px 蓝色粗横线

slides:
  - 01 封面：超大 Pitch Deck 标题 + 粗蓝线 + 三枚联系图标
  - 02 About：左竖幅照片，右大标题 + 正文
  - 03 Problem：大标题 + 导语 + 三栏小字 + 右竖幅照片
  - 04 Solution：左标题 + 横幅照片 + 导语，右 2×2 关键词网格（标题 + 正文 + 短蓝线）
  - 05 Product Overview：左大标题 + 导语，右 2×2 蓝卡 / 照片交错棋盘
  - 06 Market Size：左大标题 + 世界地图 + 小字，右三组「标签条 + 大数字 + 说明」
  - 07 Market Affirmation：大标题 + 导语 + 三组大数字，右竖幅线构照片
  - 08 Business Model：左标题 + 横幅照片 + 导语，右标签条 + 比例 + 双饼图 + 双组柱状图
  - 09 Our Team：标题 + 导语 + 四人照片行（右上蓝色职位标签）
  - 10 Thank You：超大标题 + 导语 + Ready 行 + 右侧联系方式
---
