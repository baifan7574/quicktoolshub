import re
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOContentBooster:
    """
    SoEasyHub SEO 内容注入脚本
    准则：
    1. 严禁修改 CSS 和 HTML 结构。
    2. 只优化字符串（标题、描述、关键词）。
    3. 在内容中注入高流量长尾词（无水印、隐私保护、2025最新等）。
    """
    def __init__(self):
        self.target_file = 'd:/quicktoolshub/quicktoolshub-python/routes/blog.py'
        self.backup_file = 'd:/quicktoolshub/quicktoolshub-python/routes/blog.py.bak'
        
        # 定义优化映射表 (只针对文字)
        self.optimization_map = {
            # 1. PDF 压缩优化
            "How to Compress PDF Online Free - Complete Guide 2025": 
            "Free PDF Compressor Online: No Watermark, Privacy-Focused & High Quality (2025)",
            
            "Learn how to compress PDF files online for free. Step-by-step guide with expert tips.":
            "Safe & fast PDF compression online. Processes locally in your browser for 100% privacy. No file uploads, no watermarks, no quality loss.",

            "compress PDF, reduce PDF size, PDF compressor":
            "compress PDF no watermark, safe PDF compressor, reduce PDF size without losing quality, private PDF tools 2025",

            # 2. 图片工具/通用优化
            "Best Image Compressor Tools Compared":
            "Best Free Image Compressor 2025: Bulk Compress JPG, PNG & WebP Safely",
            
            "best-image-compressor": "best-free-image-compressor-online",
        }

    def boost_content(self):
        if not os.path.exists(self.target_file):
            logger.error(f"找不到目标文件: {self.target_file}")
            return

        # 先备份，万一出问题可以瞬间恢复
        with open(self.target_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        logger.info("✅ 已创建原始文件备份 (.bak)")

        new_content = original_content
        changes_count = 0

        # 执行精准替换 (只替换引号内的文本)
        for old_txt, new_txt in self.optimization_map.items():
            if old_txt in new_content:
                # 只在作为完整字符串匹配时才替换，避免破坏变量名
                pattern = f'"{re.escape(old_txt)}"'
                replacement = f'"{new_txt}"'
                new_content = re.sub(pattern, replacement, new_content)
                
                # 同时也尝试替换单引号版本
                pattern_single = f"'{re.escape(old_txt)}'"
                replacement_single = f"'{new_txt}'"
                new_content = re.sub(pattern_single, replacement_single, new_content)
                
                logger.info(f"✨ 优化关键词: [{old_txt[:30]}...] -> [{new_txt[:30]}...]")
                changes_count += 1

        if new_content != original_content:
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"🚀 优化完成！共注入 {changes_count} 组高流量关键词。")
            print("\n" + "="*60)
            print("🛡️ SEO 流量注入成功 (双保险保障)")
            print("="*60)
            print("1. CSS/格式: 保持原样 (未改动)")
            print("2. 功能逻辑: 保持原样 (未改动)")
            print("3. 注入内容: 隐私保护、无水印、2025抢流词")
            print("4. 安全提醒: 如需恢复，请将 blog.py.bak 覆盖回 blog.py")
            print("="*60)
        else:
            logger.info("查无匹配项，文件内容已是最优或需要老窗口先同步代码。")

if __name__ == "__main__":
    booster = SEOContentBooster()
    booster.boost_content()
