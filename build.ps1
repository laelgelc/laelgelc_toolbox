param(
    [string]$Target = "Help"
)

# --- Configuration ----------------------------------------------------------

$PYTHON      = "python"
$PYTEST      = "pytest"
$PYINSTALLER = "pyinstaller"

# Ensure src/ is importable
$env:PYTHONPATH = "src"

# --- Tasks ------------------------------------------------------------------

function Invoke-Help {
    Write-Host "Available targets:"
    Write-Host "  Help        - Show this help message"
    Write-Host "  Test        - Run tests for pdf_scrape"
    Write-Host "  Run-Cli     - Run the CLI against data/pdf_scrape/input/"
    Write-Host "  Run-Gui     - Launch the GUI"
    Write-Host "  Build-Cli   - Build CLI executable with PyInstaller"
    Write-Host "  Build-Gui   - Build GUI executable with PyInstaller"
    Write-Host "  Clean-Build - Remove PyInstaller build artifacts (build/, dist/)"
    Write-Host "  Clean-Py    - Remove Python cache files (__pycache__, *.py[cod])"
    Write-Host "  Clean       - Clean-Build + Clean-Py"
}

function Invoke-Test {
    & $PYTHON -m $PYTEST "tests/pdf_scrape"
}

function Invoke-Run-Cli {
    & $PYTHON -m "cl.pdf_scrape" "data/pdf_scrape/input/"
}

function Invoke-Run-Gui {
    & $PYTHON -m "cl.pdf_scrape" "--gui"
}

function Invoke-Build-Cli {
    & $PYINSTALLER --onefile -n "pdf_scrape_cli" "src/cl/pdf_scrape/cli.py"
}

function Invoke-Build-Gui {
    & $PYINSTALLER --onefile --windowed -n "pdf_scrape_gui" "src/cl/pdf_scrape/gui.py"
}

function Invoke-Clean-Build {
    if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
    if (Test-Path "dist")  { Remove-Item "dist"  -Recurse -Force }
    if (Test-Path "pdf_scrape_cli.spec") { Remove-Item "pdf_scrape_cli.spec" -Force }
    if (Test-Path "pdf_scrape_gui.spec") { Remove-Item "pdf_scrape_gui.spec" -Force }
}

function Invoke-Clean-Py {
    Get-ChildItem -Recurse -Directory -Filter "__pycache__" |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

    Get-ChildItem -Recurse -Include *.pyc,*.pyo,*.pyd -File |
        Remove-Item -Force -ErrorAction SilentlyContinue
}

function Invoke-Clean {
    Invoke-Clean-Build
    Invoke-Clean-Py
}

# --- Dispatch ---------------------------------------------------------------

switch ($Target.ToLower()) {
    "help"        { Invoke-Help }
    "test"        { Invoke-Test }
    "run-cli"     { Invoke-Run-Cli }
    "run-gui"     { Invoke-Run-Gui }
    "build-cli"   { Invoke-Build-Cli }
    "build-gui"   { Invoke-Build-Gui }
    "clean-build" { Invoke-Clean-Build }
    "clean-py"    { Invoke-Clean-Py }
    "clean"       { Invoke-Clean }
    default {
        Write-Error "Unknown target '$Target'. Use: .\build.ps1 -Target Help"
        exit 1
    }
}