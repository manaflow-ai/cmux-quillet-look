# Quillet Serif

Quillet Serif sets the agent's replies in the cmux chat: prose at 15 px with a 1.6 line height
(24 px lines), on screen. `build/serif.py` builds it from Newsreader (SIL OFL 1.1, no Reserved Font
Name). Every change below is our own code run on Newsreader's OFL outlines; no outline comes from
any other typeface. The name table keeps Newsreader's copyright line (name ID 0) and adds ours; the
license is `fonts/OFL.txt`.

Units are 1000 per em (the build scales Newsreader's 2000-unit em to 1000 first, the em the shared
line box and the other two faces use). At 15 px one unit is 0.015 px. Every number below is from
`build/out/serif.json`, measured at wght 400.

| | Newsreader at opsz 12 | Quillet Serif |
| --- | --- | --- |
| x-height, upright | 469 (7.04 px) | 500 (7.50 px) |
| x-height, italic | 479 (7.19 px) | 500 (7.50 px) |
| cap height | 689 (10.34 px) | 689 (10.34 px) |
| ascender (b), descender (p) | 726, -239 | 726, -239 |
| average lowercase advance, upright | 532 | 538 |
| average lowercase advance, italic | 499 | 504 |
| line box (hhea, OS/2 typo) | 735 / -265 | 960 / -240, gap 0 |
| default figure "1" | tabular, 600 | proportional, 421 |
| woff2, upright | 61,312 B | 63,396 B |
| woff2, italic | 68,072 B | 69,504 B |

## Optical size: pinned at 12

Newsreader's opsz axis runs 6 to 72, default 18. Small optical sizes are drawn for small text: a
larger x-height, sturdier serifs and hairlines, wider letters, looser fit. What the axis does at
wght 400, in ems:

| opsz | x-height | avg lowercase advance | n: advance minus ink |
| --- | --- | --- | --- |
| 6 | 0.512 | 0.601 | 0.066 |
| 10 | 0.484 | 0.555 | 0.055 |
| 12 | 0.469 | 0.532 | 0.050 |
| 14 | 0.455 | 0.509 | 0.046 |
| 16 | 0.441 | 0.486 | 0.039 |
| 18 (default) | 0.426 | 0.463 | 0.033 |

