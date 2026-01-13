@echo off
chcp 65001 >nul
cd /d "%~dp0"
python talk_to_cto.py %*
pause
