// PM2 配置文件（可选，如果使用 PM2 管理）

module.exports = {
  apps: [{
    name: 'quicktoolshub-python',
    script: 'python3',
    args: '-m gunicorn -w 2 -b 0.0.0.0:3000 --timeout 120 app:app',
    cwd: '/var/www/quicktoolshub-python',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '/var/www/quicktoolshub-python/logs/err.log',
    out_file: '/var/www/quicktoolshub-python/logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
}

