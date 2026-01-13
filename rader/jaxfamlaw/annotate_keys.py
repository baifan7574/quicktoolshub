from PIL import Image, ImageDraw, ImageFont
import os

# 路径
image_path = r"C:/Users/bai/.gemini/antigravity/brain/305e64a1-db85-4a51-b780-5aaa52cb5f85/uploaded_image_1767757340735.png"
output_path = r"C:/Users/bai/.gemini/antigravity/brain/305e64a1-db85-4a51-b780-5aaa52cb5f85/annotated_keys.png"

# 打开图片
try:
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # 坐标 (估算基于截图)
    # 图片尺寸假设很大
    w, h = img.size
    
    # 定义框的位置 (基于提供的截图结构)
    # Publishable Key (Top)
    # 假设截图大概范围
    # 我们可以画相对位置
    
    # 简单的矩形框位置 (这些是大概估算的，基于常见网页布局)
    # 顶部Publishable Key大概在 1/3 处
    # 底部Secret Key大概在 2/3 处
    
    # 为了更准确，我画大一点的箭头或框
    
    # 1. Publishable Key (Green) - 前端
    # 找到 "Publishable key" 文字附近
    # 暂时画在图片的上半部分中间
    top_box = [50, 200, w-100, 480] 
    
    # 2. Secret Key (Red) - 后台
    # 画在图片的下半部分
    bottom_box = [50, 650, w-100, 950]

    # 为了不挡住字，我主要画在右侧或者框住整行
    
    # 实际策略：画明显的半透明框
    
    # 绿框 (前端)
    draw.rectangle(top_box, outline="green", width=10)
    
    # 红框 (后台)
    draw.rectangle(bottom_box, outline="red", width=10)
    
    # 尝试加载中文字体，如果没有就用默认
    # 在Windows上通常可以直接用 Simhei
    try:
        font = ImageFont.truetype("simhei.ttf", 60)
    except:
        try:
             font = ImageFont.truetype("arial.ttf", 60)
        except:
             font = ImageFont.load_default()

    # 添加文字说明
    draw.text((w/2 - 200, 150), "1. 前端 (Cloudflare) 用这个", fill="green", font=font, stroke_width=2, stroke_fill="white")
    draw.text((w/2 - 200, 600), "2. 后台 (GitHub) 用这个", fill="red", font=font, stroke_width=2, stroke_fill="white")
    
    # 保存
    img.save(output_path)
    print(f"Saved to {output_path}")

except Exception as e:
    print(f"Error: {e}")
