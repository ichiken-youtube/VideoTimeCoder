@echo off
setlocal enabledelayedexpansion

:: バッチファイルのあるディレクトリに作業ディレクトリを変更
cd /d "%~dp0"

:: 引数（ドラッグ&ドロップされたファイルのパス）をチェック
if "%~1"=="" (
    echo File not specified.
    pause
    exit /b 1
) else (
    python VideoTimeCoder.py "%~1"
)

if %ERRORLEVEL% neq 0 pause