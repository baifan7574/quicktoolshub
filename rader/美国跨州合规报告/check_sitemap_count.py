import requests
import xml.etree.ElementTree as ET

try:
    response = requests.get('https://soeasyhub.com/sitemap.xml')
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        # Namespace handling
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('sitemap:url', namespace)
        print(f"Sitemap URL Count: {len(urls)}")
    else:
        print(f"Failed to fetch sitemap: {response.status_code}")
except Exception as e:
    print(f"Error checking sitemap: {e}")
