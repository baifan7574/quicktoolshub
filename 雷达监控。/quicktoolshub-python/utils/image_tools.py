try:
    from rembg import remove
    from PIL import Image
    REMBG_AVAILABLE = True
except Exception as e:
    print(f"Warning: rembg or onnxruntime not available due to environment issues: {e}")
    REMBG_AVAILABLE = False
    
import io
import os
from config import Config

def remove_background(input_path):
    """
    移除图片背景 (带有环境兼容性处理)
    """
    if not REMBG_AVAILABLE:
        raise Exception("AI 处理环境暂未准备就绪 (ONNX/Numpy 冲突)，请稍后再试或联系管理员修复环境。")
        
    try:
        # 1. 打开图片
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        output_data = remove(input_data)
        
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_filename = f"{name}_no-bg.png"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return output_path

    except Exception as e:
        print(f"Error processing image {input_path}: {str(e)}")
        raise Exception(f"背景移除处理失败: {str(e)}")

def compress_image(input_path, quality=75, max_width=1920):
    """
    压缩图片文件（更激进的压缩策略）
    quality: 1-100, 默认 75（更激进的压缩）
    max_width: 最大宽度，默认 1920px（如果图片更大会缩小）
    """
    try:
        from PIL import Image
        
        # 打开图片
        img = Image.open(input_path)
        
        # 获取原始文件信息
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        original_size = os.path.getsize(input_path)
        
        # 如果图片太大，先缩小尺寸
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"Resized image from {img.width}x{img.height} to {max_width}x{new_height}")
        
        # 转换 RGBA 到 RGB（如果需要）
        if img.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为 mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 输出文件路径
        output_filename = f"{name}_compressed.jpg"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        # 激进压缩策略：先尝试低质量
        img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
        
        compressed_size = os.path.getsize(output_path)
        
        # 如果压缩率不够（小于 20%），尝试更激进的压缩
        if compressed_size > original_size * 0.8:
            print(f"First compression not enough, trying more aggressive...")
            # 更激进：降低质量到 60
            img.save(output_path, 'JPEG', quality=60, optimize=True, progressive=True)
            compressed_size = os.path.getsize(output_path)
            
            # 如果还不够，缩小尺寸
            if compressed_size > original_size * 0.7 and img.width > 1280:
                print(f"Still not enough, resizing to 1280px...")
                ratio = 1280 / img.width
                new_height = int(img.height * ratio)
                img_resized = img.resize((1280, new_height), Image.Resampling.LANCZOS)
                img_resized.save(output_path, 'JPEG', quality=70, optimize=True, progressive=True)
                compressed_size = os.path.getsize(output_path)
        
        reduction = (1 - compressed_size / original_size) * 100
        print(f"Image compressed: {original_size} -> {compressed_size} bytes ({reduction:.1f}% reduction)")
        
        return output_path
        
    except Exception as e:
        print(f"Error compressing image {input_path}: {str(e)}")
        raise Exception(f"图片压缩失败: {str(e)}")

def resize_image(input_path, width=None, height=None, maintain_aspect=True):
    """
    调整图片尺寸
    width: 目标宽度（像素）
    height: 目标高度（像素）
    maintain_aspect: 是否保持宽高比
    """
    try:
        from PIL import Image
        
        # 打开图片
        img = Image.open(input_path)
        
        # 获取原始尺寸
        original_width, original_height = img.size
        
        # 获取文件信息
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        # 计算新尺寸
        if maintain_aspect:
            if width and not height:
                # 只指定宽度，按比例计算高度
                ratio = width / original_width
                new_width = width
                new_height = int(original_height * ratio)
            elif height and not width:
                # 只指定高度，按比例计算宽度
                ratio = height / original_height
                new_width = int(original_width * ratio)
                new_height = height
            elif width and height:
                # 两者都指定，选择较小的缩放比例以保持宽高比
                width_ratio = width / original_width
                height_ratio = height / original_height
                ratio = min(width_ratio, height_ratio)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            else:
                raise Exception("必须指定宽度或高度")
        else:
            # 不保持宽高比，直接使用指定尺寸
            new_width = width if width else original_width
            new_height = height if height else original_height
        
        # 调整尺寸
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 输出文件路径
        output_filename = f"{name}_resized_{new_width}x{new_height}{ext}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        # 保存图片
        if img.mode == 'RGBA' or ext.lower() == '.png':
            resized_img.save(output_path, 'PNG', optimize=True)
        else:
            # 转换为 RGB 并保存为 JPEG
            if resized_img.mode != 'RGB':
                resized_img = resized_img.convert('RGB')
            resized_img.save(output_path, 'JPEG', quality=95, optimize=True)
        
        print(f"Image resized: {original_width}x{original_height} -> {new_width}x{new_height}")
        
        return output_path
        
    except Exception as e:
        print(f"Error resizing image {input_path}: {str(e)}")
        raise Exception(f"图片调整尺寸失败: {str(e)}")

def convert_image(input_path, output_format='jpg', quality=95):
    """
    转换图片格式
    output_format: 目标格式 ('jpg', 'png', 'webp')
    quality: 输出质量 (1-100, 仅用于 JPG 和 WebP)
    """
    try:
        from PIL import Image
        
        # 打开图片
        img = Image.open(input_path)
        
        # 获取文件信息
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        
        # 标准化输出格式
        output_format = output_format.lower()
        
        # 确定输出文件扩展名和 PIL 格式
        format_map = {
            'jpg': ('jpg', 'JPEG'),
            'jpeg': ('jpg', 'JPEG'),
            'png': ('png', 'PNG'),
            'webp': ('webp', 'WebP')
        }
        
        if output_format not in format_map:
            raise Exception(f"不支持的输出格式: {output_format}. 支持的格式: jpg, png, webp")
        
        ext, pil_format = format_map[output_format]
        
        # 输出文件路径
        output_filename = f"{name}_converted.{ext}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        # 处理不同格式的转换
        if pil_format == 'JPEG':
            # 转换为 JPG：需要处理透明度
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])  # 使用 alpha 通道
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为 JPG
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
        elif pil_format == 'PNG':
            # 转换为 PNG：保留透明度
            if img.mode not in ('RGB', 'RGBA'):
                if img.mode == 'P':
                    img = img.convert('RGBA')
                elif 'A' in img.mode:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
            
            # 保存为 PNG
            img.save(output_path, 'PNG', optimize=True)
            
        elif pil_format == 'WebP':
            # 转换为 WebP：支持透明度
            if img.mode == 'P':
                img = img.convert('RGBA')
            
            # 保存为 WebP
            img.save(output_path, 'WebP', quality=quality, method=6)
        
        original_size = os.path.getsize(input_path)
        converted_size = os.path.getsize(output_path)
        
        print(f"Image converted: {img.mode} -> {pil_format}, {original_size} -> {converted_size} bytes")
        
        return output_path
        
    except Exception as e:
        print(f"Error converting image {input_path}: {str(e)}")
        raise Exception(f"图片格式转换失败: {str(e)}")
