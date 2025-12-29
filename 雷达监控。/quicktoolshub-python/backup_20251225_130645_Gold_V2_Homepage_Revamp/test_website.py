import requests
import time

time.sleep(2)

try:
    r = requests.get('http://43.130.229.184/', timeout=10)
    print(f'Status Code: {r.status_code}')
    print(f'Content Length: {len(r.text)}')
    
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in r.text)
    print(f'Has Chinese: {has_chinese}')
    print(f'Has "Solving Troubles": {"Solving Troubles with Tech" in r.text}')
    print(f'Has "Soothing Minds": {"Soothing Minds with Humanities" in r.text}')
    
    print('\n--- First 600 characters ---')
    print(r.text[:600])
    
    if r.status_code == 200 and "Solving Troubles with Tech" in r.text and not has_chinese:
        print('\n✅ SUCCESS! Website is fully English and working!')
    else:
        print('\n❌ Issues detected')
        
except Exception as e:
    print(f'Error: {e}')
