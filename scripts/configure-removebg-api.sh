#!/bin/bash
# 配置 Remove.bg API Key 脚本

set -e

echo "========================================="
echo "配置 Remove.bg API Key"
echo "========================================="
echo ""

cd /var/www/quicktoolshub

# 检查 .env.production 是否存在
if [ ! -f ".env.production" ]; then
    echo "⚠️ .env.production 文件不存在，正在创建..."
    touch .env.production
fi

# 检查是否已有 API Key
if grep -q "REMOVE_BG_API_KEY" .env.production 2>/dev/null; then
    echo "发现已存在的 REMOVE_BG_API_KEY 配置"
    echo ""
    echo "当前配置："
    grep "REMOVE_BG_API_KEY" .env.production
    echo ""
    read -p "是否要更新 API Key？(y/n): " update_choice
    if [ "$update_choice" != "y" ] && [ "$update_choice" != "Y" ]; then
        echo "已取消更新"
        exit 0
    fi
    # 删除旧配置
    sed -i '/REMOVE_BG_API_KEY/d' .env.production
fi

# 获取 API Key
echo ""
echo "请输入你的 Remove.bg API Key"
echo "（如果还没有，请访问：https://www.remove.bg/api 获取）"
echo ""
read -p "API Key: " api_key

if [ -z "$api_key" ]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

# 添加 API Key 到配置文件
echo "" >> .env.production
echo "# Remove.bg API Key（背景移除工具必需）" >> .env.production
echo "REMOVE_BG_API_KEY=$api_key" >> .env.production

echo ""
echo "✅ API Key 配置完成！"
echo ""
echo "正在重启应用..."
pm2 restart quicktoolshub

echo ""
echo "========================================="
echo "配置完成！"
echo "========================================="
echo ""
echo "📋 验证配置："
grep "REMOVE_BG_API_KEY" .env.production
echo ""
echo "✅ 背景移除工具现在应该可以正常使用了！"

