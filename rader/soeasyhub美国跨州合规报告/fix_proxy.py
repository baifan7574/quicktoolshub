import os

f = r"D:\quicktoolshub\rader\美国跨州合规报告\matrix_librarian.py"
t = open(f, "r", encoding="utf-8").read()
t = t.replace('os.environ["HTTP_PROXY"]', 'pass # os.environ["HTTP_PROXY"]')
t = t.replace('os.environ["HTTPS_PROXY"]', 'PROXIES={"http":"http://127.0.0.1:10808", "https":"http://127.0.0.1:10808"} #')
t = t.replace('timeout=15)', 'timeout=15, proxies=PROXIES)')
t = t.replace('timeout=30, verify=False)', 'timeout=30, verify=False, proxies=PROXIES)')
t = t.replace('timeout=10)', 'timeout=10, proxies={"http": None, "https": None})')

open(f, "w", encoding="utf-8").write(t)
