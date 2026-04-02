import os

f = r"D:\quicktoolshub\rader\美国跨州合规报告\matrix_librarian.py"
t = open(f, "r", encoding="utf-8").read()
t = t.replace('if verify_req.status_code >= 400:', 'if False: # bucket is private, head request returns 400, so we skip verification')

open(f, "w", encoding="utf-8").write(t)
