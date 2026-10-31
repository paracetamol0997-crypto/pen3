@echo off
title Install DoubtDesk Offline Packages
cd /d "%~dp0"

echo =========================================================
echo      DoubtDesk - Offline Package Installer
echo =========================================================
echo.

set PY_CMD=
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 set PY_CMD=py
if "%PY_CMD%"=="" (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PY_CMD=python
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python is not found on this computer!
    echo Please install Python from python.org and check
    echo "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found:
%PY_CMD% --version
echo.

echo (Note: The project now already includes pre-extracted packages in the 'vendor' folder!)
echo Attempting optional pip install into your environment from local 'wheels' folder...
echo.

:: 1. Try installing pip/setuptools/wheel if missing
%PY_CMD% -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing pip from offline wheels...
    %PY_CMD% -m ensurepip --default-pip >nul 2>&1
)

:: 2. Try user install (avoids permission errors)
%PY_CMD% -m pip install --no-index --find-links=wheels --user -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying standard install without --user flag...
    %PY_CMD% -m pip install --no-index --find-links=wheels -r requirements.txt
)

echo.
echo =========================================================
echo  Setup complete! 
echo  You can simply double-click 'START_WEBSITE.bat' to launch!
echo =========================================================
echo.
pause
