#!/usr/bin/env python3
"""
更新 PRICE_TRACKING.md 文件，填入今日价格
"""

import json
import re
from datetime import datetime

def load_today_prices():
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    prices = {}
    for code, item in data['commodities'].items():
        name = item['name']
        price = item['price']
        # 根据单位格式化价格
        unit = item['unit']
        if unit == '元/克':
            # 黄金，保留一位小数
            formatted = f"{price:.1f}"
        elif unit == '美元/桶':
            # 原油，保留两位小数
            formatted = f"{price:.2f}"
        elif unit == '元/千克':
            # 白银，取整数
            formatted = f"{int(price)}"
        else:
            # 其他商品，取整数
            formatted = f"{int(price)}"
        prices[name] = formatted
    return prices

def update_markdown():
    today = datetime.now().strftime('%Y-%m-%d')
    prices = load_today_prices()
    
    with open('PRICE_TRACKING.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到表头后的行
    in_table = False
    for i, line in enumerate(lines):
        if line.startswith('| 日期 | 星期 |'):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith('|'):
            continue
        # 解析行
        parts = line.split('|')
        if len(parts) < 15:  # 列数
            continue
        date_col = parts[1].strip()
        if date_col == today:
            # 更新这一行
            # 列顺序: 日期, 星期, 碳酸锂, 氢氧化锂, 铜, 铝, 锡, 镍, 黄金, 白银, 铁矿石, ABS, 瓦楞纸, 原油, 状态
            # 映射名称到索引
            mapping = {
                '碳酸锂': 2,
                '氢氧化锂': 3,
                '铜': 4,
                '铝': 5,
                '锡': 6,
                '镍': 7,
                '黄金': 8,
                '白银': 9,
                '铁矿石': 10,
                'ABS塑料': 11,
                '瓦楞纸': 12,
                '原油': 13
            }
            for name, idx in mapping.items():
                if name in prices:
                    parts[idx] = f" {prices[name]} "
            # 更新状态为 ✅
            parts[14] = " ✅ "
            # 重新组装行
            new_line = '|'.join(parts)
            lines[i] = new_line + '\n'
            break
    
    with open('PRICE_TRACKING.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"[OK] Updated PRICE_TRACKING.md for {today}")
    return True

if __name__ == '__main__':
    update_markdown()