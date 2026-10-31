@echo off
title Student Doubt Portal - DoubtDesk
cd /d "%~dp0"

echo =========================================================
echo         Starting Student Doubt Portal (DoubtDesk)
echo =========================================================
echo.

:: Detect Python or Py launcher
set PY_CMD=
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 set PY_CMD=py
if "%PY_CMD%"=="" (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PY_CMD=python
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python is not installed or not in PATH on this laptop!
    echo.
    echo Please install Python (3.10, 3.11, or 3.12) from python.org
    echo and MAKE SURE to check "Add python.exe to PATH" during setup.
    echo.
    pause
    exit /b 1
)

:: Ensure vendor folder is available on PYTHONPATH as a fallback
set "PYTHONPATH=%~dp0vendor;%PYTHONPATH%"

echo [1/3] Preparing database...
%PY_CMD% manage.py migrate --noinput >nul 2>&1

echo [2/3] Checking demo subjects and accounts...
%PY_CMD% manage.py seed_data >nul 2>&1

echo [3/3] Launching DoubtDesk in your browser...
start http://127.0.0.1:8000/

echo.
echo =========================================================
echo   Server is running at: http://127.0.0.1:8000/
echo.
echo   Demo Accounts:
echo    - Student: 323136410112   ^| Password: 123456
echo    - Teacher: T101 (Maths)   ^| Password: teacher123
echo    - Teacher: T102 (CS)      ^| Password: teacher123
echo.
echo   (Keep this window open while using the website)
echo   Press Ctrl + C to stop the server anytime.
echo =========================================================
echo.

%PY_CMD% manage.py runserver 127.0.0.1:8000

pause
