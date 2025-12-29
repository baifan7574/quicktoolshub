import re
import os

def merge():
    # Load the original full blog file we downloaded as a backup
    with open('blog_check.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the two new articles to be added
    new_articles_data = [
        {
            "slug": "base64-encoder-online-free-guide",
            "title": "Base64 Encoder Online Free: How to Encode and Decode Text Securely 2025",
            "description": "Learn why Base64 encoding is essential for data integrity and how to use our free, secure online base64 encoder and decoder.",
            "keywords": "base64 encoder, base64 decoder, online base64, base64 encoding guide",
            "date": "2025-12-23",
            "category": "Developer Tools",
            "tool_name": "Base64 Encoder/Decoder",
            "tool_slug": "base64-encoder",
            "excerpt": "Master Base64 encoding and decoding for your development projects. Our free online tool ensures your data stays private with local browser processing.",
            "content": """
<h1 class="playfair">Base64 Encoder Online Free: How to Encode and Decode Text Securely 2025</h1>
<p class="lead">In the world of web development, data integrity and security are paramount. Discover how to use Base64 encoding correctly to transmit binary data over text-based protocols safely.</p>

<h2>What is Base64 Encoding?</h2>
<p>Base64 is a binary-to-text encoding scheme that represents binary data in an ASCII string format. It is commonly used when there is a need to encode binary data that needs to be stored and transferred over media that are designed to deal with textual data.</p>

<h3>Why Use Base64?</h3>
<ul>
    <li>Safe data transmission over HTTP</li>
    <li>Embedding images in HTML or CSS (Data URIs)</li>
    <li>Handling authentication headers (Basic Auth)</li>
    <li>Storing complex data in text-based formats like JSON or XML</li>
</ul>

<h2>The Security and Privacy Advantage</h2>
<p>Unlike many online tools that send your data to their servers for processing, our <strong>Base64 Encoder/Decoder</strong> works entirely within your browser. This means your sensitive API keys, passwords, or private data <strong>never leave your computer</strong>.</p>
<p>When searching for a <i>base64 encoder online free</i>, privacy should be your top consideration.</p>

<h2>How to Use</h2>
<ol>
    <li>Paste your plain text or binary data into the input field.</li>
    <li>Click <strong>Encode</strong> to get the Base64 representation.</li>
    <li>For decoding, paste a Base64 string and click <strong>Decode</strong>.</li>
</ol>

<p>Experience the most secure way to handle your data: <a href="/tools/base64-encoder">Secure Base64 Tool</a>.</p>
"""
        },
        {
            "slug": "url-encoder-online-free-guide",
            "title": "URL Encoder Online Free: How to Encode and Decode URLs Securely 2025",
            "description": "Learn why URL encoding (percent-encoding) is essential for web development. Securely encode and decode URL parameters with our local-first tool.",
            "keywords": "URL encoder, URL decoder, percent encoding, encode URL online, decode URL string",
            "date": "2025-12-23",
            "category": "Developer Tools",
            "tool_name": "URL Encoder/Decoder",
            "tool_slug": "url-encoder-decoder",
            "excerpt": "Master URL encoding/decoding for safe data transmission. Avoid broken links and parameter errors with our secure, browser-based URL tool.",
            "content": """
<h1 class="playfair">URL Encoder Online Free: How to Encode & Decode URLs Securely 2025</h1>
<p class="lead">A single special character in the wrong place can break an entire web application. Understanding URL encoding—also known as percent-encoding—is the first step toward building robust, professional web systems.</p>

<h2>What is URL Encoding?</h2>
<p>URL encoding is a mechanism for encoding information in a Uniform Resource Identifier (URI). Characters that are not allowed in a URL must be replaced with a <code>%</code> followed by two hexadecimal digits representing the character's ASCII value.</p>

<h3>Commonly Encoded Characters</h3>
<ul>
    <li><strong>Space</strong> becomes <code>%20</code></li>
    <li><strong>& (Ampersand)</strong> becomes <code>%26</code></li>
    <li><strong>? (Question Mark)</strong> becomes <code>%3F</code></li>
    <li><strong># (Hash)</strong> becomes <code>%23</code></li>
</ul>

<h2>Why You Need a URL Encoder Online Free Tool</h2>
<p>When you pass data through a URL parameter (Query String), you must ensure that the data doesn't interfere with the URL's structure. For example, if your search query contains a <code>&</code>, the browser might think a new parameter is starting.</p>
<p>Using our <strong>URL Encoder/Decoder</strong> ensures your parameters are always "safe" for the open web.</p>

<h2>The Privacy Advantage</h2>
<p>Like all SoEasyHub developer tools, our URL converter processes your input <strong>entirely in your browser</strong>. Most other sites log your queries on their servers. If you are encoding sensitive redirect URLs or internal system paths, privacy is non-negotiable.</p>

<h2>How to Use</h2>
<ol>
    <li>Enter your string into the input box.</li>
    <li>Click <strong>Encode</strong> for safe URL transmission.</li>
    <li>Click <strong>Decode</strong> to see the human-readable version of an encoded URL.</li>
</ol>

<p>Try it now: <a href="/tools/url-encoder-decoder">Secure URL Encoder/Decoder</a>.</p>
"""
        }
    ]

    # Convert the new articles to Python literal string format for insertion
    import json
    new_articles_list_str = ""
    for art in new_articles_data:
        # Use simple repr for strings to avoid escaping issues
        art_str = "    {\n"
        for k, v in art.items():
            if k == 'content' or k == 'description':
                 art_str += f'        "{k}": """{v}""",\n'
            else:
                 art_str += f'        "{k}": {repr(v)},\n'
        art_str += "    },\n"
        new_articles_list_str += art_str

    # Find where the ARTICLES list ends.
    # We'll look for the last '    }' before a ']'
    # Since ARTICLES is a list of dicts, it ends with ']'
    if 'ARTICLES = [' in content:
        # Find the opening bracket
        start_idx = content.find('ARTICLES = [') + len('ARTICLES = [')
        # Insert at the beginning of the list for better visibility on index
        new_content = content[:start_idx] + "\n" + new_articles_list_str + content[start_idx:]
        
        with open('blog_final.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully merged 11 articles into blog_final.py")
    else:
        print("Could not find ARTICLES list in blog_check.py")

if __name__ == "__main__":
    merge()
