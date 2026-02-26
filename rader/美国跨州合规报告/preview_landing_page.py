import os
import markdown
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line:
                config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("keys:")[1].strip()
    return config

def main():
    config = load_config()
    supabase: Client = create_client(config['url'], config['key'])

    print("🔍 Fetching one golden article for preview...")
    
    # Get the latest written article
    res = supabase.table("grich_keywords_pool")\
        .select("keyword, final_article")\
        .neq("final_article", "null")\
        .limit(1)\
        .execute()

    if not res.data:
        print("❌ No articles found in database.")
        return

    data = res.data[0]
    keyword = data['keyword']
    content_md = data['final_article']
    
    # Convert Markdown to HTML
    content_html = markdown.markdown(content_md, extensions=['tables', 'fenced_code'])

    # Premium Template
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{keyword} - Professional Guide</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #2563eb;
                --text: #1f2937;
                --bg: #f9fafb;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                line-height: 1.6;
                color: var(--text);
                background: var(--bg);
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 800px;
                margin: 40px auto;
                background: white;
                padding: 60px;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            h1 {{ color: #111827; font-size: 2.5rem; margin-bottom: 30px; line-height: 1.2; }}
            h2 {{ color: #1e40af; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-top: 40px; }}
            h3 {{ color: #111827; margin-top: 30px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #e5e7eb; padding: 12px; text-align: left; }}
            th {{ background: #f3f4f6; }}
            blockquote {{ border-left: 4px solid var(--primary); padding-left: 20px; font-style: italic; color: #4b5563; background: #eff6ff; padding: 20px; border-radius: 0 8px 8px 0; }}
            .badge {{ display: inline-block; background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="badge">Verified Expert Guide</div>
            {content_html}
        </div>
    </body>
    </html>
    """

    preview_path = os.path.abspath("landing_page_preview.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"\n✨ Landing Page Generated!")
    print(f"👉 File Path: {preview_path}")
    print(f"请在浏览器中打开此文件查看最终落地的‘专家感’效果。")

if __name__ == "__main__":
    main()
