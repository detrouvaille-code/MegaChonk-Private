@echo off
cd /d "%~dp0"
set "GAME_PYTHON=python"
rem Prefer the installed interpreter over Windows' Store execution alias.
if exist "%LocalAppData%\Python\bin\python.exe" set "GAME_PYTHON=%LocalAppData%\Python\bin\python.exe"
"%GAME_PYTHON%" -c "import http.server" >nul 2>&1
if errorlevel 1 (
  echo Python could not start. Install Python or repair its Windows app alias.
  pause
  exit /b 1
)
"%GAME_PYTHON%" tools\serve_game.py %*
if errorlevel 1 pause
