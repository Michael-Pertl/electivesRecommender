@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_LAUNCHER=py"

where py >nul 2>&1
if errorlevel 1 (
  where python >nul 2>&1
  if errorlevel 1 goto :error
  set "PYTHON_LAUNCHER=python"
)

echo Starting prototype at http://localhost:8600/
echo Press Ctrl+C to stop the server.
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8600/"
%PYTHON_LAUNCHER% -m http.server 8600 --bind 127.0.0.1
exit /b %errorlevel%

:error
echo Launch failed: Python was not found. Install Python and try again.
pause
exit /b 1
