"""The two outline steps Quillet UI adds to the pipeline: drawing a face larger on its em, and scaling its
lowercase horizontally. Both are linear maps, applied to the default outline and to every variation delta, so the
variable font interpolates as before. Built on build/common.py.
"""

from __future__ import annotations

from typing import Iterable

from fontTools.misc.fixedTools import otRound
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

from common import _gpos_subtables, lowercase_glyphs, measured


def scale_width(font: TTFont, factor: float, glyphs: Iterable[str] | None = None) -> dict:
    """Scales glyphs horizontally by `factor` about x = 0: outlines, advances and side bearings at every master,
    composite offsets, and the GPOS mark anchors on them. A linear map commutes with interpolation, so the
    default outline and every gvar delta (phantom points included, which carry the variable advance) scale by
    the same factor and the font interpolates as before. HVAR is rebuilt from the scaled phantoms. Kerning is
    left as it is (at a few percent it moves a pair by a unit or two). Returns {"factor", "glyphs"}."""
    if abs(factor - 1) < 1e-6:
        return {"factor": 1.0, "glyphs": 0}
    glyf, hmtx = font["glyf"], font["hmtx"]
    names = set(glyphs) if glyphs is not None else lowercase_glyphs(font)
    gvar = font.get("gvar")
    for name in sorted(names):
        glyph = glyf[name]
        if glyph.isComposite():
            for component in glyph.components:
                component.x = otRound(component.x * factor)
        elif glyph.numberOfContours > 0:
            glyph.coordinates = GlyphCoordinates([(otRound(x * factor), y) for x, y in glyph.coordinates])
        if gvar is not None:
            for variation in gvar.variations.get(name, []):
                variation.coordinates = [
                    None if c is None else (otRound(c[0] * factor), c[1]) for c in variation.coordinates
                ]
        advance, lsb = hmtx[name]
        hmtx[name] = (otRound(advance * factor), otRound(lsb * factor))
        glyph.recalcBounds(glyf)
    for table in _gpos_subtables(font, 4):
        for base, record in zip(table.BaseCoverage.glyphs, table.BaseArray.BaseRecord):
            if base in names:
                for anchor in record.BaseAnchor:
                    if anchor is not None:
                        anchor.XCoordinate = otRound(anchor.XCoordinate * factor)
    if "HVAR" in font and gvar is not None:
        from fontTools.varLib.hvar import add_HVAR

        del font["HVAR"]
        add_HVAR(font)
    font["hhea"].advanceWidthMax = max(a for a, _ in hmtx.metrics.values())
    return {"factor": round(factor, 4), "glyphs": len(names)}


def scale_em(font: TTFont, factor: float) -> dict:
    """Draws everything `factor` times larger on the same em: outlines, advances, kerning, anchors, the variation
    data and the vertical metrics, all through fontTools' scale_upem, after which the em is set back to its
    old size. The same as setting the face `factor` larger, but inside the file, so the pack needs no
    size-adjust. Returns {"factor", "x_height"}."""
    from fontTools.ttLib.scaleUpem import scale_upem

    upm = font["head"].unitsPerEm
    if abs(factor - 1) < 1e-6:
        return {"factor": 1.0, "x_height": measured(font, "x")}
    scale_upem(font, otRound(upm * factor))
    font["head"].unitsPerEm = upm
    return {"factor": round(otRound(upm * factor) / upm, 4), "x_height": measured(font, "x")}
