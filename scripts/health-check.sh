#!/bin/bash
# 网站健康检查脚本
# 检查所有功能和状态

set -e

echo "========================================="
echo "网站健康检查 - QuickToolsHub"
echo "========================================="
echo "检查时间: $(date)"
echo ""

cd /var/www/quicktoolshub

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
PASSED=0
FAILED=0
WARNING=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNING++))
}

# ========================================
# 1. 基础环境检查
# ========================================
echo "=== 1. 基础环境检查 ==="
echo ""

# PM2 状态
if pm2 list | grep -q "quicktoolshub.*online"; then
    UPTIME=$(pm2 jlist | grep -o '"pm_uptime":[0-9]*' | head -1 | cut -d: -f2)
    MEMORY=$(pm2 jlist | grep -o '"memory":[0-9]*' | head -1 | cut -d: -f2)
    MEMORY_MB=$((MEMORY / 1024 / 1024))
    check_pass "PM2 进程运行中 (运行时间: ${UPTIME}s, 内存: ${MEMORY_MB}MB)"
else
    check_fail "PM2 进程未运行"
fi

# Nginx 状态
if sudo systemctl is-active --quiet nginx; then
    check_pass "Nginx 服务运行中"
else
    check_fail "Nginx 服务未运行"
fi

# 构建目录
if [ -d ".next" ] && [ -f ".next/BUILD_ID" ]; then
    BUILD_ID=$(cat .next/BUILD_ID)
    check_pass "构建目录存在 (BUILD_ID: $BUILD_ID)"
else
    check_fail "构建目录不存在或构建不完整"
fi

echo ""

# ========================================
# 2. 应用访问检查
# ========================================
echo "=== 2. 应用访问检查 ==="
echo ""

# 本地访问
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    check_pass "本地访问正常 (HTTP $HTTP_CODE)"
else
    check_fail "本地访问失败 (HTTP $HTTP_CODE)"
fi

