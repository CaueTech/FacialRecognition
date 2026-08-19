#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

echo "=== Setting up virtual environment and installing dependencies ==="

# Check if system Python is >= 3.14 (TensorFlow requires Python <= 3.12/3.13)
if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 14) else 1)' 2>/dev/null; then
    echo "[!] Python $(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")') detected."
    echo "[*] Setting up Python 3.11 compatible virtual environment..."
    
    if [ ! -d ".venv" ] || [ ! -f ".venv/bin/python" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --quiet --upgrade pip uv
    uv python install 3.11
    uv venv .venv --python 3.11 --clear --seed
    source .venv/bin/activate
else
    if [ ! -d ".venv" ]; then
        echo "[*] Creating virtual environment in .venv..."
        python3 -m venv .venv
    fi
    source .venv/bin/activate
fi

echo "[*] Upgrading pip..."
pip install --quiet --upgrade pip

echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "[*] Running scripts/setup.py..."
python scripts/setup.py

echo "=== Installation completed successfully! ==="
echo "To activate the virtual environment in terminal, run:"
echo "  source .venv/bin/activate"