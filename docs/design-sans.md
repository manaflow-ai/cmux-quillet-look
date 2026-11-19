# Quillet Sans: design notes

Quillet Sans is the sans of Quillet: the chat interface (13-14 px), the composer and the user's own
messages (15 px). It is built by `build/sans.py` from Hanken Grotesk (SIL OFL 1.1, no Reserved Font
Name), as a renamed modified version: the original copyright stays in name ID 0 and the license ships as
`fonts/OFL.txt`. Every change below is our own code run on Hanken's OFL outlines at every weight master
(`common.edit_glyph` solves the gvar deltas again), so the weight axis (100-900) works as before. No
outline is traced or copied from any other face. The numbers come from `build/out/sans.json`.

Units are 1000 to the em; at 15 px one unit is 0.015 px, at 13 px 0.013 px.

## What Hanken gives us

Measured on the source (upright and italic agree):

| | units | em |
| --- | --- | --- |
| x-height | 493 | 0.493 |
| cap height | 697 | 0.697 |
| ascender (b d h k l) | 697 | the cap height: ascenders stop level with capitals |
| descender (p) | -204 | |
| avg lowercase advance | 503.7 (italic 508.3) | |
| line box (hhea, typo) | 1000 / -303 / 0 | 1.303 em |

Hanken already draws a hooked l (the stem turns right at the baseline) and a flat-topped 1 with a flag, and
its I is a bare stem, so I l 1 are three different shapes before any change; that stays as it is. Its
GSUB has three stylistic sets: ss01 a single-storey g (upright; in the italic, whose own g is single-storey,
ss01 and ss02 are two-storey forms), ss02 a second two-storey g, and ss03 round dots (i, j, the dot
accents, and . , : ; ! ? · … ÷ and the like). There is no single-storey a in the upright (the italic's a
is single-storey already) and no other letter alternate.

## 1. x-height: 493 -> 512 (0.512 em)

At 13 px Hanken's x-height is 6.4 px; at 512 it is 6.7 px, and at 15 px 7.7 px (from 7.4). The lowercase
is stretched from the baseline to the x-height and squeezed from there to the ascender
(`common.set_x_height`), so capitals, ascenders and descenders keep their heights, and accents and mark
anchors move up with the letters.

Why 512 and not the 520 we aimed at: Hanken's ascenders stop at the cap height (697), so every unit of
x-height comes out of the ascenders. At 512 b d h k l rise 185 units over the x-height (2.8 px at 15 px,
2.4 px at 13 px); at 520 that is 177, and the word shapes that tell "hand" from "nand" at 13 px start to
flatten. 512 keeps 26.5 % of the cap height for the ascender stroke and still reads a size up from Hanken.

Mixed line: the serif targets about 0.50 em at 15 px (7.5 px) and the mono 0.55 em at 0.875 scale
(0.48 em of the line, 7.2 px). The sans sits a little over the serif (7.7 px), which is where an interface
face should be next to its reading face; the cap height stays 697.

## 2. Spacing: +10 units of tracking

Every advance grows by 10 units, 5 on each side (`common.track`; marks and the kerning stay as they are).
That is 0.15 px at 15 px and 0.13 px at 13 px: the average lowercase advance goes from 503.7 to 516.5
(italic 508.3 to 518.3); 10 of that is the tracking, the rest the single-storey g, which is wider (588
against 514).
Why: a taller x-height makes each letter's counters and the white between letters relatively smaller, and
Hanken's spacing is set for display sizes as much as text; at 13-15 px, on 1x and 2x screens, the extra room
keeps rn from reading as m and stops bold UI labels from clotting. It is small enough to keep the face as
dense as an interface face should be. More (20 units) was not tried in this round.

## 3. Default forms

- Single-storey g in the upright (ss01 made the default). Hanken's default upright g is the two-storey
  (binocular) form; at 13 px its lower bowl closes up, the more so with the taller x-height, and it is the
  one letter in a UI line that draws the eye. The single-storey g stays open at 13 px, it matches the
  italic's g (single-storey by default), and its plain round bowl suits the soft, bookish tone. The
  two-storey g stays one feature away: `ss01` now swaps the single-storey g back to Hanken's two-storey g,
  and `ss02` still gives the other two-storey form.
