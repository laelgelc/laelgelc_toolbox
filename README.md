# Corpus Linguistics - Toolbox

This project is organised as a multi-phase pipeline.

## Repository layout

- src/cl/
  - common/
  - pdf_scrape/
- docs/
- data/
  - pdf_scrape/
- config/
- env/
- tests/
  - pdf_scrape/

## Phase 1 - PDF document scrapper
- Goal: Scrape PDF documents;
- Inputs: PDF documents in a folder;
- Outputs: Text files in a folder;
- Entry points: GUI app and CLI under src/cl/pdf_scrape/.

### PDF scraper usage

#### Input / output folders

By convention, sample data for Phase 1 lives under:

- `data/pdf_scrape/input/`  – example PDFs;
- `data/pdf_scrape/output/` – generated `.txt` files (optional, can also write alongside PDFs).

These folders are not required at runtime; you can point the tool at any file or directory.

#### CLI

Run the CLI from the project root (with your environment activated):

``` bash
python -m cl.pdf_scrape path\to\file_or_directory
```

Examples:

Single PDF → same folder, same name, .txt extension

``` bash
python -m cl.pdf_scrape data/pdf_scrape/input/example.pdf
```

All PDFs in a folder → .txt files alongside each PDF

``` bash
python -m cl.pdf_scrape data/pdf_scrape/input/
```

Write all outputs to a single folder

``` bash
python -m cl.pdf_scrape data/pdf_scrape/input/ -o data/pdf_scrape/output/
```

Overwrite existing .txt files

``` bash
python -m cl.pdf_scrape data/pdf_scrape/input/ --overwrite
```

To launch the GUI instead of the CLI:

``` bash
python -m cl.pdf_scrape --gui
```

#### GUI

The GUI offers:

- “Select PDF file(s)…” – choose one or more PDFs via file dialog;
- “Select folder…” – process all PDFs in a chosen folder;
- “Overwrite existing .txt” – checkbox to control overwrite behaviour;
- A log panel showing created / skipped / error status for each file.

#### Packaging with PyInstaller (Windows)

Once Phase 1 is stable, you can build standalone executables (from the project root):

``` bash
pyinstaller --onefile -n pdf_scrape_cli src/cl/pdf_scrape/cli.py pyinstaller --onefile -n pdf_scrape_gui --windowed src/cl/pdf_scrape/gui.py
```

This will produce:

- `dist/pdf_scrape_cli.exe` – command-line tool;
- `dist/pdf_scrape_gui.exe` – GUI application.

These executables can be distributed to users who do not have Python installed.
