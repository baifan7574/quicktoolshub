import os
import markdown
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
    return config

def main():
    config = load_config()
    supabase: Client = create_client(config['url'], config['key'])

    slug = "does-a-california-rn-license-transfer-to-other-states"
    print(f"🔍 Fetching MONETIZED article for preview: {slug}...")
    
    res = supabase.table("grich_keywords_pool")\
        .select("keyword, final_article")\
        .eq("slug", slug)\
        .execute()

    if not res.data:
        print(f"❌ Record {slug} not found.")
        return

    data = res.data[0]
    keyword = data['keyword']
    content_md = data['final_article']
    
    # Convert Markdown to HTML
    content_html = markdown.markdown(content_md, extensions=['tables', 'fenced_code'])

    # Premium Template with Monetization Support
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{keyword} - Professional Fast-Track Registry</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #2563eb;
                --text: #1f2937;
                --bg: #f8fafc;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                line-height: 1.6;
                color: var(--text);
                background: var(--bg);
                margin: 0;
                padding: 0;
            }}
            .header {{
               background: #1e293b;
               color: white;
               padding: 20px 0;
               text-align: center;
               font-weight: 600;
               letter-spacing: 0.05em;
               text-transform: uppercase;
               font-size: 0.8rem;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 80px;
                border-radius: 0;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }}
            h1 {{ color: #0f172a; font-size: 3rem; margin-bottom: 30px; line-height: 1.1; font-weight: 800; }}
            h2 {{ color: #1e40af; border-bottom: 2px solid #eff6ff; padding-bottom: 15px; margin-top: 50px; font-weight: 700; }}
            h3 {{ color: #111827; margin-top: 35px; weight: 600; }}
            table {{ border-collapse: collapse; width: 100%; margin: 30px 0; font-size: 0.95rem; }}
            th, td {{ border: 1px solid #e2e8f0; padding: 15px; text-align: left; }}
            th {{ background: #f8fafc; font-weight: 700; color: #475569; }}
            blockquote {{ border-left: 5px solid #3b82f6; padding: 25px; font-style: italic; color: #334155; background: #f0f9ff; border-radius: 0 12px 12px 0; margin: 30px 0; }}
            .badge {{ display: inline-block; background: #3b82f6; color: white; padding: 6px 16px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; margin-bottom: 25px; text-transform: uppercase; }}
            footer {{ text-align: center; padding: 40px; color: #64748b; font-size: 0.875rem; }}
            
            /* CTA BUTTON STYLE */
            .cta-box {{ border: 2px solid #e2e8f0; border-radius: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">Compliance Authority - Official 2026 Licensing Database</div>
        <div class="container">
            <div class="badge">Official Registry Report</div>
            {content_html}
        </div>
        <footer>
            &copy; 2026 Matrix Compliance Network. All Rights Reserved. | Privacy Policy | Terms of Service
        </footer>
    </body>
    </html>
    """

    preview_path = os.path.abspath("landing_page_monetized.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"\n✨ Monetized Landing Page Generated!")
    print(f"👉 File Path: {preview_path}")

if __name__ == "__main__":
    main()
