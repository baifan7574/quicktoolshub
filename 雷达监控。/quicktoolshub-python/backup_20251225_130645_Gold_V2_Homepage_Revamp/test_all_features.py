import requests
import time

def test_all_features():
    """全面测试 SoEasyHub 的所有功能"""
    
    base_url = "http://43.130.229.184"
    results = []
    
    print("=" * 80)
    print("SoEasyHub 全站功能测试报告")
    print("=" * 80)
    
    # 1. 测试主页
    print("\n[1/8] 测试主页...")
    try:
        r = requests.get(f"{base_url}/", timeout=10)
        if r.status_code == 200 and "SoEasyHub" in r.text:
            results.append(("✅ 主页", "正常"))
            print("  ✅ 主页加载正常")
        else:
            results.append(("❌ 主页", f"状态码: {r.status_code}"))
            print(f"  ❌ 主页异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ 主页", str(e)))
        print(f"  ❌ 主页错误: {e}")
    
    # 2. 测试工具列表页
    print("\n[2/8] 测试工具列表页...")
    try:
        r = requests.get(f"{base_url}/tools", timeout=10)
        if r.status_code == 200:
            results.append(("✅ 工具列表", "正常"))
            print("  ✅ 工具列表页正常")
        else:
            results.append(("❌ 工具列表", f"状态码: {r.status_code}"))
            print(f"  ❌ 工具列表页异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ 工具列表", str(e)))
        print(f"  ❌ 工具列表页错误: {e}")
    
    # 3. 测试背景移除工具详情页
    print("\n[3/8] 测试背景移除工具页...")
    try:
        r = requests.get(f"{base_url}/tools/background-remover", timeout=10)
        if r.status_code == 200 and "Background Remover" in r.text:
            results.append(("✅ 背景移除页面", "正常"))
            print("  ✅ 背景移除页面正常")
        else:
            results.append(("❌ 背景移除页面", f"状态码: {r.status_code}"))
            print(f"  ❌ 背景移除页面异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ 背景移除页面", str(e)))
        print(f"  ❌ 背景移除页面错误: {e}")
    
    # 4. 测试 PDF 压缩工具详情页
    print("\n[4/8] 测试 PDF 压缩工具页...")
    try:
        r = requests.get(f"{base_url}/tools/pdf-compressor", timeout=10)
        if r.status_code == 200:
            results.append(("✅ PDF 压缩页面", "正常"))
            print("  ✅ PDF 压缩页面正常")
        else:
            results.append(("❌ PDF 压缩页面", f"状态码: {r.status_code}"))
            print(f"  ❌ PDF 压缩页面异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ PDF 压缩页面", str(e)))
        print(f"  ❌ PDF 压缩页面错误: {e}")
    
    # 5. 测试博客页面
    print("\n[5/8] 测试博客/Expert Advice 页...")
    try:
        r = requests.get(f"{base_url}/blog", timeout=10)
        if r.status_code == 200:
            results.append(("✅ 博客页面", "正常"))
            print("  ✅ 博客页面正常")
        else:
            results.append(("❌ 博客页面", f"状态码: {r.status_code}"))
            print(f"  ❌ 博客页面异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ 博客页面", str(e)))
        print(f"  ❌ 博客页面错误: {e}")
    
    # 6. 测试 API 健康检查
    print("\n[6/8] 测试 API 健康检查...")
    try:
        r = requests.get(f"{base_url}/api/health", timeout=10)
        if r.status_code == 200:
            results.append(("✅ API 健康检查", "正常"))
            print("  ✅ API 健康检查正常")
        else:
            results.append(("❌ API 健康检查", f"状态码: {r.status_code}"))
            print(f"  ❌ API 健康检查异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ API 健康检查", str(e)))
        print(f"  ❌ API 健康检查错误: {e}")
    
    # 7. 测试 CSS 加载
    print("\n[7/8] 测试 CSS 样式文件...")
    try:
        r = requests.get(f"{base_url}/static/css/premium.css", timeout=10)
        if r.status_code == 200 and "--primary" in r.text:
            results.append(("✅ CSS 样式", "正常"))
            print("  ✅ CSS 样式文件正常")
        else:
            results.append(("❌ CSS 样式", f"状态码: {r.status_code}"))
            print(f"  ❌ CSS 样式文件异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ CSS 样式", str(e)))
        print(f"  ❌ CSS 样式文件错误: {e}")
    
    # 8. 测试背景移除 API（实际功能）
    print("\n[8/8] 测试背景移除 API 功能...")
    try:
        from PIL import Image
        import io
        
        # 创建测试图片
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        r = requests.post(f"{base_url}/api/remove-background", files=files, timeout=60)
        
        if r.status_code == 200:
            results.append(("✅ 背景移除 API", "正常"))
            print("  ✅ 背景移除 API 功能正常")
        else:
            results.append(("❌ 背景移除 API", f"状态码: {r.status_code}"))
            print(f"  ❌ 背景移除 API 异常: {r.status_code}")
    except Exception as e:
        results.append(("❌ 背景移除 API", str(e)))
        print(f"  ❌ 背景移除 API 错误: {e}")
    
    # 总结报告
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    
    passed = sum(1 for r in results if "✅" in r[0])
    failed = sum(1 for r in results if "❌" in r[0])
    
    for result in results:
        print(f"{result[0]}: {result[1]}")
    
    print(f"\n通过: {passed}/{len(results)}")
    print(f"失败: {failed}/{len(results)}")
    
    if failed == 0:
        print("\n🎉 所有功能测试通过！网站已准备好发布到 Product Hunt！")
    else:
        print(f"\n⚠️ 发现 {failed} 个问题需要修复")
    
    return results

if __name__ == "__main__":
    test_all_features()
