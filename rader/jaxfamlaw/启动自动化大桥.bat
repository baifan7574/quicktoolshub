@echo off
chcp 65001 >nul
echo ==========================================
echo   GRICH 自动化大桥 - 启动助手 (永久版)
echo ==========================================

:: 切换到脚本所在目录
cd /d "%~dp0"

echo [1/2] 正在检测并清理旧进程...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM cloudflared_386.exe /T >nul 2>&1

echo [2/2] 正在启动 n8n 引擎 (新窗口)...
start "n8n 引擎" cmd /k "npx n8n start"

echo [3/2] 正在拉起 Cloudflare 永久隧道 (n8n.jaxfamlaw.com)...
.\cloudflared_386.exe tunnel run --token eyJhIjoiYzcwZjI5MWI3N2ZiYzAyYTZmMjA5MGViZTRhYmRkNDQiLCJ0IjoiMzM0NmE0NDAtN2MxNS00MzIwLTgzMDktYTA1OGRmOGFkZDk2IiwicyI6IlkyVTBOakk1TnpNdE56WTBOQzAwWTJZMExUazROREF0TXpVME56Sm1NREF5T0RneCJ9

pause
