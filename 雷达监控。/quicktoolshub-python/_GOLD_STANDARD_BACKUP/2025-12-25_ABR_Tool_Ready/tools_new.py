"""
Standardized tools.py with Base64 Encoder support
"""
from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase
import os

bp = Blueprint('tools', __name__, url_prefix='/tools')

def log_debug(msg):
    try:
        with open('/root/soeasyhub_v2/debug.txt', 'a') as f:
            f.write(msg + '\n')
    except:
        pass

def get_tools_list(category_slug=None, sort='popular', page=1, limit=100):
    supabase = get_supabase()
    tools_data = []
    try:
        if supabase:
            # We fetch more to ensure we have all tools for categorization accuracy
            query = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True)
            
            if sort == 'recent': query = query.order('created_at', desc=True)
            elif sort == 'alphabetical': query = query.order('name', desc=False)
            elif sort == 'most-used': query = query.order('use_count', desc=True)
            else: query = query.order('view_count', desc=True)
            
            result = query.execute()
            tools_data = result.data if result.data else []
            
            # CRITICAL: Filter out old duplicate tools that are being replaced by hardcoded versions
            unwanted_slugs = {'url-encoder'} 
            tools_data = [t for t in tools_data if t.get('slug') not in unwanted_slugs]
    except Exception as e:
        log_debug(f"Error fetching tools: {e}")
        pass
    
    # 强制添加硬编码工具
    hardcoded = [
        {
            "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
            "description": "Format, validate, and beautify JSON data instantly.", "view_count": 500, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9992, "name": "Base64 Encoder/Decoder", "slug": "base64-encoder",
            "description": "Encode and decode text to/from Base64 format securely.", "view_count": 300, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9993, "name": "URL Encoder/Decoder", "slug": "url-encoder-decoder",
            "description": "Encode and decode URLs with percent-encoding for safe transmission.", "view_count": 250, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9994, "name": "Word Counter", "slug": "word-counter",
            "description": "Count words, characters, and paragraphs in real-time.", "view_count": 600, "category_id": 3, 
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        },
        {
            "id": 9995, "name": "Text Case Converter", "slug": "text-case-converter",
            "description": "Convert text between uppercase, lowercase, title case, and more.", "view_count": 200, "category_id": 3,
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        },
        {
            "id": 9996, "name": "Lorem Ipsum Generator", "slug": "lorem-ipsum-generator",
            "description": "Generate placeholder text for designs and layouts.", "view_count": 180, "category_id": 4,
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9997, "name": "Random Password Generator", "slug": "random-password-generator",
            "description": "Generate strong, secure passwords locally in your browser.", "view_count": 150, "category_id": 4,
            "categories": {"name": "Security Tools", "slug": "security-tools"}
        },
        {
            "id": 9998, "name": "AI Text Rewriter", "slug": "ai-text-rewriter",
            "description": "Paraphrase text to improve fluency or avoid plagiarism.", "view_count": 100, "category_id": 3,
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        },
        {
            "id": 9999, "name": "AI Text Summarizer", "slug": "ai-text-summarizer",
            "description": "Summarize long articles into concise key points.", "view_count": 100, "category_id": 3,
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        },
        {
            "id": 10000, "name": "Text to PDF Converter", "slug": "text-to-pdf-converter",
            "description": "Convert plain text to PDF document instantly in browser.", "view_count": 100, "category_id": 2,
            "categories": {"name": "PDF Tools", "slug": "pdf-tools"}
        },
        {
            "id": 10001, "name": "Text Reverser", "slug": "text-reverser",
            "description": "Reverse text characters, words, or flip text instantly.", "view_count": 80, "category_id": 3,
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        },
        {
            "id": 20001, "name": "Bing Image Creator (DALL-E 3)", "slug": "bing-image-creator",
            "description": "Best Midjourney alternative. Generate high-quality AI art for free using DALL-E 3.", "view_count": 99999, "category_id": 5,
            "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
        },
        {
            "id": 20002, "name": "Photopea Online Editor", "slug": "photopea-online-editor",
            "description": "Advanced online photo editor. A free Photoshop alternative that runs in your browser.", "view_count": 88888, "category_id": 5,
            "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
        },
        {
            "id": 20003, "name": "Playground AI", "slug": "playground-ai",
            "description": "Generate up to 1000 AI images per day for free. Versatile and easy to use.", "view_count": 77777, "category_id": 5,
            "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
        },
        {
            "id": 20004, "name": "Leonardo.ai", "slug": "leonardo-ai",
            "description": "Create stunning, high-quality production-ready AI assets with Leonardo.ai.", "view_count": 66666, "category_id": 5,
            "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
        },
        {
            "id": 20005, "name": "CapCut Online Video Editor", "slug": "capcut-online-video-editor",
            "description": "Powerful AI video editing in your browser. The best free movie and clip maker.", "view_count": 55555, "category_id": 5,
            "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
        },
        {
            "id": 10002, "name": "Professional Email Sign-Off Generator", "slug": "email-sign-off-generator",
            "description": "Stop using 'Best regards'. Generate creative and professional email endings for any context.", "view_count": 99999, "category_id": 6,
            "categories": {"name": "Writing Assistant", "slug": "writing-assistant"}
        },
        {
            "id": 10003, "name": "Alternative to Best Regards", "slug": "alternative-to-best-regards",
            "description": "The ultimate list of 50+ professional, warm, and creative alternatives to 'Best regards' for 2025.", "view_count": 100000, "category_id": 6,
            "categories": {"name": "Writing Assistant", "slug": "writing-assistant"}
        },
        {
            "id": 30001, "name": "Image Compressor", "slug": "image-compressor",
            "description": "Compress images up to 80% with zero visible quality loss. Supports JPG, PNG, and WebP.", "view_count": 75000, "category_id": 1,
            "categories": {"name": "Image Tools", "slug": "image-tools"}
        },
        {
            "id": 99999, "name": "Michael's Wish Wall", "slug": "wish-wall",
            "description": "Help Michael build the future of SoEasyHub. Share your feature requests and visions.",
            "view_count": 1000, "category_id": 7,
            "categories": {"name": "Community", "slug": "community"}
        }
    ]
    
    # 合并并去重
    existing_slugs = {t['slug'] for t in tools_data}
    for h in hardcoded:
        if h['slug'] not in existing_slugs:
            tools_data.append(h)

    # 过滤分类
    if category_slug and category_slug != 'all':
        tools_data = [t for t in tools_data if t.get('categories', {}).get('slug') == category_slug]

    return tools_data

