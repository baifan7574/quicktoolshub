import os

f = r"D:\quicktoolshub\rader\美国跨州合规报告\matrix_librarian.py"
t = open(f, "r", encoding="utf-8").read()
t = t.replace('"file_type": actual_type', '# "file_type": actual_type')

open(f, "w", encoding="utf-8").write(t)
