# Makefile for laelgelc_toolbox
# Basic tasks for Phase 1: tests, running, and PyInstaller builds.

PYTHON := python
PYTEST := pytest
PYINSTALLER := pyinstaller

# --- Helpers -------------------------------------------------------------

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  help           - Show this help message"
	@echo "  test           - Run tests for pdf_scrape"
	@echo "  run-cli        - Run the CLI against data/pdf_scrape/input/"
	@echo "  run-gui        - Launch the GUI"
	@echo "  build-cli      - Build CLI executable with PyInstaller"
	@echo "  build-gui      - Build GUI executable with PyInstaller"
	@echo "  clean-build    - Remove PyInstaller build artifacts (build/, dist/)"
	@echo "  clean-py       - Remove Python cache files (__pycache__, *.py[cod])"
	@echo "  clean          - clean-build + clean-py"

# --- Testing -------------------------------------------------------------

.PHONY: test
test:
	$(PYTHON) -m $(PYTEST) tests/pdf_scrape

# --- Running (development) ----------------------------------------------

.PHONY: run-cli
run-cli:
	$(PYTHON) -m cl.pdf_scrape data/pdf_scrape/input/

.PHONY: run-gui
run-gui:
	$(PYTHON) -m cl.pdf_scrape --gui

# --- PyInstaller builds -------------------------------------------------

# Note: assumes PyInstaller is installed in the active environment.
# Outputs will be in dist/pdf_scrape_cli(.exe) and dist/pdf_scrape_gui(.exe)

.PHONY: build-cli
build-cli:
	$(PYINSTALLER) --onefile -n pdf_scrape_cli src/cl/pdf_scrape/cli.py

.PHONY: build-gui
build-gui:
	$(PYINSTALLER) --onefile --windowed -n pdf_scrape_gui src/cl/pdf_scrape/gui.py

# --- Cleaning -----------------------------------------------------------

.PHONY: clean-build
clean-build:
	@if [ -d "build" ]; then rm -rf build; fi
	@if [ -d "dist" ]; then rm -rf dist; fi
	@if [ -f "pdf_scrape_cli.spec" ]; then rm -f pdf_scrape_cli.spec; fi
	@if [ -f "pdf_scrape_gui.spec" ]; then rm -f pdf_scrape_gui.spec; fi

.PHONY: clean-py
clean-py:
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} \; 2>/dev/null || true
	@find . -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) -delete 2>/dev/null || true

.PHONY: clean
clean: clean-build clean-py