@echo off
setlocal
cd /d "%~dp0"
if exist "%LocalAppData%\Python\pythoncore-3.14-64\python.exe" (
  "%LocalAppData%\Python\pythoncore-3.14-64\python.exe" preview.py
) else (
  py -3 preview.py
)
if errorlevel 1 (
  echo Python is needed for this viewer. You can open tactical-tabby.blend in Blender instead.
  pause
)
