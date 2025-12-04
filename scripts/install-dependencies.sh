#!/bin/bash
# 安装服务器依赖脚本
# 用于确保所有功能可以正常使用

set -e

echo "========================================="
echo "开始安装服务器依赖"
echo "========================================="

# 1. 安装 Ghostscript（PDF 压缩优化）
echo ""
echo "=== 1. 安装 Ghostscript（PDF 压缩优化）==="
if command -v gs &> /dev/null; then
    echo "✅ Ghostscript 已安装"
    gs --version
else
    echo "正在安装 Ghostscript..."
    sudo apt-get update
    sudo apt-get install -y ghostscript
    if command -v gs &> /dev/null; then
        echo "✅ Ghostscript 安装成功"
        gs --version
    else
        echo "⚠️ Ghostscript 安装失败，但 PDF 压缩功能仍可使用（效果较差）"
    fi
fi

# 2. 检查环境变量配置
echo ""
echo "=== 2. 检查环境变量配置 ==="
ENV_FILE=".env.production"

if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️ .env.production 文件不存在，正在创建..."
    cp .env.production.example .env.production 2>/dev/null || touch .env.production
fi

# 检查 Remove.bg API Key
if grep -q "REMOVE_BG_API_KEY=" "$ENV_FILE" 2>/dev/null; then
    API_KEY=$(grep "REMOVE_BG_API_KEY=" "$ENV_FILE" | cut -d '=' -f2)
    if [ -n "$API_KEY" ] && [ "$API_KEY" != "your_remove_bg_api_key" ]; then
        echo "✅ Remove.bg API Key 已配置"
    else
        echo "⚠️ Remove.bg API Key 未配置（背景移除工具需要）"
        echo "   请编辑 .env.production 文件，添加："
        echo "   REMOVE_BG_API_KEY=你的API Key"
        echo "   获取地址：https://www.remove.bg/api"
    fi
else
    echo "⚠️ Remove.bg API Key 未配置（背景移除工具需要）"
    echo "   请编辑 .env.production 文件，添加："
    echo "   REMOVE_BG_API_KEY=你的API Key"
    echo "   获取地址：https://www.remove.bg/api"
fi

# 3. 检查 npm 包
echo ""
echo "=== 3. 检查 npm 包 ==="
if [ -f "package.json" ]; then
    echo "检查关键 npm 包..."
    npm list pdf-lib pdf2json docx 2>/dev/null | grep -E "(pdf-lib|pdf2json|docx)" || echo "⚠️ 某些 npm 包可能未安装，运行 npm install"
else
    echo "⚠️ package.json 不存在"
fi

echo ""
echo "========================================="
echo "依赖检查完成"
echo "========================================="
echo ""
echo "📋 下一步："
echo "1. 如果 Remove.bg API Key 未配置，请编辑 .env.production 文件"
echo "2. 配置完成后，重启应用：pm2 restart quicktoolshub"
echo "3. 验证功能：访问网站测试各个工具"
echo ""

