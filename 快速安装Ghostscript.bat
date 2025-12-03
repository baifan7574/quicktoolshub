@echo off
chcp 65001 >nul
echo ========================================
echo Ghostscript 自动安装脚本
echo ========================================
echo.

echo 正在下载 Ghostscript 安装程序...
echo 这可能需要几分钟，请耐心等待...
echo.

powershell -ExecutionPolicy Bypass -Command "$ProgressPreference = 'SilentlyContinue'; $url = 'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs1000/gs1000w64.exe'; $output = 'gs-installer.exe'; try { Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing; Write-Host '下载完成！' -ForegroundColor Green } catch { Write-Host '下载失败: ' $_.Exception.Message -ForegroundColor Red; exit 1 }"

if not exist gs-installer.exe (
    echo.
    echo 错误：下载失败
    echo 请手动下载：https://www.ghostscript.com/download/gsdnld.html
    pause
    exit /b 1
)

echo.
echo 正在启动安装程序（需要管理员权限）...
echo 请按照安装向导完成安装...
echo.

start /wait "" gs-installer.exe /S

echo.
echo 安装完成！
echo.
echo 正在验证安装...

timeout /t 2 /nobreak >nul

gs --version >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ✅ Ghostscript 安装成功！
    gs --version
) else (
    echo.
    echo ⚠️  安装可能已完成，但需要重启终端才能使用
    echo 请关闭并重新打开终端，然后运行 'gs --version' 验证
)

echo.
echo 清理安装程序...
del gs-installer.exe >nul 2>&1

echo.
echo 完成！
pause

