"""
SoEasyHub 最终验收测试
测试所有功能并生成详细报告
"""

import requests
import time
from PIL import Image
import io

def final_acceptance_test():
    base_url = "http://43.130.229.184"
    
    print("=" * 80)
    print("SoEasyHub Product Hunt 发布前最终验收测试")
    print("=" * 80)
    print()
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # 测试 1: 主页加载和 SEO
    print("[1/6] 测试主页和 SEO 元素...")
    try:
        r = requests.get(f"{base_url}/", timeout=10)
        if r.status_code == 200:
            checks = {
                "SoEasyHub": "品牌名称",
                "Solving Troubles with Tech": "主标语",
                "Soothing Minds with Humanities": "副标语",
                "premium.css": "CSS 加载",
                "Playfair Display": "高端字体",
            }
            
            for keyword, desc in checks.items():
                if keyword in r.text:
                    results["passed"].append(f"✅ 主页 - {desc}")
                else:
                    results["failed"].append(f"❌ 主页 - {desc} 缺失")
        else:
            results["failed"].append(f"❌ 主页加载失败: {r.status_code}")
    except Exception as e:
        results["failed"].append(f"❌ 主页错误: {str(e)}")
    
    # 测试 2: 背景移除功能
    print("[2/6] 测试背景移除功能...")
    try:
        # 创建测试图片
        img = Image.new('RGB', (200, 200), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        r = requests.post(f"{base_url}/api/remove-background", files=files, timeout=60)
        
        if r.status_code == 200 and len(r.content) > 0:
            results["passed"].append(f"✅ 背景移除 API 正常工作 ({len(r.content)} bytes)")
        else:
            results["failed"].append(f"❌ 背景移除失败: {r.status_code}")
    except Exception as e:
        results["failed"].append(f"❌ 背景移除错误: {str(e)}")
    
    # 测试 3: 背景移除页面 UI
    print("[3/6] 测试背景移除页面 UI...")
    try:
        r = requests.get(f"{base_url}/tools/background-remover", timeout=10)
        if r.status_code == 200:
            ui_checks = {
                "Upload Image for Processing": "上传区域",
                "Legal Perspective": "专家视角 SEO",
                "Subliminal Trust": "焦虑驱动文案",
                "file-info": "文件信息显示",
            }
            
            for keyword, desc in ui_checks.items():
                if keyword in r.text:
                    results["passed"].append(f"✅ 背景移除页 - {desc}")
                else:
                    results["warnings"].append(f"⚠️ 背景移除页 - {desc} 可能缺失")
        else:
            results["failed"].append(f"❌ 背景移除页加载失败")
    except Exception as e:
        results["failed"].append(f"❌ 背景移除页错误: {str(e)}")
    
    # 测试 4: PDF 压缩页面
    print("[4/6] 测试 PDF 压缩页面...")
    try:
        r = requests.get(f"{base_url}/tools/pdf-compressor", timeout=10)
        if r.status_code == 200:
            seo_checks = {
                "Corporate Etiquette": "专家视角标题",
                "Hidden Cost": "焦虑驱动内容",
                "Legal Compliance": "法律合规性",
            }
            
            for keyword, desc in seo_checks.items():
                if keyword in r.text:
                    results["passed"].append(f"✅ PDF 压缩页 - {desc}")
                else:
                    results["warnings"].append(f"⚠️ PDF 压缩页 - {desc} 可能缺失")
        else:
            results["failed"].append(f"❌ PDF 压缩页加载失败")
    except Exception as e:
        results["failed"].append(f"❌ PDF 压缩页错误: {str(e)}")
    
    # 测试 5: 工具列表页
    print("[5/6] 测试工具列表页...")
    try:
        r = requests.get(f"{base_url}/tools", timeout=10)
        if r.status_code == 200:
            results["passed"].append("✅ 工具列表页正常")
        else:
            results["failed"].append(f"❌ 工具列表页失败: {r.status_code}")
    except Exception as e:
        results["failed"].append(f"❌ 工具列表页错误: {str(e)}")
    
    # 测试 6: 博客页面
    print("[6/6] 测试博客/Expert Advice 页...")
    try:
        r = requests.get(f"{base_url}/blog", timeout=10)
        if r.status_code == 200:
            results["passed"].append("✅ 博客页面正常")
        else:
            results["warnings"].append(f"⚠️ 博客页面: {r.status_code}")
    except Exception as e:
        results["warnings"].append(f"⚠️ 博客页面: {str(e)}")
    
    # 生成报告
    print("\n" + "=" * 80)
    print("最终验收报告")
    print("=" * 80)
    
    print(f"\n✅ 通过项目 ({len(results['passed'])}):")
    for item in results["passed"]:
        print(f"  {item}")
    
    if results["warnings"]:
        print(f"\n⚠️ 警告项目 ({len(results['warnings'])}):")
        for item in results["warnings"]:
            print(f"  {item}")
    
    if results["failed"]:
        print(f"\n❌ 失败项目 ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"  {item}")
    
    print("\n" + "=" * 80)
    
    total = len(results["passed"]) + len(results["failed"]) + len(results["warnings"])
    pass_rate = (len(results["passed"]) / total * 100) if total > 0 else 0
    
    print(f"总体通过率: {pass_rate:.1f}%")
    
    if len(results["failed"]) == 0:
        print("\n🎉 恭喜！所有关键功能测试通过！")
        print("✅ 网站已准备好发布到 Product Hunt！")
        print("\n建议的下一步:")
        print("1. 设置域名 HTTPS (可选但推荐)")
        print("2. 添加 Google Analytics")
        print("3. 准备 Product Hunt 发布素材")
        print("4. 设置社交媒体账号")
    else:
        print(f"\n⚠️ 发现 {len(results['failed'])} 个关键问题需要修复")
    
    return results

if __name__ == "__main__":
    final_acceptance_test()