def render_tools_page(tools_list, page=1, total_pages=1):
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    categories_data = []
    
    supabase = get_supabase()
    try:
        if supabase:
             categories = supabase.table('categories').select('*').order('name').execute()
             if categories.data: categories_data = categories.data
    except: pass
    
    if not categories_data:
        categories_data = [
            {"id": 1, "name": "Image Tools", "slug": "image-tools"},
            {"id": 2, "name": "PDF Tools", "slug": "pdf-tools"},
            {"id": 3, "name": "Text Tools", "slug": "text-tools"},
            {"id": 4, "name": "Developer Tools", "slug": "developer-tools"}
        ]
    
    # CRITICAL FIX: Manually inject new categories if not present in DB
    c_slugs = [c['slug'] for c in categories_data]
    if 'ai-creative-lab' not in c_slugs:
        categories_data.append({"id": 5, "name": "AI Creative Lab", "slug": "ai-creative-lab"})
    if 'writing-assistant' not in c_slugs:
        categories_data.append({"id": 6, "name": "Writing Assistant", "slug": "writing-assistant"})
    
    # Rename PDF category for better marketing
    for cat in categories_data:
        if cat['slug'] == 'pdf-tools':
            cat['name'] = 'PDF & Office Lab'

    # 动态重新计算所有工具的分类统计
    # 获取“所有”工具（不带过滤）
    all_active_tools = get_tools_list(category_slug='all')
    total_count = len(all_active_tools)
    
    # 计算每个分类的数量
    counts = {}
    for t in all_active_tools:
        c_slug = t.get('categories', {}).get('slug')
        if c_slug:
            counts[c_slug] = counts.get(c_slug, 0) + 1
    
    # 将统计结果写入 categories_data
    for cat in categories_data:
        cat['tool_count'] = counts.get(cat['slug'], 0)
    
    return render_template('tools/index.html', 
                          tools=tools_list, 
                          categories=categories_data, 
                          current_category=category_slug, 
                          current_sort=sort, 
                          page=page, 
                          total_pages=total_pages,
                          total_count=total_count)

