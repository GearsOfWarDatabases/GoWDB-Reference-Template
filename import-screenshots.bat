@echo off
rem Imports new screenshots as shot-NNNN.jpg without metadata (see import-screenshots.py).
rem Add --dry-run to preview, or a folder to import from instead of SOURCE.
cd /d "%~dp0"
python import-screenshots.py %*
pause
