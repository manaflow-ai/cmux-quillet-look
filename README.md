# Quillet

[![Get it on cmux](https://cmux.com/extensions/badge.svg)](https://cmux.com/extensions/manaflow-ai/cmux-quillet-look)

cmux's own type family for the agent chat. Three faces that share one line box, set for 15 px
prose at a 1.6 line height and code at the default 0.875 scale:

| Face | Where it shows | Built from |
| --- | --- | --- |
| **Quillet Sans** | the chat interface and the composer | Hanken Grotesk |
| **Quillet Serif** | replies | Newsreader |
| **Quillet Mono** | code | JetBrains Mono |

Each face is a variable-weight upright and italic, under the SIL Open Font License 1.1
([`fonts/OFL.txt`](fonts/OFL.txt)). The theme files name only the Quillet families.

Two looks: `quillet` sets only type and keeps your colors; `quillet-paper` adds a cream page, a beige
sidebar and a clay accent.

## Install

As a community theme (from the App Store's Community section, or):

```sh
cmux theme install github.com/manaflow-ai/cmux-quillet-look
cmux theme remove manaflow-ai/quillet
```

To use the paper look, set `"appearance.themeFile": "quillet-paper"` in your settings.

As a setup, which also sets the chat's font settings:

```sh
cmux setup install github.com/manaflow-ai/cmux-quillet-look
cmux setup remove manaflow-ai/quillet-look
```

Either route copies the fonts and their license to `<config dir>/fonts/<entry>/` and points the
theme file's faces there. Removing it deletes that folder, and whatever was set before comes back.

| File | What it does |
| --- | --- |
| `cmux-theme.json` | The community theme listing; declares `"fontLicense": "OFL-1.1"` |
| `cmux-setup.json` | The setup: picks the `quillet` theme file and sets the chat's families, size and line height |
| `themes/quillet.json` | Type only: the three families, the six faces, size and line height |
| `themes/quillet-paper.json` | The same type on warm paper colors |
| `fonts/` | The six `.woff2` faces and `OFL.txt` |
| `sources/` | The upstream fonts they are built from, pinned by sha256 in `SOURCES.json` |
| `build/` | The scripts that build `fonts/` from `sources/` |

## Rebuild

```sh
pip install -r build/requirements.txt && python3 build/build.py
```

`build/build.py` runs `sans.py`, `serif.py` and `mono.py` in turn, each writing its upright and
italic `.woff2` into `fonts/` and a report into `build/out/`, then prints a size table.

## Design changes

What Quillet changes from its sources, face by face: [docs/DESIGN.md](docs/DESIGN.md).

## License

The fonts and their sources are under the SIL Open Font License 1.1; everything else is MIT. See
[LICENSE](LICENSE).
