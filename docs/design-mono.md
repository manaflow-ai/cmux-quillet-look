# Quillet Mono: design notes

Quillet Mono is the code face of Quillet: inline code and code blocks inside agent replies, set at the
chat's default code scale, 0.875 of 15 px prose (13.1 px). It is built by `build/mono.py` from JetBrains
Mono (SIL OFL 1.1, no Reserved Font Name), as a renamed modified version: the original copyright stays in
name ID 0 and the license ships as `fonts/OFL.txt`. Every change below is our own code run on the OFL
outlines; no outline is traced or copied from any other face. The numbers come from `build/out/mono.json`.

## 1. x-height for code inside serif prose

The earlier stand-in pack set its code at 0.8 instead of the chat's default 0.875: the stock mono's
lowercase stood well above the serif's. Quillet Serif now targets an x-height of 0.50 em, 7.5 px at 15 px.
At the default code scale the mono is set at 13.1 px, so its x-height in pixels is `x / 1000 * 13.125`.

| | x-height (units) | at 13.1 px | against the serif's 7.5 px |
| --- | --- | --- | --- |
| JetBrains Mono (measured on x) | 550 | 7.22 px | 0.963 |
| Quillet Mono | 540 | 7.09 px | 0.945 |

Against a 0.50 em serif the source's 550 already lands inside the 7.1 to 7.3 px window. Quillet Mono still takes 540, the low end of
it, for an optical reason: a monospaced letter is wider than the serif letter beside it (600 units against the serif's
narrower lowercase), so at an equal x-height it reads larger. Sitting about 0.4 px under the serif's
lowercase, inline code reads as the same size of type, not a size up, and the theme keeps the default 0.875
scale. Ascenders, capitals, figures and descenders keep their heights (`common.set_x_height` stretches only
the band from the baseline to the x-height, and from there to the ascender); accents and mark anchors over
lowercase move with the letters; in the italic, points move along the slant so the italic angle is kept.

## 2. Width: no tracking

The advance stays at 600 units: 7.9 px a character at 13.1 px. That is already one of the more open
monospace widths (several system monospace faces sit at 600 to 602 as well), and the lower x-height in
section 1 opens the letters a little more against that width. More room would push code blocks to wrap
earlier in a chat column that is often narrow, and inline code would grow wider than the serif words around
it. So `TRACK = 0`: the grid is the source's, every spacing glyph keeps one advance, and the face stays
monospaced (checked in section 8).

## 3. Default forms: the dotted zero, and why there are no other swaps

The pinned source build (`sources/SOURCES.json`) carries one alternate
set: `zero`, which swaps the default zero (an oval with a dot in its counter) for `zero.zero` (an oval with
a slash). Its GSUB has no `cvNN` or `ssNN` features and its glyph set no other letter alternates (no second
g, l, r, f or y), so the letterforms are the source's: the single-storey g, the l and i with their
feet, all kept.

Quillet Mono keeps the **dotted zero** as the default (`DEFAULT_FEATURES` stays empty; the slashed form
stays one `font-feature-settings: "zero"` away):

- the slashed zero reads as Ø and ø, which are in the Latin subset and turn up in names and Nordic text an
  agent may quote; the dot has no such twin;
- the dot is the quieter mark: in a serif paragraph the slash is a diagonal stroke the prose never has, the
  dot a small round counter-mark like the dot of an i;
- at 13 px the dot still separates 0 from O on its own (checked in the proof at 13.1 px: `0O0`).

The warmer r, f, t, j terminals come from section 5, which rounds them on the
source's own outlines, not from an alternate.

## 4. Ligatures: off

The source's `calt` feature joins operator sequences into ligatures (`->`, `=>`, `!=`, `>=`, `===`,
`/*`, ...). Chat code is mostly read and copied, rarely typed: an agent quotes a command, a diff, a config
line. There a ligature hides the characters the reader will paste (a `!=` drawn as one sign, a `--` drawn
as a dash in a flag), and in inline code next to prose the joined shapes read as math symbols rather than
code. So the face draws code as typed: `calt` is dropped at subset time (`DROP_FEATURES`). `aalt` goes with
it: that feature only feeds glyph-picker lists in desktop apps (no browser applies it), and once `calt` was
gone it alone still reached the 139 ligature glyphs. With both out the Latin subset falls from 412 to 273
glyphs, the largest single cut in the file (section 7). A reader who wants ligatures can set a ligature face
for code in their own theme.

## 5. Terminals: softened, a quarter pixel at most

`common.soften_corners` rounds sharp convex corners: the corner point becomes the control point of a short
quadratic arc between two new on-curve points, one on each edge. Quillet Mono uses it with
`fraction 0.2, cap 20, curve_ends`:

- The radius at each weight master is 0.2 of the shorter edge there, at most 20 units. At 13.1 px one pixel
  is 76 units, so a corner rounds by a quarter pixel at most: the stems' straight edges still land on whole
  pixels and nothing blurs, while the ends lose the cut-metal edge. At larger sizes (a zoomed code block,
  the 20 px and up a reader may set) the rounding shows as a soft, ink-like end. Thin weights round less
  than bold ones because their edges are shorter.
