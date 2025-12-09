#!/bin/bash

# 自动更新脚本 - 检查 Git 更新并自动重启

cd /var/www/quicktoolshub-python

# 检查是否是 Git 仓库
if [ ! -d ".git" ]; then
    echo "❌ 不是 Git 仓库，请先设置 Git 仓库"
    exit 1
fi

# 获取当前提交
CURRENT_COMMIT=$(git rev-parse HEAD)

# 拉取最新代码
git fetch origin master

# 检查是否有更新
REMOTE_COMMIT=$(git rev-parse origin/master)

if [ "$CURRENT_COMMIT" != "$REMOTE_COMMIT" ]; then
    echo "✅ 发现新代码，开始更新..."
    
    # 拉取代码
    git pull origin master
    
    # 检查是否需要安装依赖
    if [ -f "requirements.txt" ]; then
        # 检查 requirements.txt 是否有变化
        if git diff HEAD@{1} HEAD -- requirements.txt | grep -q "^+"; then
            echo "📦 检测到依赖变化，重新安装..."
            pip3 install -r requirements.txt
        fi
    fi
    
    # 重启应用
    echo "🔄 重启应用..."
    pm2 restart quicktoolshub-python
    
    echo "✅ 更新完成！"
else
    echo "ℹ️ 没有新更新"
fi

