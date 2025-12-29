#!/bin/bash

# 自动部署脚本 - Python 版本
# 用于从 GitHub 自动拉取代码并重启应用

set -e

# 配置
PROJECT_DIR="/var/www/quicktoolshub-python"
BRANCH="master"
PM2_APP_NAME="quicktoolshub-python"

echo "========================================="
echo "自动部署开始"
echo "时间: $(date)"
echo "========================================="

# 进入项目目录
cd "$PROJECT_DIR" || exit 1

# 1. 拉取最新代码
echo "=== 1. 拉取最新代码 ==="
git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"
echo "✅ 代码已更新"

# 2. 检查是否有新依赖
echo ""
echo "=== 2. 检查依赖 ==="
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    echo "✅ 依赖已更新"
fi

# 3. 重启应用
echo ""
echo "=== 3. 重启应用 ==="
if pm2 list | grep -q "$PM2_APP_NAME"; then
    pm2 restart "$PM2_APP_NAME"
    echo "✅ 应用已重启"
else
    echo "⚠️ 应用未运行，正在启动..."
    pm2 start "gunicorn -w 4 -b 0.0.0.0:3000 app:app" --name "$PM2_APP_NAME"
    pm2 save
    echo "✅ 应用已启动"
fi

# 4. 等待应用启动
echo ""
echo "=== 4. 等待应用启动 ==="
sleep 5

# 5. 检查应用状态
echo ""
echo "=== 5. 检查应用状态 ==="
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ 应用运行正常"
else
    echo "❌ 应用启动失败，请检查日志"
    pm2 logs "$PM2_APP_NAME" --lines 20
    exit 1
fi

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="

