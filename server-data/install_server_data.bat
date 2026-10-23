@echo off
rem ============================================================
rem  mod-turtle-content - rebuild maps / vmaps / mmaps for the Turtle terrain
rem  and install them into Acore Data (asks first, backs up first).
rem ============================================================
setlocal
cd /d "%~dp0"
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY if exist "%USERPROFILE%\miniconda3\python.exe" set "PY=%USERPROFILE%\miniconda3\python.exe"
if not defined PY if exist "%USERPROFILE%\anaconda3\python.exe" set "PY=%USERPROFILE%\anaconda3\python.exe"
if not defined PY (
  echo Python was not found. Install it from python.org or edit the PY line in this file.
  pause
  exit /b 1
)
"%PY%" install_server_data.py %*
