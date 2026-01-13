@echo off
chcp 65001 >nul
cd /d "%~dp0"
python save_session_memory.py
pause
