@echo off
chcp 65001 >nul
echo ========================================
echo 自动化内容营销 - 快速开始
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查依赖...
pip show openai >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已安装
)

echo.
echo [2/4] 检查配置文件...
if not exist ".env" (
    echo [警告] 未找到 .env 文件
    echo 请复制 config/env.example 为 .env 并填写配置
    echo.
    echo 必需配置：
    echo   - SUPABASE_URL
    echo   - SUPABASE_SERVICE_KEY
    echo   - OPENAI_API_KEY 或 ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
) else (
    echo 配置文件已存在
)

echo.
echo [3/4] 检查数据目录...
if not exist "..\data" mkdir "..\data"
if not exist "..\data\keywords-raw" mkdir "..\data\keywords-raw"
if not exist "..\data\keywords-processed" mkdir "..\data\keywords-processed"
if not exist "..\data\articles-generated" mkdir "..\data\articles-generated"
echo 数据目录已准备

echo.
echo [4/4] 准备完成！
echo.
echo 下一步：
echo   1. 将你的关键词数据放到 ..\data\keywords-raw\ 目录
echo   2. 运行: python batch-processor.py ..\data\keywords-raw\keywords.csv --max 10
echo   3. 检查生成的文章质量
echo   4. 满意后运行: python batch-processor.py ..\data\keywords-raw\keywords.csv --max 50 --publish
echo.
pause

