@echo off
echo ====================================================
echo   Building Both Executables
echo ====================================================
echo.

echo Building CLI version...
python -m PyInstaller --onefile --name="EchoOfTheLastSystem-CLI" --console main.py

echo.
echo Building GUI version...
python -m PyInstaller --onefile --name="EchoOfTheLastSystem-GUI" --windowed gui_tkinter.py

echo.
echo ====================================================
echo   BUILD COMPLETE!
echo ====================================================
echo.
echo Executables created in: dist\
echo   - EchoOfTheLastSystem-CLI.exe
echo   - EchoOfTheLastSystem-GUI.exe
echo.
pause
