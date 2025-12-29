import os
import re

path = r'd:\quicktoolshub\quicktoolshub-python\detail_new.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the paragraph inside expert-quote
# We want to add " — Michael" before the closing </p>
def add_signature(match):
    text = match.group(1).rstrip()
    if '— Michael' not in text:
        return f'<p>{text} — Michael</p>'
    return match.group(0)

# Apply to all expert-quote blocks
# Matches <div class="expert-quote"> ... <p>(content)</p>
new_content = re.sub(r'(<div class="expert-quote">\s*)<p>(.*?)</p>', 
                     r'\1<p>\2 — Michael</p>', 
                     content, flags=re.DOTALL)

# Also, let's add an expert quote for JSON Formatter if it's missing
json_expert_block = """            <div class="scary-seo-content">
                <h2 class="playfair">JSON Formatter Online Free: Validate and Beautify 2025</h2>
                <div class="expert-quote">
                    <p>"Clean code starts with clean data. If you can't read your JSON, you can't trust your API." — Michael</p>
                </div>
                <p>Ensure your JSON is perfectly formatted and error-free with our secure, browser-based tool.</p>
            </div>"""

# Replace the existing simple JSON block
old_json_block = """            <div class="scary-seo-content">
                <h2 class="playfair">JSON Formatter Online Free: Validate and Beautify 2025</h2>
                <p>Ensure your JSON is perfectly formatted and error-free with our secure, browser-based tool.</p>
            </div>"""

new_content = new_content.replace(old_json_block, json_expert_block)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Signature added to all expert quotes.")
