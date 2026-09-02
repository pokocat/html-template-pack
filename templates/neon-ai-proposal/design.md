---
version: alpha
name: Neon AI Proposal
description: "An acid, Y2K-tinged business-proposal system for AI digital-marketing agencies. A pure-black canvas carries electric neon-yellow (acid lime) display type, with a handful of light 'paper' pages inverting to off-white for contrast. Archivo Black headlines stack in full-caps with tight leading; Archivo carries body copy, labels and micro-caps chrome. The signature decorations are a five-bar rounded EQ 'capsule' motif, a yellow-to-cyan-to-green spectrum strip, concentric arc blooms, horizontal data scan-lines, and a fine film-grain overlay. The cultural reference is a confident agency pitch dressed as an acid rave poster: black + one acid-yellow accent, data-first, high-voltage."

colors:
  bg: "#000000"
  panel: "#141414"
  panel-2: "#1b1b1b"
  neon: "#D4FF00"
  neon-2: "#C8FF00"
  cyan: "#30E3C0"
  green: "#1FC25E"
  paper: "#f4f4f1"
  ink: "#0a0a0a"
  muted: "#a2a2a2"
  muted-2: "#7a7a7a"

color-aliases:
  lime: neon
  spectrum: "linear-gradient(90deg, neon 0%, cyan 55%, green 100%)"

typography:
  display:
    fontFamily: "Archivo Black, Archivo, Arial Black, sans-serif"
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: "-0.01em"
    textTransform: uppercase
  body:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontWeight: 400
    lineHeight: 1.6
  micro:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontWeight: 700
    letterSpacing: "0.12em"
    textTransform: uppercase

spacing:
  gutter: "clamp(40px, 4vw, 88px)"
  top-zone: "clamp(50px, 6vh, 96px)"
  bottom-zone: "clamp(50px, 6vh, 96px)"

decorations:
  - five-bar rounded EQ capsule motif (outline or solid neon)
  - yellow-to-cyan-to-green spectrum strip
  - concentric arc blooms on cover, contents and why-us
  - vertical capsule bars on the contents split panel
  - horizontal data scan-lines beside the intro portrait
  - film-grain overlay on light pages
  - hairline white rule separators in contents and why-us lists