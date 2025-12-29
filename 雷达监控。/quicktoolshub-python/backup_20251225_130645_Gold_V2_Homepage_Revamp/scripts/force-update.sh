#!/bin/bash

# 强制更新脚本 - 确保服务器上的代码是最新的

cd /var/www/quicktoolshub-python

echo "========================================="
echo "开始强制更新..."
echo "========================================="

# 1. 备份 .env 文件
if [ -f .env ]; then
    echo "📦 备份 .env 文件..."
    cp .env .env.backup
fi

# 2. 停止应用
echo "🛑 停止应用..."
pm2 stop quicktoolshub-python || true

# 3. 拉取最新代码
echo "📥 拉取最新代码..."
git fetch origin master
git reset --hard origin/master

# 4. 检查 requirements.txt 是否有变化
if [ -f requirements.txt ]; then
    echo "📦 检查依赖..."
    pip3 install -r requirements.txt --quiet
fi

# 5. 恢复 .env 文件
if [ -f .env.backup ]; then
    echo "📦 恢复 .env 文件..."
    mv .env.backup .env
fi

# 6. 启动应用
echo "🚀 启动应用..."
pm2 start ecosystem.config.js

# 7. 等待应用启动
sleep 3

# 8. 检查应用状态
echo "✅ 检查应用状态..."
pm2 status quicktoolshub-python

# 9. 测试健康检查
echo "🔍 测试健康检查..."
curl -s http://localhost:3000/api/health | head -1

echo ""
echo "========================================="
echo "更新完成！"
echo "========================================="

