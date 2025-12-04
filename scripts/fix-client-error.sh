#!/bin/bash
# 彻底修复客户端错误脚本

set -e

echo "========================================="
echo "彻底修复客户端错误"
echo "========================================="

cd /var/www/quicktoolshub

# 1. 备份当前状态
echo ""
echo "=== 1. 备份当前状态 ==="
cp -r .next .next.backup 2>/dev/null || true

# 2. 强制拉取最新代码
echo ""
echo "=== 2. 强制拉取最新代码 ==="
git fetch origin master
git reset --hard origin/master

# 3. 检查关键文件是否已更新
echo ""
echo "=== 3. 检查关键文件 ==="
echo "检查 ToolRenderer.tsx:"
if grep -q "LoadingComponent\|loading:" components/tools/ToolRenderer.tsx 2>/dev/null; then
    echo "⚠️ ToolRenderer.tsx 仍有 loading 组件，需要更新"
else
    echo "✅ ToolRenderer.tsx 已更新"
fi

echo ""
echo "检查 layout.tsx Script 位置:"
if grep -q "<head>" app/layout.tsx && grep -A 5 "Google Analytics" app/layout.tsx | grep -q "<head>"; then
    echo "⚠️ Script 仍在 head 中，需要更新"
else
    echo "✅ layout.tsx Script 位置正确"
fi

# 4. 清理并重新安装依赖
echo ""
echo "=== 4. 清理并重新安装依赖 ==="
rm -rf node_modules/.cache
npm install

# 5. 清理构建缓存并重新构建
echo ""
echo "=== 5. 清理构建缓存并重新构建 ==="
rm -rf .next
npm run build 2>&1 | tee /tmp/build.log

# 检查构建是否有错误
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 构建失败！查看错误："
    tail -50 /tmp/build.log
    exit 1
fi

# 6. 重启应用
echo ""
echo "=== 6. 重启应用 ==="
pm2 restart quicktoolshub
sleep 5

# 7. 检查应用状态
echo ""
echo "=== 7. 检查应用状态 ==="
pm2 list | grep quicktoolshub

# 8. 测试应用
echo ""
echo "=== 8. 测试应用 ==="
curl -I http://localhost:3000 2>&1 | head -5

echo ""
echo "========================================="
echo "修复完成！"
echo "========================================="
echo ""
echo "如果还有问题，请检查："
echo "1. PM2 日志：pm2 logs quicktoolshub --err --lines 50"
echo "2. 浏览器控制台错误信息"

