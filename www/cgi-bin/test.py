#!/usr/bin/python3

import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

html = """Content-Type:text/html

aaa:iueo
"""

print(html)
print(os.environ)
