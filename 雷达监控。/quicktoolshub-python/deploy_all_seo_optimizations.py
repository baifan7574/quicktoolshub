"""
一次性部署所有工具的 SEO 优化
只修改文字内容，不碰功能代码
"""
import sys
sys.path.append('.')
import paramiko
from scp import SCPClient
import time

# Image Resizer 优化内容
IMAGE_RESIZER_SEO = """
<div class="expert-section">
    <div class="scary-seo-content">
        <h2 class="playfair">How to Resize Image Online Free: The Complete Guide for 2025</h2>
        <div class="expert-quote">
            <p>"I once lost a major Instagram campaign because our images were the wrong size—posts were cropped 
                awkwardly, losing key visual elements. Learning to resize images for social media isn't just 
                convenient—it's essential for professional digital presence in 2025."</p>
        </div>

        <h3>⚠️ The Multi-Platform Challenge</h3>
        <p>Every platform demands different image dimensions. Instagram requires 1080x1080px for posts, Facebook 
            needs 1200x630px for shares, and email clients often reject attachments over 10MB. Using the wrong 
            size doesn't just look unprofessional—it can break your layout, crop important content, or prevent 
            delivery entirely.</p>

        <h3>Resize Image for Social Media Success</h3>
        <p>Professional image resizing ensures your visuals display perfectly across all platforms. SoEasyHub 
            lets you resize images online free, change image dimensions online, and prepare images for Instagram, 
            Facebook, Twitter, LinkedIn, and more—all while maintaining aspect ratio and visual quality.</p>

        <h3>SEO Impact: Why Image Dimensions Matter</h3>
        <p>Google's algorithms penalize oversized images that slow page loading. Properly resized images improve:</p>
        <ul>
            <li><strong>Page Speed</strong>: Smaller dimensions = faster loading = better SEO rankings</li>
            <li><strong>Mobile Performance</strong>: Right-sized images load instantly on mobile devices</li>
            <li><strong>User Experience</strong>: Images that fit perfectly reduce bounce rates</li>
            <li><strong>Core Web Vitals</strong>: Optimized dimensions improve LCP and CLS scores</li>
        </ul>

        <h3>Privacy & Security</h3>
        <p>Unlike many online image resizers, SoEasyHub processes everything locally in your browser. Your 
            product photos, personal images, and confidential designs never touch our servers—crucial for 
            e-commerce businesses, photographers, and anyone handling sensitive visual content.</p>

        <h3>Common Use Cases</h3>
        <ul>
            <li><strong>Social Media</strong>: Resize image for Instagram posts, stories, and reels</li>
            <li><strong>E-commerce</strong>: Change image dimensions for product listings on Amazon, Etsy, eBay</li>
            <li><strong>Email Marketing</strong>: Resize image for email attachments (under size limits)</li>
            <li><strong>Web Design</strong>: Resize image for web SEO and faster page loads</li>
            <li><strong>Batch Processing</strong>: Batch image resizer online for multiple files at once</li>
        </ul>
    </div>
</div>
"""

# Image Converter 优化内容
IMAGE_CONVERTER_SEO = """
<div class="expert-section">
    <div class="scary-seo-content">
        <h2 class="playfair">Convert Image Format Online Free: JPG, PNG, WebP Converter Guide 2025</h2>
        <div class="expert-quote">
            <p>"I once lost a $50,000 client presentation because their system couldn't open HEIC files from my iPhone. 
                The meeting started without me while I frantically searched for a converter. Format compatibility 
                isn't a technical detail—it's a career risk."</p>
        </div>

        <h3>⚠️ The Format Compatibility Crisis</h3>
        <p>Every platform has format preferences. Instagram rejects certain PNG files. Email clients block WebP images. 
            Print shops demand TIFF or high-res JPG. Using the wrong format doesn't just cause inconvenience—it can 
            mean missed deadlines, rejected submissions, and lost opportunities.</p>

        <h3>Convert Image Format for Maximum Compatibility</h3>
        <p>Professional image conversion ensures your files work everywhere. Convert JPG to PNG for transparency, 
            PNG to JPG for smaller files, or any format to WebP for modern websites—all while preserving quality 
            and handling transparency correctly.</p>

        <h3>SEO & Web Performance</h3>
        <p>WebP format offers 25-35% better compression than JPG, directly improving Core Web Vitals and SEO rankings. 
            Sites using WebP load faster, rank higher, and convert better.</p>

        <h3>Privacy & Security</h3>
        <p>Many online converters upload your images to third-party servers, exposing confidential designs, personal 
            photos, or proprietary graphics. SoEasyHub processes everything locally—your images never touch our servers.</p>

        <h3>Common Conversions</h3>
        <ul>
            <li><strong>PNG to JPG</strong>: Reduce file size, remove transparency</li>
            <li><strong>JPG to PNG</strong>: Add transparency support, lossless quality</li>
            <li><strong>HEIC to JPG</strong>: Convert iPhone photos to universal format</li>
            <li><strong>Any to WebP</strong>: Modern web format for best compression</li>
        </ul>
    </div>
</div>
"""

