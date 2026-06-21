@echo off
setlocal

cd /d "%~dp0"

set "VENV_DIR=.venv-win"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
set "PYTHON_LAUNCHER=py"

where py >nul 2>&1
if errorlevel 1 set "PYTHON_LAUNCHER=python"

if not exist "%PYTHON_EXE%" (
  echo Creating virtual environment...
  %PYTHON_LAUNCHER% -m venv "%VENV_DIR%"
  if errorlevel 1 goto :error
)

"%PYTHON_EXE%" -c "import streamlit, pandas, sklearn, numpy" >nul 2>&1
if errorlevel 1 (
  echo Installing dependencies...
  "%PYTHON_EXE%" -m pip install -r requirements.txt
  if errorlevel 1 goto :error
)

echo Starting demo at http://localhost:8501
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run app.py --server.headless true --server.port 8501 --browser.gatherUsageStats false
exit /b %errorlevel%

:error
echo Launch failed.
exit /b 1
