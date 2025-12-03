module.exports = {
  apps: [
    {
      name: 'quicktoolshub',
      script: 'npm',
      args: 'start',
      instances: 1, // 单实例运行，避免端口冲突
      exec_mode: 'fork', // 使用fork模式
      watch: false, // 生产环境不启用watch
      max_memory_restart: '800M', // 内存超过800M自动重启（优化内存使用）
      env: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      // 自动重启配置
      autorestart: true,
      max_restarts: 10, // 最多重启10次
      min_uptime: '10s', // 至少运行10秒才算成功启动
      restart_delay: 4000, // 重启延迟4秒
      // 日志轮转（由 pm2-logrotate 模块管理）
      log_type: 'json',
      // 性能监控
      pmx: true,
      // 进程监控
      listen_timeout: 10000, // 监听超时10秒
      kill_timeout: 5000, // 杀死进程超时5秒
      // 环境变量
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
    },
  ],
}

