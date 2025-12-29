import requests
import time

time.sleep(3)

try:
    r = requests.get('http://43.130.229.184/', timeout=10)
    print(f'Status: {r.status_code}')
    print(f'Length: {len(r.text)}')
    print(f'Has navbar: {"navbar" in r.text}')
    print(f'Has tools-grid: {"tools-grid" in r.text}')
    print(f'Has footer: {"footer" in r.text}')
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in r.text)
    print(f'Has Chinese: {has_chinese}')
    
    if r.status_code == 200 and "tools-grid" in r.text and "navbar" in r.text:
        print('\n✅ SUCCESS! Complete professional site is live!')
    else:
        print('\n⚠️ Site loaded but missing components')
    
    print(f'\nFirst 800 chars:\n{r.text[:800]}')
        
except Exception as e:
    print(f'Error: {e}')
