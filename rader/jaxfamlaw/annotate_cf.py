from PIL import Image, ImageDraw, ImageFont

# 路径
image_path = r"C:/Users/bai/.gemini/antigravity/brain/305e64a1-db85-4a51-b780-5aaa52cb5f85/uploaded_image_1767758354029.png"
output_path = r"C:/Users/bai/.gemini/antigravity/brain/305e64a1-db85-4a51-b780-5aaa52cb5f85/cf_guide_step1.png"

try:
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # 目标：左侧边栏的 "Workers 和 Pages"
    # 在截图里，它大约在左侧列表的中下部。
    # 假设截图左侧栏宽约 250px
    # "Workers 和 Pages" 大概在垂直方向的中间偏下位置
    
    # 让我们画一个框在左边栏的大概位置，并加文字
    # 估算坐标: x=10, y=550 (大概位置), w=200, h=50
    # 为了保险，画一个大的区域指引
    
    # 绘制一个红色矩形框，圈出左侧菜单栏里的 "Workers 和 Pages"
    # 根据截图比例，大概在左侧，垂直高度60%左右
    # 这里的坐标是基于对1080p全屏截图的一般估算
    
    # 框的坐标 (Left, Top, Right, Bottom)
    # 假设侧边栏宽度
    sidebar_width = 250
    # 假设 "Workers" 在列表下方
    workers_y = 650  # 估算值
    
    draw.rectangle([10, workers_y, sidebar_width, workers_y + 80], outline="red", width=8)
    
    # 画一个大箭头指向它
    # 从右边指向左边
    arrow_end = (sidebar_width + 10, workers_y + 40)
    arrow_start = (sidebar_width + 150, workers_y + 40)
    
    draw.line([arrow_start, arrow_end], fill="red", width=10)
    # 箭头头部
    draw.polygon([(arrow_end[0], arrow_end[1]), 
                  (arrow_end[0]+30, arrow_end[1]-20), 
                  (arrow_end[0]+30, arrow_end[1]+20)], fill="red")

    # 文字
    try:
        font = ImageFont.truetype("msyh.ttc", 60) # 微软雅黑
    except:
        font = ImageFont.load_default()
        
    draw.text((arrow_start[0] + 10, arrow_start[1] - 80), "第一步：点这里", fill="red", font=font, stroke_width=2, stroke_fill="white")

    img.save(output_path)
    print(f"Saved to {output_path}")

except Exception as e:
    print(f"Error: {e}")
