@echo off

cd /d "%~dp0"

if "%~1"=="" (
    echo File not specified.
    pause
    exit /b 1
) else (
    python VideoTimeCoder.py "%~1"
)

if %ERRORLEVEL% neq 0 pause