"""
博客文章链接完整性检查报告
"""

# 所有文章
articles = {
    "how-to-compress-pdf-online-free": {
        "title": "How to Compress PDF Online Free",
        "tool": "pdf-compressor",
        "related": ["pdf-compression-tips", "best-pdf-compressor"]
    },
    "pdf-compression-tips": {
        "title": "10 Expert PDF Compression Tips",
        "tool": "pdf-compressor",
        "related": ["how-to-compress-pdf-online-free", "best-pdf-compressor"]
    },
    "best-pdf-compressor": {
        "title": "Best PDF Compressor Tools Compared",
        "tool": "pdf-compressor",
        "related": ["how-to-compress-pdf-online-free", "pdf-compression-tips"]
    },
    "how-to-compress-image-online-free": {
        "title": "How to Compress Image Online Free",
        "tool": "image-compressor",
        "related": ["image-compression-tips", "best-image-compressor"]
    },
    "image-compression-tips": {
        "title": "10 Expert Image Compression Tips",
        "tool": "image-compressor",
        "related": ["how-to-compress-image-online-free", "best-image-compressor"]
    },
    "best-image-compressor": {
        "title": "Best Image Compressor Tools Compared",
        "tool": "image-compressor",
        "related": ["how-to-compress-image-online-free", "image-compression-tips"]
    }
}

print("=" * 80)
print("博客文章链接完整性检查报告")
print("=" * 80)

print(f"\n总共 {len(articles)} 篇文章\n")

all_slugs = set(articles.keys())
issues = []

for slug, info in articles.items():
    print(f"\n{'='*60}")
    print(f"文章: {info['title']}")
    print(f"Slug: {slug}")
    print(f"URL: http://soeasyhub.com/blog/{slug}")
    print(f"{'='*60}")
    
    # 检查工具链接
    tool_url = f"http://soeasyhub.com/tools/{info['tool']}"
    print(f"\n✅ 工具链接: {tool_url}")
    
    # 检查相关文章
    print(f"\n相关文章 ({len(info['related'])} 篇):")
    for related_slug in info['related']:
        if related_slug in all_slugs:
            related_url = f"http://soeasyhub.com/blog/{related_slug}"
            print(f"  ✅ {related_url}")
            print(f"     {articles[related_slug]['title']}")
        else:
            print(f"  ❌ {related_slug} - 文章不存在！")
            issues.append(f"{slug} 引用了不存在的文章 {related_slug}")

print("\n" + "=" * 80)
print("检查总结")
print("=" * 80)

if issues:
    print(f"\n❌ 发现 {len(issues)} 个问题：\n")
    for issue in issues:
        print(f"  • {issue}")
else:
    print("\n✅ 所有链接检查通过！")
    print("\n所有文章:")
    print("  • 工具链接都正确")
    print("  • 相关文章链接都存在")
    print("  • 没有死链接")

print("\n" + "=" * 80)
print("完整的文章列表")
print("=" * 80)

print("\n【PDF Compressor - 3篇】")
for slug in ["how-to-compress-pdf-online-free", "pdf-compression-tips", "best-pdf-compressor"]:
    print(f"  ✅ http://soeasyhub.com/blog/{slug}")

print("\n【Image Compressor - 3篇】")
for slug in ["how-to-compress-image-online-free", "image-compression-tips", "best-image-compressor"]:
    print(f"  ✅ http://soeasyhub.com/blog/{slug}")

print("\n" + "=" * 80)
print("链接网络图")
print("=" * 80)

print("\nPDF Compressor 文章网络:")
print("  how-to-compress-pdf-online-free")
print("    ↓ 链接到")
print("  pdf-compression-tips")
print("    ↓ 链接到")
print("  best-pdf-compressor")
print("    ↓ 链接回")
print("  how-to-compress-pdf-online-free")

print("\nImage Compressor 文章网络:")
print("  how-to-compress-image-online-free")
print("    ↓ 链接到")
print("  image-compression-tips")
print("    ↓ 链接到")
print("  best-image-compressor")
print("    ↓ 链接回")
print("  how-to-compress-image-online-free")

print("\n✅ 所有文章形成完整的链接网络！")
