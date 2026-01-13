@echo off
echo ====================================================
echo   Building Tkinter GUI Executable
echo ====================================================
echo.

python -m PyInstaller --onefile --name="EchoOfTheLastSystem-GUI" --windowed gui_tkinter.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo   BUILD COMPLETE!
echo ====================================================
echo.
echo Executable created: dist\EchoOfTheLastSystem-GUI.exe
echo.
pause
