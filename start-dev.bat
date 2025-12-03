@echo off
echo ==========================================
echo QuickToolsHub 开发服务器启动
echo ==========================================
echo.

cd /d "%~dp0"

echo 检查Node.js...
node -v
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

echo.
echo 检查npm...
npm -v
if errorlevel 1 (
    echo 错误: 未找到npm，请先安装npm
    pause
    exit /b 1
)

echo.
echo 检查项目依赖...
if not exist "node_modules" (
    echo 正在安装依赖...
    call npm install
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo 启动开发服务器...
echo ==========================================
echo.
echo 服务器将在 http://localhost:3000 启动
echo.
echo 按 Ctrl+C 可以停止服务器
echo.
echo ==========================================
echo.

call npm run dev

pause

