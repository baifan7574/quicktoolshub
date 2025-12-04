#!/bin/bash
# 自动恢复脚本
# 检测网站问题并自动修复

set -e

LOG_FILE="/var/www/quicktoolshub/logs/auto-recovery.log"
PROJECT_DIR="/var/www/quicktoolshub"
MAX_LOG_SIZE=10485760  # 10MB，超过则清理

# 日志函数（限制日志大小，减少磁盘消耗）
log() {
    # 检查日志文件大小，超过限制则清理（只保留最近500行）
    if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]; then
        tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========================================="
log "自动恢复检查开始"
log "========================================="

cd "$PROJECT_DIR"

# ========================================
# 1. 检查应用是否运行
# ========================================
log "检查 PM2 进程状态..."
if ! pm2 list | grep -q "quicktoolshub.*online"; then
    log "⚠️ 应用未运行，尝试重启..."
    pm2 restart quicktoolshub || pm2 start ecosystem.config.js
    sleep 5
    if pm2 list | grep -q "quicktoolshub.*online"; then
        log "✅ 应用已重启"
    else
        log "❌ 应用启动失败，需要手动检查"
        exit 1
    fi
else
    log "✅ 应用正在运行"
fi

# ========================================
# 2. 检查应用访问
# ========================================
log "检查应用访问..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
    log "⚠️ 应用无法访问 (HTTP $HTTP_CODE)，尝试重启..."
    pm2 restart quicktoolshub
    sleep 5  # 减少等待时间
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log "✅ 应用已恢复"
    else
        log "❌ 应用仍无法访问，检查构建..."
        # 继续检查构建
    fi
else
    log "✅ 应用访问正常 (HTTP $HTTP_CODE)"
fi

# ========================================
# 3. 检查构建完整性
# ========================================
log "检查构建完整性..."
if [ ! -f ".next/BUILD_ID" ]; then
    log "⚠️ 构建不完整（BUILD_ID 不存在），开始重新构建..."
    
    # 停止应用
    pm2 stop quicktoolshub
    
    # 只清理必要的文件（不清理 node_modules/.cache，节省时间）
    rm -rf .next
    
    log "开始构建（使用最小内存限制）..."
    # 构建时静默输出，减少 I/O 消耗
    NODE_OPTIONS="--max-old-space-size=512" npm run build >/dev/null 2>&1
    
    # 验证构建
    if [ -f ".next/BUILD_ID" ]; then
        BUILD_ID=$(cat .next/BUILD_ID)
        CHUNK_COUNT=$(find .next/static/chunks -name "*.js" 2>/dev/null | wc -l)
        log "✅ 构建完成 (BUILD_ID: $BUILD_ID, Chunks: $CHUNK_COUNT)"
    else
        log "❌ 构建失败，需要手动检查"
        pm2 start quicktoolshub || true
        exit 1
    fi
    
    # 重启应用
    pm2 start quicktoolshub
    sleep 10
    
    # 验证应用
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log "✅ 应用已恢复并正常运行"
    else
        log "❌ 应用仍无法访问，需要手动检查"
        exit 1
    fi
else
    log "✅ 构建完整 (BUILD_ID: $(cat .next/BUILD_ID))"
fi

# ========================================
# 4. 检查静态资源
# ========================================
log "检查静态资源..."
CSS_FILE=$(find .next/static -name "*.css" 2>/dev/null | head -1)
if [ -n "$CSS_FILE" ]; then
    CSS_PATH=$(echo "$CSS_FILE" | sed 's|\.next/static|/_next/static|')
    CSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$CSS_PATH" 2>/dev/null || echo "000")
    if [ "$CSS_CODE" = "200" ]; then
        log "✅ 静态资源正常"
    else
        log "⚠️ 静态资源访问失败 (HTTP $CSS_CODE)，可能需要检查 Nginx 配置"
    fi
else
    log "⚠️ 未找到 CSS 文件，构建可能不完整"
fi

log "========================================="
log "自动恢复检查完成"
log "========================================="

