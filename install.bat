@echo off
echo ========================================
echo ChatBook IA - Installation
echo ========================================
echo.
echo Installing required packages...
echo.

pip install customtkinter==5.2.1
pip install Pillow==10.1.0
pip install google-generativeai==0.3.2
pip install python-dotenv==1.0.0

echo.
echo ========================================
echo Installation complete!
echo.
echo To run the application:
echo python main.py
echo ========================================
pause
