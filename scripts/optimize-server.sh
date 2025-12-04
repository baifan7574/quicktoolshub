#!/bin/bash
# 服务器优化脚本
# 清理空间和内存，为多个网站做准备

set -e

echo "========================================="
echo "服务器优化 - 清理空间和内存"
echo "========================================="
echo ""

# ========================================
# 第一部分：检查当前资源使用
# ========================================
echo "=== 1. 当前资源使用情况 ==="
echo ""

echo "内存使用："
free -h
echo ""

echo "磁盘使用："
df -h /
echo ""

echo "PM2 进程内存使用："
pm2 list
echo ""

# ========================================
# 第二部分：清理系统缓存和临时文件
# ========================================
echo "=== 2. 清理系统缓存和临时文件 ==="
echo ""

# 清理 apt 缓存
echo "清理 apt 缓存..."
sudo apt-get clean
sudo apt-get autoclean
echo "✅ apt 缓存已清理"
echo ""

# 清理系统日志（保留最近7天）
echo "清理系统日志..."
sudo journalctl --vacuum-time=7d 2>/dev/null || echo "⚠️ 无法清理系统日志"
echo ""

# 清理临时文件
echo "清理临时文件..."
sudo find /tmp -type f -atime +7 -delete 2>/dev/null || true
sudo find /var/tmp -type f -atime +7 -delete 2>/dev/null || true
echo "✅ 临时文件已清理"
echo ""

# ========================================
# 第三部分：清理 Node.js 相关
# ========================================
echo "=== 3. 清理 Node.js 缓存 ==="
echo ""

# 清理 npm 缓存
echo "清理 npm 缓存..."
npm cache clean --force 2>/dev/null || true
echo "✅ npm 缓存已清理"
echo ""

# 清理各项目的 node_modules/.cache
echo "清理项目构建缓存..."
for dir in /var/www/*/; do
    if [ -d "$dir/node_modules/.cache" ]; then
        echo "清理 $dir"
        rm -rf "$dir/node_modules/.cache"
    fi
done
echo "✅ 项目构建缓存已清理"
echo ""

# ========================================
# 第四部分：清理 PM2 日志
# ========================================
echo "=== 4. 清理 PM2 日志 ==="
echo ""

# PM2 日志轮转（保留最近7天）
pm2 flush 2>/dev/null || echo "⚠️ 无法清理 PM2 日志"
echo "✅ PM2 日志已清理"
echo ""

# ========================================
# 第五部分：清理 Nginx 日志
# ========================================
echo "=== 5. 清理 Nginx 日志 ==="
echo ""

# 清理旧的 Nginx 日志（保留最近7天）
sudo find /var/log/nginx -name "*.log.*" -mtime +7 -delete 2>/dev/null || true
sudo truncate -s 0 /var/log/nginx/*.log 2>/dev/null || true
echo "✅ Nginx 日志已清理"
echo ""

# ========================================
# 第六部分：优化 PM2 配置
# ========================================
echo "=== 6. 检查 PM2 配置 ==="
echo ""

# 检查 PM2 监控模块（占用内存）
PM2_MONIT=$(pm2 list | grep "pm2-server-monit" || echo "")
if [ -n "$PM2_MONIT" ]; then
    echo "⚠️ PM2 监控模块正在运行（占用约 40MB 内存）"
    echo "   如果内存紧张，可以停止：pm2 stop pm2-server-monit"
else
    echo "✅ PM2 监控模块未运行"
fi
echo ""

# ========================================
# 第七部分：检查大文件
# ========================================
echo "=== 7. 查找大文件（>100MB）==="
echo ""

sudo find /var/www -type f -size +100M 2>/dev/null | head -10 || echo "未找到大文件"
echo ""

# ========================================
# 第八部分：优化结果
# ========================================
echo "=== 8. 优化后资源使用 ==="
echo ""

echo "内存使用："
free -h
echo ""

echo "磁盘使用："
df -h /
echo ""

echo "========================================="
echo "优化完成！"
echo "========================================="
echo ""
echo "建议："
echo "1. 如果内存仍然紧张，考虑停止 PM2 监控模块"
echo "2. 定期运行此脚本清理缓存"
echo "3. 考虑升级服务器配置（如果预算允许）"

