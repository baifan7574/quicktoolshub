"""
批量生成所有 SEO 文章并部署
"""

import os
import sys
sys.path.append('.')
from complete_seo_system import CompleteSEOSystem

def generate_all_articles():
    seo = CompleteSEOSystem()
    
    print("=" * 80)
    print("批量生成 SEO 文章")
    print("=" * 80)
    
    os.makedirs("articles", exist_ok=True)
    
    articles_generated = []
    
    for keyword_key in seo.keyword_database.keys():
        print(f"\n生成文章: {seo.keyword_database[keyword_key]['primary']}")
        
        # 生成文章
        article = seo.generate_article(keyword_key)
        
        # 保存文章
        filename = f"articles/{keyword_key.replace('_', '-')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(article)
        
        articles_generated.append({
            "keyword": seo.keyword_database[keyword_key]['primary'],
            "file": filename,
            "words": len(article.split()),
            "tool": seo.keyword_database[keyword_key]['tool_slug']
        })
        
        print(f"  ✅ 已保存: {filename}")
        print(f"  📝 字数: {len(article.split())} 词")
    
    print("\n" + "=" * 80)
    print(f"✅ 成功生成 {len(articles_generated)} 篇文章！")
    print("=" * 80)
    
    print("\n【文章列表】")
    for article in articles_generated:
        print(f"  📄 {article['keyword']}")
        print(f"     文件: {article['file']}")
        print(f"     字数: {article['words']} 词")
        print(f"     工具: {article['tool']}")
        print()
    
    return articles_generated

if __name__ == "__main__":
    articles = generate_all_articles()
    
    print("\n下一步：")
    print("  1. ✅ 所有文章已生成")
    print("  2. ⏳ 添加 Google Analytics")
    print("  3. ⏳ 部署到服务器")
    print("  4. ⏳ 提交到 Google Search Console")
