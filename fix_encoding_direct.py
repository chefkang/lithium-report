#!/usr/bin/env python3
"""
直接修复daily_update_complete.py中的编码问题
"""

import re

def fix_encoding():
    with open('daily_update_complete.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 修复第124行：新闻数据已更新行
    for i, line in enumerate(lines):
        if '新闻数据已更' in line or '���������Ѹ���' in line:
            print(f"修复第{i+1}行: {line.strip()}")
            # 提取花括号部分
            match = re.search(r'\{len\(news_items\)\}', line)
            if match:
                lines[i] = f'    print(f"[OK] 新闻数据已更新: {{len(news_items)}} 条")\n'
            print(f"修复后: {lines[i].strip()}")
    
    # 修复第126行：圆点字符行
    for i, line in enumerate(lines):
        if '�?' in line or '•' in line:
            print(f"修复第{i+1}行: {line.strip()}")
            # 替换圆点字符为连字符
            lines[i] = lines[i].replace('�?', '-')
            lines[i] = lines[i].replace('•', '-')
            print(f"修复后: {lines[i].strip()}")
    
    # 修复其他中文乱码
    for i, line in enumerate(lines):
        if '步骤3: 更新历史数据�?' in line:
            lines[i] = line.replace('步骤3: 更新历史数据�?', '步骤3: 更新历史数据库')
    
    with open('daily_update_complete.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("编码修复完成")

if __name__ == '__main__':
    fix_encoding()