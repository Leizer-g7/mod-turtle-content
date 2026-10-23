@echo off
rem Checks a 3.3.5 client against patch-y.mpq (read-only). Drag the client's Data folder onto this file,
rem or run it and paste the path.
setlocal
cd /d "%~dp0"
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY if exist "%USERPROFILE%\miniconda3\python.exe" set "PY=%USERPROFILE%\miniconda3\python.exe"
if not defined PY (
  echo Python was not found.
  pause
  exit /b 1
)
if "%~1"=="" (
  "%PY%" check_client.py
) else (
  "%PY%" check_client.py "%~1"
  pause
)
