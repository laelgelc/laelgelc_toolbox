`build.ps1` is intended to be a PowerShell counterpart to Makefile. Task-for-task, it mirrors what Makefile does.

Here's the mapping:

- make help → .\build.ps1 -Target Help (or just .\build.ps1)
- make test → .\build.ps1 -Target Test
- make run-cli → .\build.ps1 -Target Run-Cli
- make run-gui → .\build.ps1 -Target Run-Gui
- make build-cli → .\build.ps1 -Target Build-Cli
- make build-gui → .\build.ps1 -Target Build-Gui
- make clean-build → .\build.ps1 -Target Clean-Build
- make clean-py → .\build.ps1 -Target Clean-Py
- make clean → .\build.ps1 -Target Clean

It also:

- Sets PYTHONPATH to src before running anything;
- Uses python, pytest, and pyinstaller in the same roles;
- Cleans build/, dist/, the two .spec files, and Python cache files recursively.
