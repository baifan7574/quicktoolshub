import paramiko

def warmup_ai_model():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 一个极小的 Base64 图片用于热身
    warmup_script = """
import base64
from rembg import remove
from PIL import Image
import io

# 1x1 像素的白色图片
img_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNiAAAABgADNjd8qAAAAABJRU5ErkJggg==")
print("Starting warmup...")
try:
    remove(img_data)
    print("AI Model Warmup Successful!")
except Exception as e:
    print(f"Warmup failed: {e}")
"""
    
    commands = [
        f"cd /root/soeasyhub_v2 && python3 -c '{warmup_script}'"
    ]
    
    for cmd in commands:
        print("Running AI Model Warmup...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        print(output)
        if error:
            print(f"Error: {error}")
            
    ssh.close()

if __name__ == "__main__":
    warmup_ai_model()
