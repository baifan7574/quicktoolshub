import requests
import os

# 创建一个测试图片
from PIL import Image
import io

# 创建一个简单的测试图片
img = Image.new('RGB', (100, 100), color='red')
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# 测试 API
url = 'http://43.130.229.184/api/remove-background'
files = {'file': ('test.png', img_bytes, 'image/png')}

print(f"Testing API endpoint: {url}")
try:
    response = requests.post(url, files=files, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    if response.status_code == 200:
        print("✅ API is working! Image processed successfully.")
        print(f"Response size: {len(response.content)} bytes")
    else:
        print(f"❌ API returned error")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ Error: {e}")