@bp.route('')
def tools_list():
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    tools_list = get_tools_list(category_slug=category_slug, sort=sort)
    return render_tools_page(tools_list)

@bp.route('/<slug>')
def tool_detail(slug):
    log_debug(f"DEBUG: tool_detail called with slug='{slug}'")
    
    if slug == 'pdf-merger': return render_template('tools/pdf_merger.html')
    if slug == 'pdf-splitter': return render_template('tools/pdf_splitter.html')
    
    # Safe Supabase retrieval
    try:
        supabase = get_supabase()
    except Exception as e:
        log_debug(f"Supabase Init Error: {e}")
        supabase = None

    if slug == 'wish-wall':
        wishes = []
        try:
            if supabase:
                try:
                    result = supabase.table('user_feedback').select('*').eq('type', 'wishlist').order('created_at', desc=True).limit(20).execute()
                    wishes = result.data if result.data else []
                except Exception as inner_e:
                    log_debug(f"Wish fetch error: {inner_e}")
                    # If table missing or connection fail, simply show empty wall
                    pass
        except Exception as e:
            log_debug(f"General Wish Wall Error: {e}")
            pass
            
        try:
            return render_template('pages/wish_wall.html', wishes=wishes)
        except Exception as e:
            log_debug(f"Template Render Error: {e}")
            return f"<h1>System Maintenance</h1><p>The Wish Wall is briefly unavailable due to an upgrade. Please try again in 5 minutes.</p><!-- Debug: {str(e)} -->", 500
    tool = None
    try:
        tool_result = supabase.table('tools').select('*, categories(name, slug)').eq('slug', slug).eq('is_active', True).single().execute()
        if tool_result.data: tool = tool_result.data
    except Exception as e:
        log_debug(f"DB Error: {e}")
        pass
        
    # Overrides for self-developed tools not in production DB yet
    if not tool:
        if slug == 'json-formatter':
            tool = {
                "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
                "description": "Format, validate, and beautify JSON data.",
                "short_description": "Format JSON",
                "view_count": 500, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'base64-encoder':
            tool = {
                "id": 9992, "name": "Base64 Encoder/Decoder", "slug": "base64-encoder",
                "description": "Encode and decode text to/from Base64 format securely.",
                "short_description": "Base64 Tool",
                "view_count": 300, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'url-encoder-decoder':
            tool = {
                "id": 9993, "name": "URL Encoder/Decoder", "slug": "url-encoder-decoder",
                "description": "Encode and decode URLs instantly.",
                "short_description": "URL Tool",
                "view_count": 250, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'word-counter':
            tool = {
                "id": 9994, "name": "Word Counter", "slug": "word-counter",
                "description": "Accurate word and character counting tool.",
                "short_description": "Word Tool",
                "view_count": 600, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
        elif slug == 'text-case-converter':
            tool = {
                "id": 9995, "name": "Text Case Converter", "slug": "text-case-converter",
                "description": "Convert text between uppercase, lowercase, title case, and more.", 
                "view_count": 200, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
        elif slug == 'lorem-ipsum-generator':
            tool = {
                "id": 9996, "name": "Lorem Ipsum Generator", "slug": "lorem-ipsum-generator",
                "description": "Generate placeholder text for designs and layouts.",
                "view_count": 180, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'random-password-generator':
            tool = {
                "id": 9997, "name": "Random Password Generator", "slug": "random-password-generator",
                "description": "Generate strong, secure passwords locally in your browser.",
                "view_count": 150, "category_id": 4,
                "categories": {"name": "Security Tools", "slug": "security-tools"}
            }
        elif slug == 'ai-text-rewriter':
            tool = {
                "id": 9998, "name": "AI Text Rewriter", "slug": "ai-text-rewriter",
                "description": "Paraphrase text to improve fluency or avoid plagiarism.",
                "view_count": 100, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
        elif slug == 'ai-text-summarizer':
            tool = {
                "id": 9999, "name": "AI Text Summarizer", "slug": "ai-text-summarizer",
                "description": "Summarize long articles into concise key points.",
                "view_count": 100, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
        elif slug == 'text-to-pdf-converter':
            tool = {
                "id": 10000, "name": "Text to PDF Converter", "slug": "text-to-pdf-converter",
                "description": "Convert plain text to PDF document instantly in browser.",
                "view_count": 100, "category_id": 2,
                "categories": {"name": "PDF Tools", "slug": "pdf-tools"}
            }
        elif slug == 'text-reverser':
            tool = {
                "id": 10001, "name": "Text Reverser", "slug": "text-reverser",
                "description": "Reverse text characters, words, or flip text instantly.",
                "view_count": 80, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
        elif slug == 'bing-image-creator':
            tool = {
                "id": 20001, "name": "Bing Image Creator (DALL-E 3)", "slug": "bing-image-creator",
                "description": "Best Midjourney alternative. Generate high-quality AI art for free using DALL-E 3.",
                "view_count": 1200, "category_id": 5,
                "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
            }
        elif slug == 'photopea-online-editor':
            tool = {
                "id": 20002, "name": "Photopea Online Editor", "slug": "photopea-online-editor",
                "description": "Advanced online photo editor. A free Photoshop alternative that runs in your browser.",
                "view_count": 1500, "category_id": 5,
                "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
            }
        elif slug == 'playground-ai':
            tool = {
                "id": 20003, "name": "Playground AI", "slug": "playground-ai",
                "description": "Generate up to 1000 AI images per day for free. Versatile and easy to use.",
                "view_count": 900, "category_id": 5,
                "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
            }
        elif slug == 'leonardo-ai':
            tool = {
                "id": 20004, "name": "Leonardo.ai", "slug": "leonardo-ai",
                "description": "Create stunning, high-quality production-ready AI assets with Leonardo.ai.",
                "view_count": 800, "category_id": 5,
                "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
            }
        elif slug == 'capcut-online-video-editor':
            tool = {
                "id": 20005, "name": "CapCut Online Video Editor", "slug": "capcut-online-video-editor",
                "description": "Powerful AI video editing in your browser. The best free movie and clip maker.",
                "view_count": 1100, "category_id": 5,
                "categories": {"name": "AI Creative Lab", "slug": "ai-creative-lab"}
            }
        elif slug == 'email-sign-off-generator':
            tool = {
                "id": 10002, "name": "Professional Email Sign-Off Generator", "slug": "email-sign-off-generator",
                "description": "Stop using 'Best regards'. Generate creative and professional email endings for any context.", "view_count": 99999, "category_id": 6,
                "categories": {"name": "Writing Assistant", "slug": "writing-assistant"}
            }
        elif slug == 'alternative-to-best-regards':
            tool = {
                "id": 10003, "name": "Alternative to Best Regards", "slug": "alternative-to-best-regards",
                "description": "The ultimate list of 50+ professional, warm, and creative alternatives to 'Best regards' for 2025.", 
                "short_description": "Best Regards Alternatives",
                "view_count": 888, "category_id": 6,
                "categories": {"name": "Writing Assistant", "slug": "writing-assistant"}
            }
    
    if not tool:
        return "Tool not found", 404
        
    related_tools = []
    return render_template('tools/detail.html', tool=tool, related_tools=related_tools)
