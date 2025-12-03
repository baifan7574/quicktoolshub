#!/bin/bash

# PM2 日志轮转配置脚本
# 使用方法: bash scripts/setup-pm2-logrotate.sh

echo "========================================="
echo "配置 PM2 日志轮转"
echo "========================================="

# 安装 pm2-logrotate 模块
echo "安装 pm2-logrotate 模块..."
pm2 install pm2-logrotate

# 配置日志轮转参数
echo "配置日志轮转参数..."
pm2 set pm2-logrotate:max_size 10M      # 单个日志文件最大10MB
pm2 set pm2-logrotate:retain 7          # 保留7天的日志
pm2 set pm2-logrotate:compress true     # 压缩旧日志
pm2 set pm2-logrotate:dateFormat YYYY-MM-DD_HH-mm-ss  # 日志文件名格式
pm2 set pm2-logrotate:workerInterval 30 # 每30秒检查一次
pm2 set pm2-logrotate:rotateInterval 0 0 * * *  # 每天午夜轮转

echo "========================================="
echo "PM2 日志轮转配置完成"
echo "========================================="
echo ""
echo "配置详情:"
pm2 conf pm2-logrotate

