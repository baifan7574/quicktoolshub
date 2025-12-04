#!/bin/bash
# 全面检查和验证脚本
# 检查所有功能、优化和配置

set -e

echo "========================================="
echo "全面检查和验证 - QuickToolsHub"
echo "========================================="
echo ""

cd /var/www/quicktoolshub

# ========================================
# 第一部分：基础环境检查
# ========================================
echo "=== 第一部分：基础环境检查 ==="
echo ""

echo "1. 检查 Node.js 版本："
node --version
echo ""

echo "2. 检查 npm 版本："
npm --version
echo ""

echo "3. 检查 PM2 状态："
pm2 list
echo ""

echo "4. 检查 Nginx 状态："
sudo systemctl status nginx --no-pager | head -5
echo ""

echo "5. 检查磁盘空间："
df -h / | tail -1
echo ""

echo "6. 检查内存使用："
free -h | grep Mem
echo ""

# ========================================
# 第二部分：代码和构建检查
# ========================================
echo "=== 第二部分：代码和构建检查 ==="
echo ""

echo "7. 检查 Git 状态："
git status --short | head -10 || echo "无未提交更改"
echo ""

echo "8. 检查最新提交："
git log -1 --oneline
echo ""

echo "9. 检查构建目录："
if [ -d ".next" ]; then
    echo "✅ .next 目录存在"
    ls -la .next/BUILD_ID 2>/dev/null && echo "✅ BUILD_ID 存在" || echo "❌ BUILD_ID 不存在"
    find .next/static -name "*.css" 2>/dev/null | head -1 && echo "✅ CSS 文件存在" || echo "❌ CSS 文件不存在"
else
    echo "❌ .next 目录不存在，需要构建"
fi
echo ""

echo "10. 检查配置文件："
[ -f "next.config.ts" ] && echo "✅ next.config.ts 存在" || echo "❌ next.config.ts 不存在"
[ -f "ecosystem.config.js" ] && echo "✅ ecosystem.config.js 存在" || echo "❌ ecosystem.config.js 不存在"
[ -f ".env.production" ] && echo "✅ .env.production 存在" || echo "⚠️ .env.production 不存在（可能正常）"
echo ""

# ========================================
# 第三部分：应用功能检查
# ========================================
echo "=== 第三部分：应用功能检查 ==="
echo ""

echo "11. 检查应用是否运行："
if pm2 list | grep -q "quicktoolshub.*online"; then
    echo "✅ 应用正在运行"
    APP_PID=$(pm2 jlist | grep -o '"pid":[0-9]*' | head -1 | cut -d: -f2)
    echo "   进程 ID: $APP_PID"
else
    echo "❌ 应用未运行"
fi
echo ""

echo "12. 测试本地访问："
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ 本地访问正常 (HTTP 200)"
else
    echo "❌ 本地访问失败"
fi
echo ""

echo "13. 测试健康检查端点："
HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/health 2>/dev/null)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ 健康检查正常"
    echo "$HEALTH_RESPONSE" | head -3
else
    echo "❌ 健康检查失败"
fi
echo ""

echo "14. 测试静态资源访问："
CSS_FILE=$(find .next/static -name "*.css" 2>/dev/null | head -1)
if [ -n "$CSS_FILE" ]; then
    CSS_PATH=$(echo "$CSS_FILE" | sed 's|\.next/static|/_next/static|')
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$CSS_PATH" | grep -q "200"; then
        echo "✅ 静态资源访问正常"
    else
        echo "❌ 静态资源访问失败: $CSS_PATH"
    fi
else
    echo "⚠️ 未找到 CSS 文件"
fi
echo ""

# ========================================
# 第四部分：Nginx 配置检查
# ========================================
echo "=== 第四部分：Nginx 配置检查 ==="
echo ""

echo "15. 检查 Nginx 配置语法："
if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
    echo "✅ Nginx 配置语法正确"
else
    echo "❌ Nginx 配置有错误"
    sudo nginx -t
fi
echo ""

