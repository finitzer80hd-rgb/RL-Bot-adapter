@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Install Python 3.11+ from https://www.python.org/downloads/windows/
  echo Enable Add python.exe to PATH during setup.
  pause
  exit /b 1
)
py -m pip install --upgrade pip pyinstaller
if errorlevel 1 (echo Dependency install failed. & pause & exit /b 1)
py -m py_compile src\rlbot_adapter.py
if errorlevel 1 (echo Python syntax check failed. & pause & exit /b 1)
py -m PyInstaller --noconfirm --clean --onefile --windowed --name RLBotEpicAdapter src\rlbot_adapter.py
if errorlevel 1 (echo Build failed. & pause & exit /b 1)
echo Built dist\RLBotEpicAdapter.exe
pause
