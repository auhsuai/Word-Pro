@echo off
title Word Pro - Build System
echo ======================================================
echo   DANG MA HOA VA DONG GOI WORD PRO (PROTECTED)
echo ======================================================

echo [1/2] Dang ma hoa nguon bang PyArmor...
pyarmor gen -O obfuscated main.py logic.py auth.py data.py audio.py graph.py dialogs.py updater.py

echo.
echo [2/2] Dang build file EXE bang PyInstaller...
pyinstaller --noconfirm --onedir --windowed --icon "app_icon.ico" --name "WordPro" --paths "obfuscated" --collect-all customtkinter --collect-all ttkbootstrap --hidden-import data --hidden-import logic --hidden-import auth --hidden-import audio --hidden-import graph --hidden-import dialogs --hidden-import updater --add-data "app_icon.ico;." "obfuscated/main.py"

echo.
echo ======================================================
echo   BUILD HOAN TAT! 
echo   Bay gio hay vao Inno Setup va nhan Compile (Play)
echo ======================================================
pause
