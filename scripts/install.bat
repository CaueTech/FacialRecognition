python -m venv .venv

call .venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

python scripts\setup.py

echo Instalação concluída.

pause