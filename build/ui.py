#!/usr/bin/env python3
"""Builds Quillet UI, the interface cut of Quillet: sidebar rows, labels and chat text at 13-15 px.

Built from Geist (SIL OFL 1.1, no Reserved Font Name) through build/common.py, the same pipeline as the other
faces. Three changes, each one number below; docs/design-ui.md says why. build/out/ui.json records what they
came to.

    python3 build/ui.py --out fonts   writes fonts/quillet-ui.woff2, fonts/quillet-ui-italic.woff2
                                      and build/out/ui.json (and the TTFs under build/out/ui/)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
import ui_steps  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.varLib import instancer  # noqa: E402

FAMILY = "Quillet UI"
FACES = [
    ("Geist[wght].ttf", "Regular", "quillet-ui"),
    ("Geist-Italic[wght].ttf", "Italic", "quillet-ui-italic"),
]
DESCRIPTION = (
    "Quillet UI is a modified version of Geist, cut for interface and chat text at 13-15 px: "
    "drawn larger on the em (a 540 x-height), with its lowercase set to its own width and a darker regular. "
    "It is not Geist and is not endorsed by its authors."
)

# --- The design numbers (docs/design-ui.md says why) -----------------------------------------------------

X_HEIGHT = 540  # units of 1000. Reached by drawing the whole face larger, so capitals and figures keep their
#                 proportion to the lowercase.
# Average lowercase advance per x-height, English letter frequencies, per style: the italic runs narrower.
WIDTH_PER_X_HEIGHT = {"Regular": 0.972, "Italic": 0.959}
# The source weight that CSS 400 draws, per style: where the ink density of n o h e reaches 0.410 upright, 0.423 italic.
REGULAR_DESIGN_WEIGHT = {"Regular": 430, "Italic": 440}

FREQ = dict(zip("etaoinshrdlcumwfgypbvkjxqz",
                [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0, 2.8, 2.8, 2.4, 2.4, 2.2, 2.0, 2.0, 1.9, 1.5, 1.0, 0.8, 0.15, 0.15, 0.1, 0.07]))


def weighted_advance(font: TTFont) -> float:
    cmap, hmtx = font.getBestCmap(), font["hmtx"]
    return sum(hmtx[cmap[ord(c)]][0] * w for c, w in FREQ.items()) / sum(FREQ.values())


def relabel_regular(font: TTFont, design: float) -> dict:
    """Makes user weight 400 draw the source's `design` weight: re-centres the variable font's default there
    (fontTools instancer, the axis ends kept), then labels that default 400 again. 100 and 900 still draw
    what they drew; between them the scale leans heavier by at most design - 400."""
    axis = next(a for a in font["fvar"].axes if a.axisTag == "wght")
    lo, default, hi = axis.minValue, axis.defaultValue, axis.maxValue
    if abs(design - default) < 0.5:
        return {"wght_400_draws": default}
    instancer.instantiateVariableFont(font, {"wght": (lo, design, hi)}, inplace=True)
    axis = next(a for a in font["fvar"].axes if a.axisTag == "wght")
    axis.defaultValue = default
    font["OS/2"].usWeightClass = int(default)
    if "STAT" in font:
        del font["STAT"]  # its weight values describe the old labels; renderers fall back to fvar
    return {"wght_400_draws": design, "axis": [lo, default, hi]}


def build(source_name: str, style: str, stem: str, out: Path, work: Path) -> dict:
    font = common.source(source_name)
    before = common.report(font)
    changes = []

    # 1. Latin subset first, so every later edit touches only shipped glyphs.
    common.subset(font)

    # 2. Regular weight first: a heavier design is a little wider and taller, and steps 3-4 measure the
    #    regular that ships.
    changes.append({"change": "regular weight", **relabel_regular(font, REGULAR_DESIGN_WEIGHT[style])})

    # 3. Larger on the em, to the x-height.
    em = ui_steps.scale_em(font, X_HEIGHT / common.measured(font, "x"))
    changes.append({"change": "larger on the em", **em})

    # 4. Lowercase width: the factor that brings the weighted lowercase advance to WIDTH_PER_X_HEIGHT x-heights.
    factor = WIDTH_PER_X_HEIGHT[style] * common.measured(font, "x") / weighted_advance(font)
    changes.append({"change": "lowercase width", "target_width_per_x_height": WIDTH_PER_X_HEIGHT[style], **ui_steps.scale_width(font, factor)})

    # 5. Shared line box.
    common.set_line_metrics(font)
    changes.append({"change": "line metrics", "ascender": common.LINE_ASCENDER, "descender": common.LINE_DESCENDER, "lineGap": 0})

    original = font["name"].getDebugName(0)
    common.rename(font, FAMILY, style, original, DESCRIPTION)

    sizes = common.write(font, work, stem)
    shutil.copyfile(work / f"{stem}.woff2", out / f"{stem}.woff2")
    after = common.report(TTFont(work / f"{stem}.ttf"))
    return {
        "source": source_name,
        "file": f"{stem}.woff2",
        "before": before,
        "after": after,
        "woff2_before": common.woff2_size_of_source_subset(source_name),
        "woff2_after": sizes["woff2"],
        "changes": changes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = common.ROOT / "build" / "out" / "ui"
    faces = [build(name, style, stem, out, work) for name, style, stem in FACES]
    path = common.ROOT / "build" / "out" / "ui.json"
    path.write_text(json.dumps({"family": FAMILY, "faces": faces}, indent=1, default=str) + "\n")
    for face in faces:
        print(f"{face['file']}: {face['woff2_before']} -> {face['woff2_after']} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
