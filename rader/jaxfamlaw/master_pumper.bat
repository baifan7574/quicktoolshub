@echo off
setlocal enabledelayedexpansion

:: ==========================================================
:: GRICH Master Pumper - 24/7 Zero-Failure Monitoring
:: ==========================================================

title GRICH Master Pumper

:LOOP
echo [%DATE% %TIME%] 🚀 Starting Intelligence Cycle...

:: 1. 运行关键词种子引擎 (CourtListener)
echo [%DATE% %TIME%] Step 1: Querying CourtListener for new cases...
python scripts/seed_engine_courtlistener.py
if %ERRORLEVEL% neq 0 (
    echo [!] Warning: Seed Engine exited with error %ERRORLEVEL%. Continuing...
)

echo [%DATE% %TIME%] ⏳ Brief rest before next step...
timeout /t 30 /nobreak > nul

:: 2. 运行律所 PDF 抓取引擎
echo [%DATE% %TIME%] Step 2: Pumping law firm websites for defendant lists...
python grich-astro/scripts/enhanced_lawfirm_pumper.py
if %ERRORLEVEL% neq 0 (
    echo [!] Warning: Lawfirm Pumper exited with error %ERRORLEVEL%. Continuing...
)

echo [%DATE% %TIME%] ✅ Cycle complete. Sleeping for 4 hours...
echo Next run at: 
:: 简单的下一次运行时间估算 (Windows CMD 下比较简陋)
echo [%DATE% %TIME%] (Scheduled every 4 hours)

:: 等待 14400 秒 (4小时)
timeout /t 14400 /nobreak

goto LOOP