`font-optical-sizing: auto` would pick opsz 15 for 15 px text, the size for print-like rendering.
On screen the hairlines and serif tips of a 15 px serif are fractions of a pixel and turn grey, so
the build pins a cut three steps below: opsz 12's serifs are sturdier (the l with its foot serif is
8 % wider than at opsz 16, 0.258 em against 0.238), 28 % more room inside n (0.050 em against 0.039), and an
x-height of 0.469 that needs only a 6.6 % stretch to reach 0.50 (opsz 16 would need 13.5 %, enough
to change the letters' proportions). Lower still (10 and below) widens the text by another 4 % and
starts to look like caption type. `fontTools.varLib.instancer` pins opsz and keeps wght variable,
which drops every opsz delta: the Latin woff2 goes from 137,456 B (both axes) to about 61 KB.

## x-height: 0.50 em

Measured first: 469 upright and 479 italic at opsz 12 (938 and 958 of 2000). The build stretches
lowercase to 500 (`common.set_x_height`): points between the baseline and the x-height scale up,
points between the x-height and the ascender compress into the rest, so ascenders (726),
descenders (-239) and capitals (689) keep their heights; marks over lowercase (composite accents
and the GPOS mark anchors) move up with the letters; liga's ligatures go with them; in the italic
a point that moves up also moves along the slant. Each weight master is mapped and its deltas
solved again, so the bold keeps its own proportion (x-height 509 upright, 514 italic at wght 800).

Why 500: at 15 px it is 7.5 px, so a lowercase letter fills seven and a half pixel rows instead of
seven; the counters of a, e, s open and the text reads a size larger without taking more width.
It stays a serif's x-height, under the sans: the family at 15 px reads Quillet Sans 0.52 em
(7.8 px), Quillet Serif 0.50 em (7.5 px), Quillet Mono 0.55 em at 0.875 of the size (7.2 px), so
inline code sits just below the prose's lowercase and UI labels just above it. Cap height stays
689 (10.3 px), x-height to cap height 0.73 (was 0.68), still a text face's proportion.

## Spacing: +6 units upright, +5 italic

`common.track` adds the units to every spacing glyph, half on each side. The taller x-height makes
each letter taller but not wider, so the white between letters is a smaller share of the letter;
+6 (0.09 px a letter at 15 px, +1.1 % of the average advance) gives that back and leaves a little
more air for screen reading. The italic is already tighter by design and gets +5. Kerning is
Newsreader's. Average lowercase advance: 532 to 538 upright, 499 to 504 italic.

## Line box (shared)

`common.set_line_metrics`: ascender 960, descender -240, no line gap, USE_TYPO_METRICS, in hhea and
OS/2 typo (Newsreader's own box was 735 / -265). Sans and Mono get the same box, so inline code and
UI text in a reply keep one baseline and one line height. Win metrics cover the subset's ink
(960 / 249). OS/2 cap height is set to the measured 689 (the source field was opsz 18's 670).

## Figures and alternates

Newsreader's GSUB has case, liga, locl, ordn, pnum, rvrn, sups and tnum. Its default figures are
tabular lining; pnum gives proportional lining figures (".lf"). There are no old-style figures, no
stylistic sets, no character variants and no salt, so no alternate a, g, y or ampersand exists.

- Default: proportional lining figures (`common.make_default` with pnum, for 0 to 9). In running
  prose tabular figures leave holes ("1" is 600 units wide, the proportional one 421), so "12
  files" and "1,284" read as words. `tnum` still reaches the tabular figures (one.lf -> one, 606)
  for tables; sups and the other features follow the new default too.
- Missing: old-style figures would suit the bookish tone, but they are not in Newsreader and
  drawing 3, 4, 5, 7, 9 below the baseline is real type design, not a clean code edit, so the
  build does not fake them. Same for a single-storey a or an alternate g, y or ampersand:
  Newsreader's own a (double storey with a ball terminal), g (two storey) and & already read warm
  and bookish, so nothing is lost by keeping them.

## Terminals: soften

Newsreader's text cuts already have bracketed serifs and ball terminals (a, c, f, r, y); what reads
cold is the dead-square serif tips, stem feet and stroke ends. Sharpening would push toward a
newspaper or display feel; the target is warm and bookish, so the build rounds them instead.
`common.soften_corners` turns every convex straight-to-straight corner of a letter that turns
between 60 and 120 degrees into a short curve: radius 0.3 of the shorter edge, at most 12 units,
edges under 12 units left alone. Upright: 638 corners in 125 letter glyphs; italic: 409. Acute
joins (more than 120 degrees of turn: the apex of v and w, the crotch of k) stay sharp, so the
letters keep their bite. Excluded: figures (their crisp shapes and rhythm are the point),
punctuation and symbols (small marks, where a rounded corner reads as blur). Accented letters are
composites and follow their base letter.

At 15 px on a 1x screen the radius is at most 0.18 px: the change there is a softer edge pixel,
not a visible curve. On a 2x screen (0.36 device px) and at larger sizes the serif tips read
blunt and slightly rounded, the warm feel the face is for.

## Weight: +60 (CSS 400 draws Newsreader 460)

Leo, 2026-11-22: "anyways i think quillet is just maybe a bit too thin". At 400 the reply serif drew
n's stem at 0.086 em, 1.29 px at 15 px. The Claude desktop app's reply serif at its 400 draws 0.0985
em: 1.48 px at 15 px, 1.58 px at 16 px. Stem is n at mid x-height, on the outline.

| Quillet Serif, CSS 400 | draws Newsreader | stem, em | at 15 px | at 17 px |
| --- | ---: | ---: | ---: | ---: |
| before | 400 | 0.086 | 1.29 px | 1.46 px |
| +30 | 430 | 0.093 | 1.40 px | 1.58 px |
| **+60 (built)** | **460** | **0.101** | **1.52 px** | **1.72 px** |
| +100 | 500 | 0.110 | 1.65 px | 1.87 px |

+60 sits between the reference serif's stem at 15 px and at 16 px, so 15 px replies read with the
same gray as the Claude app's. +30 stays thin next to the sans, which is +50 since 1.0.2 (see
design-sans.md 2b); +100 reads as a medium. Heavier is checked in light and dark, in the replies, the
user bubble and the sidebar rows, in the PR's specimen.

How: `common.shift_weight(font, WEIGHT)` (the sans' function), run right after the Latin subset so the
x-height, corners and tracking work on the 460 outlines. fontTools' instancer moves the axis default
to Newsreader 460 and cuts the range to [260, 800], then the axis is relabelled 60 lower, [200, 740],
default 400. CSS 400 draws Newsreader 460, 600 (bold) draws 660; CSS weights above 740 clamp to it,
which is Newsreader's own 800. `WEIGHT = 60` sits in `build/serif.py`; `--weight N --work DIR` builds
a variant, and `--weight 0` builds the files this change replaced.

## Size

"Before" is the untouched source pinned at the same opsz, cut to the same Latin subset without
hinting, as woff2, made by the same fontTools in the same run; "after" is the shipped file.

| | before | after |
| --- | --- | --- |
| upright | 61,312 B | 63,396 B |
| italic | 68,072 B | 69,504 B |
| both axes, Latin (for reference) | 137,456 B / 153,908 B | |

Both are under 80 KB. The weight shift (+60) adds about 4 KB a file: the masters are solved again
around the 460 outline.

## Checks (in serif.json under verify)

- Each woff2 reopens with fontTools; one axis left (wght 200 to 740, see Weight), 279 glyphs.
- `instancer` cuts each at wght 200, 400 and 740 and every glyph draws (decomposed) with no error:
  the re-solved deltas still interpolate.
- Point counts (contours unchanged):

| | a | e | g | r | y |
| --- | --- | --- | --- | --- | --- |
| upright, before | 69 | 37 | 101 | 35 | 36 |
| upright, after | 69 | 41 | 101 | 47 | 52 |
| italic, before | 54 | 51 | 110 | 44 | 66 |
| italic, after | 56 | 51 | 112 | 48 | 66 |

## What does not change

Newsreader's drawings, kerning and features stay as they are; its weights move 60 units (Weight). The build moves points
(x-height), adds them (corners), moves advances (tracking) and repoints the figures; it draws no
new letter.