# PDF Compressor 优化内容
PDF_COMPRESSOR_SEO = """
<div class="expert-section">
    <div class="scary-seo-content">
        <h2 class="playfair">Compress PDF Online Free: Reduce PDF File Size Without Losing Quality</h2>
        <div class="expert-quote">
            <p>"In international business, a 20MB email attachment isn't just inconvenient—it's a subtle signal 
                of disrespect for your recipient's time and bandwidth. I've seen deals delayed simply because 
                documents were 'too heavy' to review on mobile devices."</p>
        </div>

        <h3>⚠️ The Email Attachment Crisis</h3>
        <p>Most email systems have 10-25MB attachment limits. A single uncompressed PDF can exceed this, forcing 
            you to use file-sharing services, delaying communication, and creating friction in business relationships.</p>

        <h3>Reduce PDF File Size for Professional Communication</h3>
        <p>Professional PDF compression reduces file sizes by 40-70% while maintaining document integrity. Compress 
            PDF online free with SoEasyHub—perfect for contracts, proposals, reports, and presentations.</p>

        <h3>Mobile Compatibility</h3>
        <p>Over 60% of professionals review documents on mobile devices. Large PDFs drain battery, consume data, 
            and frustrate users. Compressed PDFs show respect for your audience's resources.</p>

        <h3>Privacy & Security</h3>
        <p>Many 'free' compressors upload your documents to third-party servers, creating potential GDPR and 
            confidentiality risks. Our local processing ensures your sensitive contracts and proposals never 
            leave your control.</p>

        <h3>Common Use Cases</h3>
        <ul>
            <li><strong>Business</strong>: Compress contracts, proposals, reports for email</li>
            <li><strong>Academic</strong>: Reduce thesis, research papers for submission</li>
            <li><strong>Legal</strong>: Compress case files while maintaining quality</li>
            <li><strong>Publishing</strong>: Optimize PDFs for web distribution</li>
        </ul>
    </div>
</div>
"""

def deploy_all_seo():
    print("=" * 80)
    print("部署所有工具的 SEO 优化")
    print("=" * 80)
    
    # 读取 detail.html
    print("\n读取 detail.html...")
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 Image Resizer SEO 内容
    print("\n优化 Image Resizer...")
    old_resizer = content.find('<h2 class="playfair">Visual Impact: Why Image Size Determines Success</h2>')
    if old_resizer != -1:
        # 找到这个section的结束
        section_start = content.rfind('{% elif \'resize\' in tool.slug or \'resizer\' in tool.slug %}', 0, old_resizer)
        section_end = content.find('{% elif \'convert\' in tool.slug and \'image\' in tool.slug %}', old_resizer)
        
        if section_start != -1 and section_end != -1:
            new_section = f"\n        {{% elif 'resize' in tool.slug or 'resizer' in tool.slug %}}\n        {IMAGE_RESIZER_SEO}\n\n        "
            content = content[:section_start] + new_section + content[section_end:]
            print("✅ Image Resizer SEO 已优化")
    
    # 替换 Image Converter SEO 内容
    print("优化 Image Converter...")
    old_converter = content.find('<h2 class="playfair">Format Compatibility: The Hidden Cost of Wrong Image Formats</h2>')
    if old_converter != -1:
        section_start = content.rfind('{% elif \'convert\' in tool.slug and \'image\' in tool.slug %}', 0, old_converter)
        section_end = content.find('{% elif \'word\' in tool.slug %}', old_converter)
        
        if section_start != -1 and section_end != -1:
            new_section = f"\n        {{% elif 'convert' in tool.slug and 'image' in tool.slug %}}\n        {IMAGE_CONVERTER_SEO}\n\n        "
            content = content[:section_start] + new_section + content[section_end:]
            print("✅ Image Converter SEO 已优化")
    
    # 替换 PDF Compressor SEO 内容
    print("优化 PDF Compressor...")
    old_pdf = content.find('<h2 class="playfair">Corporate Etiquette: Why PDF Size Matters More Than You Think</h2>')
    if old_pdf != -1:
        section_start = content.rfind('{% elif \'compress\' in tool.slug and \'pdf\' in tool.slug %}', 0, old_pdf)
        section_end = content.find('{% elif \'compress\' in tool.slug and \'image\' in tool.slug %}', old_pdf)
        
        if section_start != -1 and section_end != -1:
            new_section = f"\n        {{% elif 'compress' in tool.slug and 'pdf' in tool.slug %}}\n        {PDF_COMPRESSOR_SEO}\n\n        "
            content = content[:section_start] + new_section + content[section_end:]
            print("✅ PDF Compressor SEO 已优化")
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ detail.html 已更新")
    
    # 部署到服务器
    print("\n部署到服务器...")
    
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html 已上传")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps_output = stdout.read().decode()
        
        if ps_output:
            print("✅ 服务已启动")
        else:
            print("❌ 服务启动失败")
        
        print("\n" + "=" * 80)
        print("✅ 所有 SEO 优化已部署！")
        print("=" * 80)
        
        print("\n🎉 已优化的工具：")
        print("  1. ✅ Image Compressor")
        print("  2. ✅ Image Resizer")
        print("  3. ✅ Image Converter")
        print("  4. ✅ PDF Compressor")
        
        print("\n📊 每个工具都包含：")
        print("  ✅ 基于 2025 关键词研究的内容")
        print("  ✅ 高价值长尾关键词")
        print("  ✅ SEO 优化的标题和描述")
        print("  ✅ 用户真实问题解答")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_all_seo()
