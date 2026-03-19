#!/usr/bin/env python3
"""
修复daily_update_complete.py中的圆点字符
"""

with open('daily_update_complete.py', 'rb') as f:
    content = f.read()

# 查找并替换 Unicode 圆点字符 (•) 的 UTF-8 编码: E2 80 A2
# 将其替换为连字符和空格: 2D 20
new_content = content.replace(b'\xE2\x80\xA2', b'- ')

with open('daily_update_complete.py', 'wb') as f:
    f.write(new_content)

print("圆点字符已修复")