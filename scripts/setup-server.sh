#!/bin/bash
# 服务器初始化脚本
# 安装所有依赖，配置环境

set -e

echo "========================================="
echo "服务器初始化脚本"
echo "========================================="

# 1. 安装 Ghostscript
echo ""
echo "=== 1. 安装 Ghostscript ==="
if command -v gs &> /dev/null; then
    echo "✅ Ghostscript 已安装: $(gs --version)"
else
    echo "正在安装 Ghostscript..."
    sudo apt-get update -qq
    sudo apt-get install -y ghostscript
    echo "✅ Ghostscript 安装完成: $(gs --version)"
fi

# 2. 检查并创建 .env.production
echo ""
echo "=== 2. 检查环境变量配置 ==="
if [ ! -f ".env.production" ]; then
    if [ -f ".env.production.example" ]; then
        echo "从示例文件创建 .env.production..."
        cp .env.production.example .env.production
        echo "⚠️ 请编辑 .env.production 文件，填入实际的配置值"
    else
        echo "⚠️ .env.production 不存在，请手动创建"
    fi
else
    echo "✅ .env.production 文件存在"
fi

# 3. 安装 npm 依赖
echo ""
echo "=== 3. 安装 npm 依赖 ==="
if [ -f "package.json" ]; then
    echo "正在安装 npm 包..."
    npm install --production
    echo "✅ npm 依赖安装完成"
else
    echo "⚠️ package.json 不存在"
fi

echo ""
echo "========================================="
echo "初始化完成"
echo "========================================="

