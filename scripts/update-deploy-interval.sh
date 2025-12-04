#!/bin/bash
# 更新自动部署检查间隔

set -e

echo "========================================="
echo "更新自动部署检查间隔"
echo "========================================="
echo ""

# 新的检查间隔（分钟）
INTERVAL=${1:-2}  # 默认2分钟

echo "当前配置："
crontab -l 2>/dev/null | grep quicktoolshub || echo "未找到配置"

echo ""
echo "正在更新为每 ${INTERVAL} 分钟检查一次..."

# 移除旧的配置
crontab -l 2>/dev/null | grep -v quicktoolshub | crontab -

# 添加新配置
(crontab -l 2>/dev/null; echo "*/${INTERVAL} * * * * cd /var/www/quicktoolshub && git fetch origin master && git diff --quiet HEAD origin/master || /var/www/quicktoolshub/deploy.sh >> /var/www/quicktoolshub/logs/deploy.log 2>&1") | crontab -

echo ""
echo "✅ 更新完成！"
echo ""
echo "新配置："
crontab -l | grep quicktoolshub

echo ""
echo "========================================="
echo "说明："
echo "- 每 ${INTERVAL} 分钟检查一次 GitHub 更新"
echo "- 如果有更新，自动执行部署"
echo "- 部署日志：/var/www/quicktoolshub/logs/deploy.log"
echo "========================================="

