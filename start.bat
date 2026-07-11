@echo off
cd /d "%~dp0"
if not exist .venv (
  echo First-time setup: creating a virtual environment and installing dependencies...
  python -m venv .venv
  call .venv\Scripts\activate.bat
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)
if not exist .env (
  echo.
  echo No .env file found. Copy .env.example to .env and add your ANTHROPIC_API_KEY first.
  echo.
  pause
  exit /b 1
)
python app.py
pause
