@echo off
REM Double-click on Windows to launch Attention Tracker.
cd /d "%~dp0"
where py >nul 2>nul && (py -3 run.py & goto :end)
where python >nul 2>nul && (python run.py & goto :end)
echo Python 3 isn't installed. Get it from https://www.python.org/downloads/
:end
pause