- `curve_ends` (new in `common.py`, off by default for the other faces) also rounds the corners where a
  straight cut meets a curve: the terminals of a, c, f, j, r, s, t, y. Those are the ends that read as
  "warm" or "cold"; without it only stems and slabs would change.
- Glyphs: letters and figures (Unicode L and N) and their alternates. Punctuation, operators and brackets
  keep their sharp, geometric ends: in code they are the structure (`->`, `=>`, `{}`, `[]`, `|`), and
  their crisp corners keep them distinct from letters at 13 px. Figures are softened with the letters
  because they sit in the same words (`0x1f`, `utf8`) and a sharp 1 or 4 next to a soft l would look
  like a different face.

## 6. Line box and names

`common.set_line_metrics` puts the face on the line box all three Quillet faces share: ascender 960,
descender -240, no gap (1.2 em), `USE_TYPO_METRICS` on, win metrics covering the subset's ink. Inline code
in a serif line then keeps the serif's baseline and line height. `common.rename` names the family
"Quillet Mono" (styles Regular and Italic, both variable in weight), keeps the original copyright line in
name ID 0 and adds ours, and points the license fields at the OFL.

| Metric (units of 1000) | Source | Quillet Mono |
| --- | --- | --- |
| x-height (x) | 550 | 540 |
| cap height (H), ascender (b) | 730, 730 | 730, 730 |
| descender (p) | -180 | -180 |
| hhea / typo ascender, descender, gap | 1020, -300, 0 | 960, -240, 0 |
| win ascent, descent | 1020, 300 | 994, 240 (the subset's ink) |
| advance | 600 | 600 |

Both styles measure the same.

## 7. Size

Both files are variable in weight (the source's 100 to 800 axis) and cut to the Latin range
every Quillet face uses (`common.LATIN`), with hinting dropped (the chat renders through macOS text
rendering, which ignores TrueType hints).

| File | Source, same Latin subset | Source subset without calt and aalt | Quillet Mono |
| --- | --- | --- | --- |
| `quillet-mono.woff2` | 40,680 B (39.7 KiB) | 22,220 B (21.7 KiB) | **24,912 B (24.3 KiB)** |
| `quillet-mono-italic.woff2` | 43,044 B (42.0 KiB) | 24,220 B (23.7 KiB) | **27,048 B (26.4 KiB)** |

Each file is 37 to 39 % smaller than the untouched source cut to the same subset, and well under the 80 KB
budget. Dropping the ligatures takes 18 KB off each; the edits put back about 2.7 KB (mostly the rounded
corners: two points a corner, 475 upright and 462 italic, in the outline and both weight masters).

## 8. Checks

`build/mono.py` checks each written file and fails the build if a check fails (results in
`faces[].verify` of the report):

- the woff2 reopens;
- it still interpolates: `fontTools.varLib.instancer` instances it at the weight axis' minimum, default and
  maximum, every glyph compiles at each, and each instance saves;
- monospace holds: every glyph with a non-zero advance has the same advance in the variable font and in all
  three instances;
- point counts before and after for 0, a, g, l and r (corner rounding adds two points a corner):

  | Glyph | Upright before → after | Italic before → after |
  | --- | --- | --- |
  | 0 (zero, dotted) | 44 → 44 (all curves: nothing to round) | 44 → 44 |
  | a | 40 → 48 | 37 → 45 |
  | g | 45 → 53 | 46 → 54 |
  | l | 15 → 25 | 14 → 24 |
  | r | 22 → 36 | 22 → 36 |

- the names: family "Quillet Mono", the original copyright kept in name ID 0; and no dropped feature left
  in GSUB;
- OVERLAP_SIMPLE flags before and after (the source sets none, so there is nothing to keep here; the
  count is reported so a source that does set them shows it).

Result of the build that made the files in `fonts/` (fleet job 0fef349850c9cd6f18240277, fontTools 4.60.1):
both faces pass. 0 glyph errors at weights 100, 400 and 800; one advance, 600, in the variable font and in
every instance; x-height 540 at every weight; GSUB left with `case ccmp frac locl ordn sinf subs sups zero`.

## common.py changes made for this build

- `edit_glyph` keeps OVERLAP_SIMPLE (flag 0x40 on a glyph's first point). Edits that rebuild the flag list
  from on-curve bits alone (`soften_corners`) dropped it; variable fonts set it on glyphs whose contours
  overlap, and without it some rasterizers draw the overlap darker or with a seam. JetBrains Mono sets it on
  no glyph, so this face does not exercise it; it is there for sources that do.
- `soften_corners(..., curve_ends=False)`: new option that also rounds corners where a straight cut meets a
  curve, using the curve's tangent (its off-curve neighbour) as the edge. Off by default, so the other faces
  build as before.
- `set_x_height` moves points along the italic angle (`post.italicAngle`) in italics, so a stretched or
  shortened italic lowercase keeps its slant instead of standing up or leaning over.
