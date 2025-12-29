import requests
import time

time.sleep(3)

try:
    r_html = requests.get('http://43.130.229.184/', timeout=10)
    r_css = requests.get('http://43.130.229.184/static/css/premium.css', timeout=10)
    
    print(f'HTML Status: {r_html.status_code}')
    print(f'CSS Status: {r_css.status_code}')
    print(f'CSS Length: {len(r_css.text)} bytes')
    print(f'Has --primary: {"--primary" in r_css.text}')
    print(f'Has --accent: {"--accent" in r_css.text}')
    print(f'Has navbar styles: {".navbar" in r_css.text}')
    print(f'Has btn-premium: {".btn-premium" in r_css.text}')
    
    if r_css.status_code == 200 and "--primary" in r_css.text:
        print('\n✅ CSS is properly loaded!')
    else:
        print('\n❌ CSS has issues')
    
    print(f'\nFirst 300 chars of CSS:\n{r_css.text[:300]}')
        
except Exception as e:
    print(f'Error: {e}')
