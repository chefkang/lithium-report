#!/usr/bin/env python3
"""
修复daily_update_complete.py中的编码问题
"""

import re

def fix_encoding():
    with open('daily_update_complete.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复新闻数据已更新行
    content = re.sub(
        r'print\(f"\[OK\] 新闻数据已更.*?: \{len\(news_items\)\} .*?"\)',
        'print(f"[OK] 新闻数据已更新: {len(news_items)} 条")',
        content
    )
    
    # 修复圆点字符行
    content = re.sub(
        r'print\(f"  .\{news\[\'title\'\]\} \({news\[\'category\'\]}\)"\)',
        'print(f"  - {news[\'title\']} ({news[\'category\']})")',
        content
    )
    
    # 修复其他可能的中文乱码
    # 步骤3标题
    content = content.replace('步骤3: 更新历史数据�?', '步骤3: 更新历史数据库')
    
    with open('daily_update_complete.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("编码修复完成")

if __name__ == '__main__':
    fix_encoding()