- Round dots in both styles (ss03 made the default). Hanken's dots are square; round dots on i and j, on
  . : ; ! ? ¡ ¿ · • … ‥ ÷ and on the dieresis and dot accents are the warmest single change in a text line,
  and they pair with the softened corners. The comma and quotes keep their own shapes. `ss03` now brings
  the square dots back.
- Kept as they are: the two-storey a (upright) and the single-storey a (italic), Hanken's own; the hooked l;
  the flagged 1; the I without serifs. Il1 stay three shapes.

How: the cmap points at the alternates (`common.make_default`), which also makes the stylistic set that
named a form swap it back to the plain one and keeps every other substitution of the plain form working on
the new default (ss02's g, locl's Turkish i, the case forms). Applied one feature at a time (ss01, then
ss03), so ġ is the single-storey g with a round dot. Checked on the built file: in the upright, `ss01` on the
default g gives the two-storey g, `ss02` the other two-storey g, `ss03` on i and . gives the square dots.

## 4. Terminals: soften_corners, fraction 0.22, cap 18 units

The sharp convex corners where two straight segments meet (stroke ends, stem feet, the corners of E L T)
get a round whose radius is 22 % of the shorter edge at that master, at most 18 units. Stems measured on
the built upright (I): 20 units at wght 100, 88 at 400, 157 at 900. So the radius is about 4 units at 100,
18 at 400 (0.27 px at 15 px, 0.54 device px on a 2x screen: a stroke end that reads softened rather than
cut), and the cap holds it at 18 at 900, 11 % of the stem, so heavy weights do not go blobby. Only corners
turning between 55 and 125 degrees: the sharp vertices of diagonals (turns past 125 degrees) are never
touched, and nor are joins (concave). 308 corners in 70 glyphs in the upright, 323 in 73 in the italic.

Left sharp:
- the diagonal letters with flat-cut vertices, A M V W v w y, where a round on the cut vertex reads as a
  blob (their accented forms follow);
- marks, punctuation and symbols: small shapes whose corners are what make them read (the dots are round now);
- fraction and super/subscript figures (.numr, .dnom), too small for a round to show;
- curved terminals (c e s, the l's hook): soften_corners rounds only corners between two straight segments.

## 5. Line box

The shared Quillet box (`common.set_line_metrics`): ascender 960, descender -240, no gap, in hhea and OS/2
typo with USE_TYPO_METRICS, the win metrics covering the ink. Hanken's own box was 1000 / -303 (1.303 em);
the shared 1.2 em box keeps a line that mixes sans, serif and mono on one baseline at one height.

## 6. Size

Latin subset (`common.LATIN`), weight axis kept, all layout features kept, hints dropped:

| file | before (source cut to the same subset) | after |
| --- | --- | --- |
| quillet-sans.woff2 | 37,164 B | 39,300 B (38.4 KiB) |
| quillet-sans-italic.woff2 | 38,244 B | 40,668 B (39.7 KiB) |

The 6 % growth is the rounded corners (three points for one at each, in every master). Both are about half
of the 80 KB budget.

## 7. Metrics after

| | upright | italic |
| --- | --- | --- |
| x-height | 512 | 512 |
| cap height | 697 | 697 |
| ascender (b) / descender (p) | 697 / -204 | 697 / -204 |
| avg lowercase advance | 516.5 | 518.3 |
| hhea / typo | 960 / -240 / 0 | same |
| win ascent / descent | 960 / 257 | same |

## 8. Checks

Run by the build's own check on the fleet (Linux pool), on the woff2 files as shipped:

- fontTools reopens both woff2 files; every gvar tuple has the glyph's point count (0 mismatches);
- `varLib.instancer` instantiates wght 100, 400 and 900 and every glyph draws with no error; x-height is 512
  at all three;
- I, l and 1 are three different outlines and three different glyphs;
- the features reach the other forms from the new defaults (ss01 and ss02 for g, ss03 for i and .);
- names: family "Quillet Sans", styles Regular / Italic, name 0 keeps Hanken's copyright line and adds ours;
- point counts, source -> Quillet (upright): a 48 -> 56, g 78 (two-storey) -> 56 (single-storey, from 52),
  l 16 -> 20, t 21 -> 33, r 24 -> 34; italic: a 42 -> 52, g 55 -> 59, l 22 -> 26, t 27 -> 39, r 21 -> 31.
  The added points are the rounded corners;
- a specimen at wght 100, 400 and 900 (upright and italic) was drawn and looked at: no broken contours, the
  rounds show at 400 and stay small at 900.
