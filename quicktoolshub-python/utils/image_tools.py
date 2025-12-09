import requests
import os
from config import Config

def remove_background(input_path):
    """移除图片背景"""
    # 调用背景移除服务（您现有的 Python 服务）
    url = f"{Config.BACKGROUND_REMOVER_URL}/remove-background"
    
    with open(input_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        # 保存结果
        output_path = os.path.join(Config.UPLOAD_FOLDER, f'no_bg_{os.path.basename(input_path)}')
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"背景移除失败: {response.status_code}")

