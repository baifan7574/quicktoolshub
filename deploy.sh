#!/bin/bash

# 自动部署脚本
# 从 GitHub 拉取最新代码，构建并重启服务

set -e  # 遇到错误立即退出

echo "========================================="
echo "开始自动部署 - $(date)"
echo "========================================="

# 进入项目目录
cd /var/www/quicktoolshub

# 拉取最新代码
echo "正在拉取最新代码..."
git pull origin main

# 安装新依赖（如果有）
echo "正在检查依赖..."
npm install

# 重新构建
echo "正在构建项目..."
npm run build

# 重启 PM2 服务
echo "正在重启服务..."
pm2 restart quicktoolshub

# 检查服务状态
echo "检查服务状态..."
pm2 list

echo "========================================="
echo "部署完成 - $(date)"
echo "========================================="

