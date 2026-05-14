@echo off
echo ========================================
echo MiKTeX Iranian Mirror Proxy - GUI
echo ========================================
echo.
echo Starting GUI application...
echo.

python miktex_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error starting GUI. Make sure Python and required libraries are installed.
    echo Run: pip install requests
    echo.
    pause
)
