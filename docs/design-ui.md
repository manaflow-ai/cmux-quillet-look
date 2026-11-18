# Quillet UI: design notes

Quillet UI is the interface cut of Quillet: sidebar rows, labels, the composer and chat text at 13-15 px.
It is built by `build/ui.py` from Geist (SIL OFL 1.1, no Reserved Font Name), as a renamed modified
version: the original copyright stays in name ID 0 and the license ships as `fonts/OFL.txt`. Every change
is our own code run on Geist's OFL outlines (`build/ui_steps.py` on top of `build/common.py`); no outline
is traced or copied from any other face. The `quillet-ui` look uses it in place of Quillet Sans; the
other looks are unchanged.

## The targets

Four numbers describe how interface text at these sizes reads, and each is a target the cut is built to:

| Measure | What it is | Upright | Italic |
| --- | --- | --- | --- |
| x-height | lowercase height, per em | 0.540 | 0.540 |
| x / cap | x-height over capital height | 0.750 | 0.750 |
| width per x-height | average lowercase advance (English letter frequencies) over the x-height | 0.972 | 0.959 |
| ink density | ink area of `n o h e` over advance x x-height: weight, independent of width | 0.410 | 0.423 |

## Choosing the source

Twenty OFL sans faces from google/fonts at commit `5bd87dfc`, none with a Reserved Font Name, each
measured at weight 400. The score adds the relative misses on x / cap, width per x-height and the
per-letter width pattern (RMS over a-z after removing the overall width), half the x-height miss (the
build can move it) and half the stem miss at the weight whose density meets the target (weight is a
setting; the stem-to-x-height ratio at equal colour is not).

| Face | x | x/cap | w/x | density | n stem / x at equal colour | a-z RMS | score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| target | 0.540 | 0.750 | 0.972 | 0.410 | 0.167 | 0 | 0 |
| **Geist** | 0.530 | 0.747 | 0.969 | 0.389 | 0.171 | 0.031 | **0.060** |
| Manrope | 0.540 | 0.750 | 0.952 | 0.361 | 0.162 | 0.047 | 0.083 |
| Onest | 0.527 | 0.745 | 0.971 | 0.386 | 0.175 | 0.058 | 0.103 |
| Schibsted Grotesk | 0.527 | 0.750 | 0.966 | 0.378 | 0.174 | 0.066 | 0.104 |
| Inter | 0.543 | 0.746 | 0.943 | 0.388 | 0.173 | 0.077 | 0.135 |
| Golos Text | 0.530 | 0.757 | 1.003 | 0.388 | 0.177 | 0.059 | 0.141 |
| Plus Jakarta Sans | 0.536 | 0.720 | 0.987 | 0.355 | 0.168 | 0.082 | 0.145 |
| Figtree | 0.500 | 0.714 | 0.982 | 0.389 | 0.171 | 0.043 | 0.151 |
| Funnel Sans | 0.500 | 0.741 | 0.985 | 0.408 | 0.181 | 0.060 | 0.166 |
| Instrument Sans | 0.510 | 0.708 | 0.997 | 0.370 | 0.178 | 0.044 | 0.188 |
| Public Sans | 0.517 | 0.715 | 0.993 | 0.403 | 0.183 | 0.050 | 0.188 |
| Albert Sans | 0.500 | 0.714 | 1.000 | 0.367 | 0.172 | 0.064 | 0.192 |
| DM Sans | 0.502 | 0.717 | 1.015 | 0.388 | 0.180 | 0.046 | 0.211 |
| Hanken Grotesk (Quillet Sans' source) | 0.493 | 0.707 | 0.993 | 0.395 | 0.180 | 0.060 | 0.223 |
| Inter Tight | 0.546 | 0.750 | 0.860 | 0.403 | 0.156 | 0.088 | 0.240 |
| Rethink Sans | 0.496 | 0.709 | 1.031 | 0.387 | 0.180 | 0.056 | 0.253 |
| Red Hat Text | 0.488 | 0.697 | 1.000 | 0.340 | 0.189 | 0.045 | 0.259 |
| Work Sans | 0.500 | 0.758 | 1.071 | 0.358 | 0.190 | 0.048 | 0.266 |
| Outfit | 0.475 | 0.684 | 1.033 | 0.452 | 0.171 | 0.065 | 0.288 |
| Wix Madefor Text | 0.492 | 0.688 | 1.047 | 0.365 | 0.182 | 0.045 | 0.295 |

Geist wins on every proportion: its x-height over cap is already 0.747, its letters are within 3 % of the target width pattern (half of Hanken's miss), and at equal colour its
stems are 2 % off. What it lacks is size and colour: a 0.530 x-height and a light 400.

## The changes

In build order, with what they came to (`build/out/ui.json`):

1. **Regular weight.** CSS weight 400 draws Geist's 430 upright and 440 italic: the weights where the
   density meets 0.410 and 0.423. The variable font's default is re-centred there with the fontTools
   instancer (axis ends kept) and labelled 400 again, so 100 and 900 still draw what they drew and the
   scale between leans heavier by at most 30 and 40. It is done first because a heavier design is a
   little wider and taller, and the next two steps measure the regular that ships. The theme route needs
   no weight setting for it.
2. **Larger on the em.** Everything is drawn 1.017 times larger (outlines, advances, kerning, anchors,
   variation data; fontTools `scale_upem`, then the em set back to 1000), which brings the x-height to
   540 and keeps capitals, figures and spacing in proportion: x / cap stays 0.748. The theme route needs
   no size-adjust for it.
3. **Lowercase width.** Lowercase is scaled horizontally to 0.972 (upright) and 0.959 (italic) x-heights
   per average letter: factors 0.997 and 0.998, outlines and every variation delta together (a linear
   map, so the font interpolates as before), with HVAR rebuilt. Kerning is left as it is.
4. **Line box.** The shared Quillet line box (960 / -240, no gap), like the other faces.

## After

Measured at CSS weight 400 (the same script as the table):

| | x | x/cap | w/x | density | n stem / x | a-z RMS |
| --- | --- | --- | --- | --- | --- | --- |
| target, upright | 0.540 | 0.750 | 0.972 | 0.410 | 0.167 | 0 |
| Quillet UI | 0.540 | 0.748 | 0.972 | 0.410 | 0.170 | 0.030 |
| target, italic | 0.540 | 0.750 | 0.959 | 0.423 | 0.170 | 0 |
| Quillet UI Italic | 0.540 | 0.748 | 0.959 | 0.424 | 0.176 | 0.032 |

What stays Geist's own: the letter shapes, the per-letter widths (`l`, `z`, `j`, `k`, `g` run 6-10 %
wide of the target pattern, `t`, `r`, `y` 3-4 % narrow) and the stem contrast. Files: 37.9 KB upright,
40.3 KB italic (`.woff2`, Latin subset).
