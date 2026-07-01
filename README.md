# Writing with BEC

A small Python toolkit that turns text into an image made of real absorption images of ultracold-atom **Bose-Einstein condensates (BEC)**. Each pixel column of the rendered text is an actual experimental optical-density (OD) picture of a condensate, taken at LCAR (Laboratoire Collisions Agrégats Réactivité, Toulouse).

This is the "BEC printer" used to produce the corresponding figure in the article and PhD theses cited below.

## How it works

- `str_matrices/` contains, for every printable character, a small binary matrix (0/1) describing which "pixels" of that character should be lit up or left dark — essentially a bitmap font.
- `BECtff/` is a library of experimental BEC absorption images, sorted into folders named after a 7-bit binary code. Each code corresponds to one possible column pattern of lit/unlit pixels, and the folder for that code contains several real absorption shots that can be used interchangeably (with optional randomization) to fill that column.
- `utils.py` assembles the requested string into a full image:
  - `word2matrix` turns a single line of text into a binary pixel matrix using the character bitmaps in `str_matrices/`.
  - `word2od` walks through that matrix column by column, picks a matching absorption image from `BECtff/`, normalizes it, and stitches everything together (with center/left/right justification for multi-line text via `justification`).
  - `bec_write` renders the resulting mosaic with `matplotlib` and saves it to `images/`.
- `script.py` is the entry point: it defines the string to render and calls `bec_write`.

## Repository structure

```
writing_with_BEC/
├── script.py         # entry point: defines the text and calls bec_write()
├── utils.py          # word2matrix, word2od, justification, bec_write
├── str_matrices/     # per-character binary bitmap matrices (.npy)
├── BECtff/            # library of real BEC absorption images (.npy), one folder per binary code
└── images/           # output folder for rendered images
```

> **Note:** `utils.py` looks for the image library under `BECttf/`, while the repository ships the folder as `BECtff/`. If you hit a `FileNotFoundError` when running the script, rename or symlink one to match the other.

## Requirements

- Python 3
- `numpy`
- `matplotlib`

## Usage

1. Edit the `string` variable in `script.py` to whatever text you want to render (use `\n` for line breaks):

```python
from utils import *

string = "Written with\nBose-Einstein Condensates"

bec_write(string)
```

2. Run it from the repository root (the image and matrix paths are relative):

```bash
python script.py
```

3. The rendered figure is saved in `images/` (PNG by default) and also displayed via `matplotlib`.

Useful `bec_write` keyword arguments: `randomize` (pick a random absorption shot per pixel instead of always the first one), `alignement` (`'center'`, `'left'`, or `'right'`), `cmap`, `vmin`/`vmax` (OD color scale), and `format` (output image format).

## Scientific context

This code produces the **"BEC printer"** and **"QUANTUM CONTROL"** figures featured in

- N. Dupont, G. Chatelain, L. Gabardos, M. Arnal, J. Billy, B. Peaudecerf, D. Sugny, D. Guéry-Odelin, *"Quantum State Control of a Bose-Einstein Condensate in an Optical Lattice"*, PRX Quantum **2**, 040303 (2021). DOI: [10.1103/PRXQuantum.2.040303](https://doi.org/10.1103/PRXQuantum.2.040303)
- C. P. Koch, U. Boscain, T. Calarco, G. Dirr, S. Filipp, S. J. Glaser, R. Kosloff, S. Montangero, T. Schulte-Herbrüggen, D. Sugny, F. K. Wilhelm, "Quantum optimal control in quantum technologies. Strategic report on current status, visions and goals for research in Europe", EPJ Quantum Technology 9, 19 (2022). DOI: [10.1140/epjqt/s40507-022-00138-x](https://doi.org/10.1140/epjqt/s40507-022-00138-x)

which illustrate how single-shot absorption images of optimally controled BECs released from an optical lattice can be assembled into text. Experimental details are presented in the following two PhD theses realized at LCAR (Université de Toulouse, supervised by David Guéry-Odelin):

- G. Chatelain, "_Façonnage d'ondes de matière dans un réseau optique dépendant du temps : du chaos quantique au contrôle quantique_" (PhD thesis, in French), Université de Toulouse, 2021. [theses.hal.science/tel-03700049v2](https://theses.hal.science/tel-03700049v2)
- N. Dupont, "_Control and transport of matter waves in an optical lattice", not "Optimal control of Bose-Einstein condensates in an optical lattice_" (PhD thesis, in English), Université de Toulouse, 2022. [theses.hal.science/tel-03997401v4](https://theses.hal.science/tel-03997401v4)

## Author

[Nathan Dupont](https://github.com/nyDupont) — PhD, Post Doc in quantum physics.
