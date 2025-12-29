"""
全面检查所有博客文章的链接完整性
"""
import sys
sys.path.append('.')

def check_all_links():
    print("=" * 80)
    print("检查所有博客文章链接完整性")
    print("=" * 80)
    
    # 读取 blog.py
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 执行 blog.py 获取 ARTICLES
    exec_globals = {}
    exec(content, exec_globals)
    ARTICLES = exec_globals['ARTICLES']
    
    print(f"\n找到 {len(ARTICLES)} 篇文章\n")
    
    all_slugs = {article['slug'] for article in ARTICLES}
    
    issues = []
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"\n{'='*60}")
        print(f"文章 {i}: {article['title']}")
        print(f"Slug: {article['slug']}")
        print(f"工具: {article['tool_name']} ({article['tool_slug']})")
        print(f"{'='*60}")
        
        # 检查工具链接
        tool_slug = article['tool_slug']
        expected_tool_url = f"/tools/{tool_slug}"
        
        if expected_tool_url in article['content']:
            print(f"✅ 工具链接正确: {expected_tool_url}")
        else:
            print(f"⚠️  工具链接可能缺失: {expected_tool_url}")
            issues.append(f"文章 '{article['slug']}' 缺少工具链接 {expected_tool_url}")
        
        # 检查相关文章链接
        print(f"\n相关文章 ({len(article['related_articles'])} 篇):")
        for related in article['related_articles']:
            related_slug = related['slug']
            related_title = related['title']
            
            # 检查 slug 是否存在
            if related_slug in all_slugs:
                print(f"  ✅ {related_slug} - '{related_title}'")
            else:
                print(f"  ❌ {related_slug} - '{related_title}' (文章不存在！)")
                issues.append(f"文章 '{article['slug']}' 引用了不存在的文章 '{related_slug}'")
            
            # 检查内容中是否有链接
            expected_link = f"/blog/{related_slug}"
            if expected_link in article['content']:
                print(f"     ✅ 链接存在于内容中")
            else:
                print(f"     ⚠️  链接可能缺失于内容中")
                issues.append(f"文章 '{article['slug']}' 内容中缺少到 '{related_slug}' 的链接")
    
    # 总结
    print("\n" + "=" * 80)
    print("检查总结")
    print("=" * 80)
    
    if issues:
        print(f"\n❌ 发现 {len(issues)} 个问题：\n")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✅ 所有链接检查通过！")
    
    # 列出所有文章的 URL
    print("\n" + "=" * 80)
    print("所有文章 URL")
    print("=" * 80)
    
    for article in ARTICLES:
        print(f"\n{article['title']}")
        print(f"  URL: http://soeasyhub.com/blog/{article['slug']}")
        print(f"  工具: http://soeasyhub.com/tools/{article['tool_slug']}")
        print(f"  相关文章:")
        for related in article['related_articles']:
            print(f"    - http://soeasyhub.com/blog/{related['slug']}")

if __name__ == "__main__":
    check_all_links()
