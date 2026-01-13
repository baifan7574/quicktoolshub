import requests
import json

# 读取环境变量
env_path = r'd:\quicktoolshub\雷达监控。\GRICH\grich-astro\.env'
env_vars = {}

try:
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
except Exception as e:
    print(f"❌ Error reading .env file: {e}")
    exit(1)

DEEPSEEK_API_KEY = env_vars.get("DEEPSEEK_API_KEY")

print("="*70)
print("🧠 测试 DeepSeek API 是否可用")
print("="*70)
print()

if not DEEPSEEK_API_KEY:
    print("❌ 错误: .env 文件中没有找到 DEEPSEEK_API_KEY")
    print("请检查文件: d:\\quicktoolshub\\雷达监控。\\GRICH\\grich-astro\\.env")
    exit(1)

print(f"✅ 找到 API Key: {DEEPSEEK_API_KEY[:10]}...{DEEPSEEK_API_KEY[-5:]}")
print()

# 测试 API 调用
print("📡 发送测试请求到 DeepSeek API...")
print()

try:
    response = requests.post(
        'https://api.deepseek.com/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        },
        json={
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'Say "API Test Successful" in JSON format: {"status": "success", "message": "..."}'}
            ],
            'temperature': 0.1
        },
        timeout=15
    )
    
    print(f"📊 HTTP 状态码: {response.status_code}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print("✅ API 调用成功！")
        print()
        print("📝 返回内容:")
        print("-" * 70)
        print(content)
        print("-" * 70)
        print()
        
        # 检查余额信息（如果有）
        if 'usage' in result:
            usage = result['usage']
            print("📊 Token 使用情况:")
            print(f"  - Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  - Completion Tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"  - Total Tokens: {usage.get('total_tokens', 'N/A')}")
        
        print()
        print("🎉 结论: DeepSeek API 配置正确，可以正常使用！")
        print("   AI 报告生成功能应该可以正常工作。")
        
    elif response.status_code == 401:
        print("❌ 认证失败！")
        print("   原因: API Key 无效或已过期")
        print("   建议: 检查 API Key 是否正确，或前往 DeepSeek 官网重新生成")
        
    elif response.status_code == 429:
        print("⚠️ 请求过于频繁！")
        print("   原因: 触发了速率限制")
        print("   建议: 稍后再试")
        
    elif response.status_code == 402:
        print("❌ 余额不足！")
        print("   原因: DeepSeek 账户余额为 0")
        print("   建议: 前往 DeepSeek 官网充值")
        print()
        print("   充值地址: https://platform.deepseek.com/")
        
    else:
        print(f"❌ API 调用失败")
        print(f"   错误信息: {response.text}")
    
except requests.exceptions.Timeout:
    print("❌ 请求超时")
    print("   建议: 检查网络连接")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("测试完成")
print("="*70)
