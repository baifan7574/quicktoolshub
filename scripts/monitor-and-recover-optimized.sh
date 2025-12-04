#!/bin/bash
# 监控和自动恢复脚本（优化版 - 低资源消耗）
# 定期检查网站健康状态，发现问题自动修复

set -e

PROJECT_DIR="/var/www/quicktoolshub"
LOG_FILE="$PROJECT_DIR/logs/monitor.log"
MAX_RESTART_ATTEMPTS=3
RESTART_COUNT_FILE="$PROJECT_DIR/logs/restart_count.txt"
MAX_LOG_SIZE=10485760  # 10MB，超过则清理

# 日志函数（限制日志大小）
log() {
    # 检查日志文件大小，超过限制则清理
    if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]; then
        tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 获取重启次数
get_restart_count() {
    if [ -f "$RESTART_COUNT_FILE" ]; then
        cat "$RESTART_COUNT_FILE"
    else
        echo "0"
    fi
}

# 重置重启计数
reset_restart_count() {
    echo "0" > "$RESTART_COUNT_FILE"
}

# 增加重启计数
increment_restart_count() {
    local count=$(get_restart_count)
    echo $((count + 1)) > "$RESTART_COUNT_FILE"
}

cd "$PROJECT_DIR"

# 快速检查模式（只检查关键项，不执行恢复）
QUICK_CHECK=true

# ========================================
# 1. 快速检查 PM2 状态（轻量级）
# ========================================
PM2_STATUS=$(pm2 jlist 2>/dev/null | grep -o '"quicktoolshub".*"status":"[^"]*"' | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")

if [ "$PM2_STATUS" != "online" ]; then
    log "⚠️ PM2 进程状态异常: $PM2_STATUS"
    QUICK_CHECK=false
    
    # 检查重启次数
    RESTART_COUNT=$(get_restart_count)
    if [ "$RESTART_COUNT" -ge "$MAX_RESTART_ATTEMPTS" ]; then
        log "❌ 已达到最大重启次数 ($MAX_RESTART_ATTEMPTS)，停止自动重启"
        exit 1
    fi
    
    log "触发自动恢复..."
    increment_restart_count
    "$PROJECT_DIR/scripts/auto-recovery.sh" >/dev/null 2>&1
    
    if pm2 list | grep -q "quicktoolshub.*online"; then
        reset_restart_count
        log "✅ 恢复成功"
    fi
    exit 0
fi

# ========================================
# 2. 快速检查应用访问（轻量级，超时5秒）
# ========================================
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 --connect-timeout 3 http://localhost:3000 2>/dev/null || echo "000")

if [ "$HTTP_CODE" != "200" ]; then
    log "⚠️ 应用无法访问 (HTTP $HTTP_CODE)"
    QUICK_CHECK=false
    
    RESTART_COUNT=$(get_restart_count)
    if [ "$RESTART_COUNT" -lt "$MAX_RESTART_ATTEMPTS" ]; then
        log "触发自动恢复..."
        increment_restart_count
        "$PROJECT_DIR/scripts/auto-recovery.sh" >/dev/null 2>&1
    else
        log "❌ 已达到最大重启次数"
    fi
    exit 0
fi

# ========================================
# 3. 快速检查构建完整性（轻量级）
# ========================================
if [ ! -f ".next/BUILD_ID" ]; then
    log "⚠️ 构建不完整，触发自动恢复..."
    QUICK_CHECK=false
    "$PROJECT_DIR/scripts/auto-recovery.sh" >/dev/null 2>&1
    exit 0
fi

# ========================================
# 4. 如果所有检查都通过，只记录一次（减少日志）
# ========================================
if [ "$QUICK_CHECK" = "true" ]; then
    # 只在每小时记录一次正常状态（减少日志量）
    LAST_CHECK_FILE="$PROJECT_DIR/logs/last_check.txt"
    LAST_CHECK=$(cat "$LAST_CHECK_FILE" 2>/dev/null || echo "0")
    CURRENT_TIME=$(date +%s)
    
    # 如果距离上次记录超过1小时，才记录
    if [ $((CURRENT_TIME - LAST_CHECK)) -gt 3600 ]; then
        log "✅ 所有检查通过（正常状态）"
        echo "$CURRENT_TIME" > "$LAST_CHECK_FILE"
    fi
fi

# 重置重启计数（如果一切正常）
reset_restart_count

