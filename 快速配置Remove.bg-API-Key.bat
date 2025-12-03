@echo off
chcp 65001 >nul
echo ========================================
echo 配置 Remove.bg API Key
echo ========================================
echo.

set /p API_KEY="请输入你的 Remove.bg API Key: "

if "%API_KEY%"=="" (
    echo.
    echo 错误：API Key 不能为空
    pause
    exit /b 1
)

echo.
echo 正在更新 .env.local 文件...

REM 检查文件是否存在
if not exist .env.local (
    echo # QuickToolsHub 环境变量配置 > .env.local
    echo. >> .env.local
)

REM 检查是否已存在 REMOVE_BG_API_KEY
findstr /C:"REMOVE_BG_API_KEY" .env.local >nul 2>&1
if %errorlevel% equ 0 (
    echo 发现已存在的 REMOVE_BG_API_KEY，正在更新...
    powershell -Command "(Get-Content .env.local) -replace 'REMOVE_BG_API_KEY=.*', 'REMOVE_BG_API_KEY=%API_KEY%' | Set-Content .env.local"
) else (
    echo 添加新的 REMOVE_BG_API_KEY...
    echo. >> .env.local
    echo # Remove.bg API Key（服务器端使用） >> .env.local
    echo REMOVE_BG_API_KEY=%API_KEY% >> .env.local
)

echo.
echo ✅ API Key 配置完成！
echo.
echo 请重启开发服务器（停止后重新运行 npm run dev）
echo.
pause

