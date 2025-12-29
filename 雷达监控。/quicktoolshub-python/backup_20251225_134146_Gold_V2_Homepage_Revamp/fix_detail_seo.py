import os

path = r'd:\quicktoolshub\quicktoolshub-python\detail_new.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Look for the end of the expert-section
target = '{% endif %}\n        </div>'
if target not in content:
    # Try with different whitespace if direct match fails
    print("Direct match failed, trying flexible match...")
    import re
    new_content = re.sub(r'{%\s+endif\s+%}\s+</div>', """            {% elif tool.slug == 'url-encoder-decoder' %}
            <div class="scary-seo-content">
                <h3 class="playfair">URL Encoder/Decoder Online Free: Secure Percent-Encoding</h3>
                <div class="expert-quote">
                    <p>"URL encoding is not encryption, but it is the critical glue that holds the web together. Safe parameter handling is a mandatory skill for modern devs."</p>
                </div>
                <h4>Why Use Our Local URL Encoder?</h4>
                <p>Browsers expect URLs to follow strict formatting rules. Attempting to send raw data like spaces or symbols can lead to 404 errors or truncated parameters. Our tool ensures your data is <strong>percent-encoded</strong> for absolute reliability.</p>
                <h4>Core Benefits</h4>
                <ul>
                    <li><strong>Full Character Support</strong>: Handles all non-ASCII characters and UTF-8 symbols.</li>
                    <li><strong>Instant Transformation</strong>: Real-time encoding and decoding in one click.</li>
                    <li><strong>100% Privacy</strong>: Your URL parameters are never sent to our server logs.</li>
                </ul>
            </div>
            {% endif %}
        </div>""", content, count=1)
else:
    replacement = """            {% elif tool.slug == 'url-encoder-decoder' %}
            <div class="scary-seo-content">
                <h3 class="playfair">URL Encoder/Decoder Online Free: Secure Percent-Encoding</h3>
                <div class="expert-quote">
                    <p>"URL encoding is not encryption, but it is the critical glue that holds the web together. Safe parameter handling is a mandatory skill for modern devs."</p>
                </div>
                <h4>Why Use Our Local URL Encoder?</h4>
                <p>Browsers expect URLs to follow strict formatting rules. Attempting to send raw data like spaces or symbols can lead to 404 errors or truncated parameters. Our tool ensures your data is <strong>percent-encoded</strong> for absolute reliability.</p>
                <h4>Core Benefits</h4>
                <ul>
                    <li><strong>Full Character Support</strong>: Handles all non-ASCII characters and UTF-8 symbols.</li>
                    <li><strong>Instant Transformation</strong>: Real-time encoding and decoding in one click.</li>
                    <li><strong>100% Privacy</strong>: Your URL parameters are never sent to our server logs.</li>
                </ul>
            </div>
            {% endif %}
        </div>"""
    new_content = content.replace(target, replacement)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Modification successful.")