# 健康检查端点
HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/health 2>/dev/null || echo "")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    check_pass "健康检查端点正常"
    # 提取关键信息
    DB_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"database":{"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
    PM2_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"pm2":{"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
    echo "   数据库状态: $DB_STATUS"
    echo "   PM2 状态: $PM2_STATUS"
else
    check_fail "健康检查端点失败"
fi

# 静态资源访问
CSS_FILE=$(find .next/static -name "*.css" 2>/dev/null | head -1)
if [ -n "$CSS_FILE" ]; then
    CSS_PATH=$(echo "$CSS_FILE" | sed 's|\.next/static|/_next/static|')
    CSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$CSS_PATH" 2>/dev/null || echo "000")
    if [ "$CSS_CODE" = "200" ]; then
        check_pass "静态资源访问正常 (CSS: HTTP $CSS_CODE)"
    else
        check_fail "静态资源访问失败 (CSS: HTTP $CSS_CODE)"
    fi
else
    check_warn "未找到 CSS 文件"
fi

echo ""

# ========================================
# 3. Nginx 配置检查
# ========================================
echo "=== 3. Nginx 配置检查 ==="
echo ""

# 配置语法
if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
    check_pass "Nginx 配置语法正确"
else
    check_fail "Nginx 配置语法错误"
fi

# 静态资源配置
if sudo grep -q "location /_next/static/" /etc/nginx/sites-available/soeasyhub.com; then
    if sudo grep -A 5 "location /_next/static/" /etc/nginx/sites-available/soeasyhub.com | grep -q "proxy_pass"; then
        check_pass "静态资源代理配置正确"
    else
        check_fail "静态资源代理配置缺少 proxy_pass"
    fi
else
    check_fail "静态资源 location 配置不存在"
fi

# Gzip 配置
if sudo grep -q "gzip on" /etc/nginx/sites-available/soeasyhub.com; then
    check_pass "Gzip 压缩已启用"
else
    check_warn "Gzip 压缩未启用"
fi

echo ""

# ========================================
# 4. 依赖工具检查
# ========================================
echo "=== 4. 依赖工具检查 ==="
echo ""

# Ghostscript
if command -v gs &> /dev/null; then
    GS_VERSION=$(gs --version 2>/dev/null | head -1)
    check_pass "Ghostscript 已安装 ($GS_VERSION)"
else
    check_warn "Ghostscript 未安装 (PDF 压缩功能受限)"
fi

# API Keys
if [ -f ".env.production" ]; then
    if grep -q "REMOVE_BG_API_KEY" .env.production && ! grep "REMOVE_BG_API_KEY" .env.production | grep -qE "(your_|^REMOVE_BG_API_KEY=$)"; then
        check_pass "Remove.bg API Key 已配置"
    else
        check_warn "Remove.bg API Key 未配置 (背景移除功能不可用)"
    fi
    
    if grep -q "ERASE_BG_API_KEY" .env.production && ! grep "ERASE_BG_API_KEY" .env.production | grep -qE "(your_|^ERASE_BG_API_KEY=$)"; then
        check_pass "Erase.bg API Key 已配置"
    fi
else
    check_warn ".env.production 文件不存在"
fi

echo ""

# ========================================
# 5. 自动部署检查
# ========================================
echo "=== 5. 自动部署检查 ==="
echo ""

# 部署脚本
if [ -f "deploy.sh" ] && [ -x "deploy.sh" ]; then
    check_pass "部署脚本存在且可执行"
else
    check_warn "部署脚本不存在或不可执行"
fi

# 定时任务
CRON_JOB=$(crontab -l 2>/dev/null | grep quicktoolshub || echo "")
if [ -n "$CRON_JOB" ]; then
    INTERVAL=$(echo "$CRON_JOB" | grep -oE "\*/[0-9]+" | head -1 | cut -d/ -f2 || echo "unknown")
    check_pass "自动部署已配置 (检查间隔: 每${INTERVAL}分钟)"
else
    check_warn "自动部署未配置"
fi

echo ""

# ========================================
# 6. 资源使用检查
# ========================================
echo "=== 6. 资源使用检查 ==="
echo ""

# 内存使用
MEM_TOTAL=$(free -m | grep Mem | awk '{print $2}')
MEM_USED=$(free -m | grep Mem | awk '{print $3}')
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
if [ "$MEM_PERCENT" -lt 80 ]; then
    check_pass "内存使用正常 (${MEM_PERCENT}% / ${MEM_TOTAL}MB)"
else
    check_warn "内存使用较高 (${MEM_PERCENT}% / ${MEM_TOTAL}MB)"
fi

# 磁盘使用
DISK_USED=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USED" -lt 80 ]; then
    check_pass "磁盘使用正常 (${DISK_USED}%)"
else
    check_warn "磁盘使用较高 (${DISK_USED}%)"
fi

echo ""

# ========================================
# 7. 功能端点测试
# ========================================
echo "=== 7. API 端点检查 ==="
echo ""

# 健康检查
if curl -s http://localhost:3000/api/health | grep -q "healthy"; then
    check_pass "健康检查 API 正常"
else
    check_fail "健康检查 API 失败"
fi

# PDF 压缩 API（检查路由是否存在）
if curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:3000/api/compress-pdf 2>/dev/null | grep -qE "(400|413)"; then
    check_pass "PDF 压缩 API 路由正常"
else
    check_warn "PDF 压缩 API 路由可能有问题"
fi

# 背景移除 API（检查路由是否存在）
if curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:3000/api/remove-background 2>/dev/null | grep -qE "(400|413)"; then
    check_pass "背景移除 API 路由正常"
else
    check_warn "背景移除 API 路由可能有问题"
fi

echo ""

# ========================================
# 总结
# ========================================
echo "========================================="
echo "检查总结"
echo "========================================="
echo -e "${GREEN}✅ 通过: $PASSED${NC}"
echo -e "${YELLOW}⚠️  警告: $WARNING${NC}"
echo -e "${RED}❌ 失败: $FAILED${NC}"
echo ""

if [ "$FAILED" -eq 0 ]; then
    if [ "$WARNING" -eq 0 ]; then
        echo -e "${GREEN}🎉 网站状态：完全健康！${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  网站状态：基本正常，但有警告项${NC}"
        exit 0
    fi
else
    echo -e "${RED}❌ 网站状态：存在问题，需要修复${NC}"
    exit 1
fi

