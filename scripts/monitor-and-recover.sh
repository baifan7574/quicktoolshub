#!/bin/bash
# 监控和自动恢复脚本
# 定期检查网站健康状态，发现问题自动修复

set -e

PROJECT_DIR="/var/www/quicktoolshub"
LOG_FILE="$PROJECT_DIR/logs/monitor.log"
MAX_RESTART_ATTEMPTS=3
RESTART_COUNT_FILE="$PROJECT_DIR/logs/restart_count.txt"

# 日志函数
log() {
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

log "========================================="
log "监控检查开始"
log "========================================="

# ========================================
# 1. 基础检查
# ========================================
log "1. 检查 PM2 进程..."
PM2_STATUS=$(pm2 jlist 2>/dev/null | grep -o '"quicktoolshub".*"status":"[^"]*"' | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")

if [ "$PM2_STATUS" != "online" ]; then
    log "⚠️ PM2 进程状态异常: $PM2_STATUS"
    
    # 检查重启次数
    RESTART_COUNT=$(get_restart_count)
    if [ "$RESTART_COUNT" -ge "$MAX_RESTART_ATTEMPTS" ]; then
        log "❌ 已达到最大重启次数 ($MAX_RESTART_ATTEMPTS)，停止自动重启"
        log "请手动检查问题"
        exit 1
    fi
    
    log "尝试重启应用 (第 $((RESTART_COUNT + 1)) 次)..."
    increment_restart_count
    
    # 执行自动恢复
    "$PROJECT_DIR/scripts/auto-recovery.sh"
    
    # 如果恢复成功，重置计数
    if pm2 list | grep -q "quicktoolshub.*online"; then
        reset_restart_count
        log "✅ 恢复成功，重置重启计数"
    fi
else
    log "✅ PM2 进程正常"
    reset_restart_count
fi

# ========================================
# 2. 应用访问检查
# ========================================
log "2. 检查应用访问..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000 2>/dev/null || echo "000")

if [ "$HTTP_CODE" != "200" ]; then
    log "⚠️ 应用无法访问 (HTTP $HTTP_CODE)"
    
    RESTART_COUNT=$(get_restart_count)
    if [ "$RESTART_COUNT" -lt "$MAX_RESTART_ATTEMPTS" ]; then
        log "尝试自动恢复..."
        increment_restart_count
        "$PROJECT_DIR/scripts/auto-recovery.sh"
    else
        log "❌ 已达到最大重启次数，停止自动恢复"
    fi
else
    log "✅ 应用访问正常 (HTTP $HTTP_CODE)"
fi

# ========================================
# 3. 构建完整性检查
# ========================================
log "3. 检查构建完整性..."
if [ ! -f ".next/BUILD_ID" ]; then
    log "⚠️ 构建不完整，触发自动恢复..."
    "$PROJECT_DIR/scripts/auto-recovery.sh"
else
    log "✅ 构建完整"
fi

# ========================================
# 4. 资源使用检查
# ========================================
log "4. 检查资源使用..."
MEM_USED=$(free -m | grep Mem | awk '{print $3}')
MEM_TOTAL=$(free -m | grep Mem | awk '{print $2}')
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))

if [ "$MEM_PERCENT" -gt 90 ]; then
    log "⚠️ 内存使用过高 (${MEM_PERCENT}%)，清理缓存..."
    npm cache clean --force 2>/dev/null || true
    find /var/www -name ".cache" -type d -exec rm -rf {} + 2>/dev/null || true
    log "✅ 缓存已清理"
else
    log "✅ 内存使用正常 (${MEM_PERCENT}%)"
fi

log "========================================="
log "监控检查完成"
log "========================================="

