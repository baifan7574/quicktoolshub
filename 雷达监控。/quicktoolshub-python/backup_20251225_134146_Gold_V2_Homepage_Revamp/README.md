# QuickToolsHub - Python 版本

## 🎯 项目说明

这是 QuickToolsHub 的 Python Flask 版本，稳定可靠，不需要构建。

## 📋 功能

- ✅ 工具列表和详情
- ✅ PDF 压缩
- ✅ PDF 转 Word
- ✅ 背景移除
- ✅ 博客功能
- ✅ 后台管理

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
BACKGROUND_REMOVER_URL=http://localhost:5000
FLASK_DEBUG=False
```

### 3. 运行应用

```bash
python app.py
```

或者使用 Gunicorn（生产环境）：

```bash
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## 📁 项目结构

```
quicktoolshub-python/
├── app.py                 # Flask 主应用
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── routes/                # 路由
│   ├── tools.py           # 工具相关路由
│   ├── blog.py            # 博客相关路由
│   ├── api.py             # API 路由
│   └── admin.py            # 后台管理路由
├── templates/             # HTML 模板
├── static/                 # 静态文件
├── utils/                  # 工具函数
└── uploads/                # 上传文件临时目录
```

## 🔧 部署

使用 PM2 运行：

```bash
pm2 start "gunicorn -w 4 -b 0.0.0.0:3000 app:app" --name quicktoolshub
```

## ✅ 优势

- ✅ 不需要构建，修改代码后直接重启即可
- ✅ 稳定可靠，Python Flask 技术成熟
- ✅ 简单维护，您熟悉 Python
- ✅ 快速开发，添加新功能简单