echo "16. 检查 Nginx 静态资源配置："
if sudo grep -q "location /_next/static/" /etc/nginx/sites-available/soeasyhub.com; then
    echo "✅ /_next/static/ location 存在"
    if sudo grep -A 5 "location /_next/static/" /etc/nginx/sites-available/soeasyhub.com | grep -q "proxy_pass"; then
        echo "✅ proxy_pass 配置存在"
    else
        echo "❌ proxy_pass 配置缺失"
    fi
else
    echo "❌ /_next/static/ location 不存在"
fi
echo ""

echo "17. 检查 Nginx Gzip 配置："
if sudo grep -q "gzip on" /etc/nginx/sites-available/soeasyhub.com; then
    echo "✅ Gzip 已启用"
else
    echo "❌ Gzip 未启用"
fi
echo ""

# ========================================
# 第五部分：依赖和工具检查
# ========================================
echo "=== 第五部分：依赖和工具检查 ==="
echo ""

echo "18. 检查 Ghostscript（PDF 压缩）："
if command -v gs &> /dev/null; then
    echo "✅ Ghostscript 已安装"
    gs --version | head -1
else
    echo "⚠️ Ghostscript 未安装（PDF 压缩功能可能受限）"
fi
echo ""

echo "19. 检查 Remove.bg API Key："
if [ -f ".env.production" ]; then
    if grep -q "REMOVE_BG_API_KEY" .env.production && ! grep "REMOVE_BG_API_KEY" .env.production | grep -q "your_"; then
        echo "✅ Remove.bg API Key 已配置"
    else
        echo "⚠️ Remove.bg API Key 未配置（背景移除功能不可用）"
    fi
    if grep -q "ERASE_BG_API_KEY" .env.production && ! grep "ERASE_BG_API_KEY" .env.production | grep -q "your_"; then
        echo "✅ Erase.bg API Key 已配置"
    fi
else
    echo "⚠️ .env.production 不存在"
fi
echo ""

# ========================================
# 第六部分：自动部署检查
# ========================================
echo "=== 第六部分：自动部署检查 ==="
echo ""

echo "20. 检查自动部署脚本："
if [ -f "deploy.sh" ]; then
    echo "✅ deploy.sh 存在"
    if [ -x "deploy.sh" ]; then
        echo "✅ deploy.sh 可执行"
    else
        echo "⚠️ deploy.sh 不可执行"
    fi
else
    echo "❌ deploy.sh 不存在"
fi
echo ""

echo "21. 检查自动部署定时任务："
CRON_JOB=$(crontab -l 2>/dev/null | grep quicktoolshub || echo "")
if [ -n "$CRON_JOB" ]; then
    echo "✅ 定时任务已配置"
    echo "   $CRON_JOB"
else
    echo "⚠️ 定时任务未配置"
fi
echo ""

# ========================================
# 第七部分：性能优化检查
# ========================================
echo "=== 第七部分：性能优化检查 ==="
echo ""

echo "22. 检查 PM2 配置："
if [ -f "ecosystem.config.js" ]; then
    if grep -q "max_memory_restart" ecosystem.config.js; then
        echo "✅ PM2 内存限制已配置"
    else
        echo "⚠️ PM2 内存限制未配置"
    fi
else
    echo "❌ ecosystem.config.js 不存在"
fi
echo ""

echo "23. 检查 Nginx 缓存配置："
if sudo grep -q "expires 1y" /etc/nginx/sites-available/soeasyhub.com; then
    echo "✅ 静态文件缓存已配置"
else
    echo "⚠️ 静态文件缓存未配置"
fi
echo ""

# ========================================
# 第八部分：安全检查
# ========================================
echo "=== 第八部分：安全检查 ==="
echo ""

echo "24. 检查防火墙状态："
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status | head -1)
    echo "$UFW_STATUS"
    if echo "$UFW_STATUS" | grep -q "active"; then
        echo "✅ 防火墙已启用"
    else
        echo "⚠️ 防火墙未启用"
    fi
else
    echo "⚠️ UFW 未安装"
fi
echo ""

# ========================================
# 总结
# ========================================
echo "========================================="
echo "检查完成"
echo "========================================="
echo ""
echo "如果发现任何 ❌ 或 ⚠️，请根据提示修复"
echo ""

