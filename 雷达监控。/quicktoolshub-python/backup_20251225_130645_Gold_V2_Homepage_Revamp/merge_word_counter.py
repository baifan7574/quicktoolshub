import re
import os

def merge_word_counter():
    # Load the already merged blog file
    with open('blog_final.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_article = {
        "slug": "word-counter-online-free-guide",
        "title": "Word Counter Online Free: The Ultimate Guide to Precision Writing 2025",
        "description": "Master the art of concise communication with our Word Counter. Learn how word and character counts impact SEO, academic success, and professional credibility.",
        "keywords": "word counter, character counter, letter counter, online word count, drafting tool",
        "date": "2025-12-23",
        "category": "Text Tools",
        "tool_name": "Word Counter",
        "tool_slug": "word-counter",
        "excerpt": "Precision in writing is a superpower. Our Word Counter helps you stay within platform limits and improve readability with real-time analytics and 100% privacy.",
        "content": """
<h1 class="playfair">Word Counter Online Free: The Ultimate Guide to Precision Writing 2025</h1>
<p class="lead">Whether you're a student fighting for every word in an essay or a professional keeping a report tightly focused, knowing your exact count is the first step toward better writing.</p>

<h2>Why Does Word Count Matter?</h2>
<p>In the digital age, attention is currency. Different platforms have different 'sweet spots' for engagement:</p>
<ul>
    <li><strong>Blogs</strong>: 1,500 - 2,500 words for deep SEO impact.</li>
    <li><strong>Professional Emails</strong>: 50 - 125 words for maximum response rates.</li>
    <li><strong>Twitter</strong>: 280 characters for concise social impact.</li>
</ul>

<h2>The Michael Method: Clarity Over Clutter</h2>
<p>As a <strong>Teacher</strong> and <strong>Lawyer</strong>, Michael understands that technical constraints often lead to better creative solutions. By setting a hard limit for yourself, you force your brain to select the most impactful words rather than the most convenient ones.</p>

<h3>Privacy in Professional Drafting</h3>
<p>Most online word counters log your text on their servers to 'improve their AI'. If you are drafting a sensitive legal document or a proprietary business memo, this is a massive security risk. Our tool processes your text <strong>locally</strong> in your browser—your words never leave your screen.</p>

<h2>How to Use Our Tool</h2>
<ol>
    <li>Paste your text into the input field.</li>
    <li>Watch the counts for words, characters, and paragraphs update instantly.</li>
    <li>Use the 'Characters (no space)' count for strict academic or publishing requirements.</li>
</ol>

<p>Start your next masterpiece here: <a href="/tools/word-counter">Precision Word Counter</a>.</p>
"""
    }

    # Format the new article
    art_str = "    {\n"
    for k, v in new_article.items():
        if k == 'content' or k == 'description':
             art_str += f'        "{k}": """{v}""",\n'
        else:
             art_str += f'        "{k}": {repr(v)},\n'
    art_str += "    },\n"

    # Insert at the beginning of the ARTICLES list
    if 'ARTICLES = [' in content:
        start_idx = content.find('ARTICLES = [') + len('ARTICLES = [')
        new_content = content[:start_idx] + "\n" + art_str + content[start_idx:]
        
        with open('blog_final.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully added Word Counter article to blog_final.py")
    else:
        print("Could not find ARTICLES list in blog_final.py")

if __name__ == "__main__":
    merge_word_counter()
