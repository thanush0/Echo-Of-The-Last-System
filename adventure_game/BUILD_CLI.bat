@echo off
echo ====================================================
echo   Building CLI Executable
echo ====================================================
echo.

python -m PyInstaller --onefile --name="EchoOfTheLastSystem-CLI" --console main.py

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
echo Executable created: dist\EchoOfTheLastSystem-CLI.exe
echo.
pause
