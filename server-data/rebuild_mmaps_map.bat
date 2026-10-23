@echo off
rem ============================================================
rem  mod-turtle-content - rebuild the mmaps of whole maps whose buildings changed (default: 36, the Deadmines)
rem  Run after install_server_data.bat, worldserver stopped (asks first, backs up first).
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
"%PY%" rebuild_mmaps_map.py %*
