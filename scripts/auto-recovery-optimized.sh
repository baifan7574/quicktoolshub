#!/bin/bash
# 自动恢复脚本（优化版 - 低资源消耗）
# 检测网站问题并自动修复

set -e

LOG_FILE="/var/www/quicktoolshub/logs/auto-recovery.log"
PROJECT_DIR="/var/www/quicktoolshub"
MAX_LOG_SIZE=10485760  # 10MB

# 日志函数（限制日志大小）
log() {
    # 检查日志文件大小，超过限制则清理
    if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]; then
        tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$PROJECT_DIR"

log "自动恢复开始"

# ========================================
# 1. 检查应用是否运行（快速检查）
# ========================================
if ! pm2 list | grep -q "quicktoolshub.*online"; then
    log "应用未运行，重启..."
    pm2 restart quicktoolshub || pm2 start ecosystem.config.js
    sleep 3  # 减少等待时间
    if pm2 list | grep -q "quicktoolshub.*online"; then
        log "✅ 应用已重启"
        exit 0
    fi
fi

# ========================================
# 2. 检查应用访问（快速检查，超时5秒）
# ========================================
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 --connect-timeout 3 http://localhost:3000 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
    log "应用无法访问 (HTTP $HTTP_CODE)，重启..."
    pm2 restart quicktoolshub
    sleep 5  # 减少等待时间
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log "✅ 应用已恢复"
        exit 0
    fi
fi

# ========================================
# 3. 检查构建完整性（只在必要时重新构建）
# ========================================
if [ ! -f ".next/BUILD_ID" ]; then
    log "构建不完整，开始重新构建..."
    
    pm2 stop quicktoolshub
    
    # 只清理必要的文件
    rm -rf .next
    # 不清理 node_modules/.cache（节省时间）
    
    log "构建中（使用最小内存限制）..."
    NODE_OPTIONS="--max-old-space-size=512" npm run build >/dev/null 2>&1
    
    if [ -f ".next/BUILD_ID" ]; then
        BUILD_ID=$(cat .next/BUILD_ID)
        log "✅ 构建完成 (BUILD_ID: $BUILD_ID)"
    else
        log "❌ 构建失败"
        pm2 start quicktoolshub || true
        exit 1
    fi
    
    pm2 start quicktoolshub
    sleep 5  # 减少等待时间
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log "✅ 应用已恢复并正常运行"
    else
        log "❌ 应用仍无法访问"
        exit 1
    fi
fi

log "✅ 所有检查通过"

