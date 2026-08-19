@echo off
echo === Setting up virtual environment and installing dependencies (Windows) ===

if not exist .venv (
    echo [*] Creating virtual environment in .venv...
    python -m venv .venv
)

echo [*] Activating virtual environment...
call .venv\Scripts\activate

echo [*] Upgrading pip...
python -m pip install --upgrade pip

echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo [*] Running scripts\setup.py...
python scripts\setup.py

echo === Installation completed successfully! ===
echo To activate the virtual environment in CMD/PowerShell:
echo   .venv\Scripts\activate

pause