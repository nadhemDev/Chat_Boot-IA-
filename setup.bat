@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install customtkinter Pillow google-generativeai python-dotenv

echo.
echo Setup complete!
echo To run the application:
echo 1. Activate venv: venv\Scripts\activate
echo 2. Run: python main.py
echo ========================================
pause
