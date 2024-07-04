@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set PACKAGE_DIR=%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_*
set BIN_DIR=ffmpeg-*-full_build
set MATCH=

if not exist "!PACKAGE_DIR!" (
    echo 検索ディレクトリが存在しません。
    pause
    rem exit /b 1
)

for /d %%G in ("!PACKAGE_DIR!") do (
    if not defined MATCH (
        set MATCH=%%G
    )
)

for /d %%G in (!MATCH!\!BIN_DIR!) do (
    set MATCH=%%G\bin
)

if defined MATCH (
    echo Add the following to PATH : !MATCH!
    set PATH=!PATH!;!MATCH!
    if "%~1"=="" (
        echo File not specified.
        pause
        exit /b 1
    ) else (
        python VideoTimeCoder.py "%~1"
    )
) else (
    echo Not matched
)

endlocal
if %ERRORLEVEL% neq 0 pause