@echo off
echo ============================================
echo   BUILD RECHARGE MANAGER - VERSION 1.0
echo ============================================
echo.

echo [1/3] Nettoyage...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo [2/3] Compilation (patiente 2-5 min)...
python -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "RechargeManager" ^
    --add-data "data;data" ^
    --collect-all PySide6 ^
    main.py

echo [3/3] Copie data a cote de l'exe...
if not exist "dist" mkdir "dist"
if not exist "dist\data" mkdir "dist\data"
if not exist "dist\data\logos" mkdir "dist\data\logos"

xcopy /E /I /Y "data\logos" "dist\data\logos" >nul
if exist "data\recharge.db" copy "data\recharge.db" "dist\data\" >nul

echo.
echo ============================================
echo   BUILD TERMINE !
echo ============================================
echo.
echo Ton exe : dist\RechargeManager.exe
echo.
echo IMPORTANT : garde le dossier 'data' a cote de l'exe !
echo.
pause