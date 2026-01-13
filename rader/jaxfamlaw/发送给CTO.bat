@echo off
chcp 65001 >nul
echo ============================================
echo   执行官给 CTO 发送测试消息
echo ============================================
echo.

set /p message="请输入您要对 CTO 说的话: "

echo.
echo 正在发送消息到 n8n webhook...

python -c "import requests; import json; from datetime import datetime; msg = '''CTO，这是来自执行官的测试消息:%message%发送时间: ''' + datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S'); r = requests.post('https://n8n.jaxfamlaw.com/webhook/gemini-update', json={'owner': 'baifan7574', 'repo': 'grich-cloud', 'path': 'EXEC_TO_CTO.md', 'content': msg, 'message': 'Message from Executive to CTO'}); print('✅ 发送成功！') if r.status_code == 200 else print(f'❌ 发送失败: {r.status_code}')"

echo.
echo ============================================
echo 验证步骤:
echo 1. 等待 3-5 秒
echo 2. 在浏览器打开: https://github.com/baifan7574/grich-cloud/blob/main/EXEC_TO_CTO.md
echo 3. 在 Google Drive 搜索: GRICH_MASTER_LOG.md 查看本地内容
echo ============================================
pause
