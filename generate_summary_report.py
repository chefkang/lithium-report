#!/usr/bin/env python3
"""
生成大宗商品汇总报告（Markdown格式）
"""
import json
import sys
from datetime import datetime

def generate_summary():
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = data.get('last_update', datetime.now().strftime('%Y-%m-%d'))
    
    lines = []
    lines.append(f'# 大宗商品价格报告 ({today})')
    lines.append('')
    lines.append('| 商品 | 价格 | 涨跌 | 涨跌幅 | 单位 | 数据真实性 |')
    lines.append('|------|------|------|--------|------|------------|')
    
    for code, item in data['commodities'].items():
        change = item['change']
        change_percent = item['change_percent']
        change_sign = '+' if change >= 0 else ''
        is_real = '✅ 真实' if item.get('is_real', False) else '❌ 模拟'
        price_str = f"{item['price']:,}"
        # 格式化涨跌幅，保留适当小数位
        if abs(change_percent) < 0.01:
            change_percent_str = f'{change_percent:.4f}'
        elif abs(change_percent) < 1:
            change_percent_str = f'{change_percent:.2f}'
        else:
            change_percent_str = f'{change_percent:.1f}'
        
        lines.append(f'| {item["name"]} | {price_str} | {change_sign}{change} | {change_sign}{change_percent_str}% | {item["unit"]} | {is_real} |')
    
    lines.append('')
    lines.append(f'**数据来源**: {data.get("data_source", "SMM上海有色网 + 多方数据源")}')
    lines.append('')
    
    real_count = sum(1 for item in data['commodities'].values() if item.get('is_real', False))
    lines.append(f'**数据真实性**: 共{len(data["commodities"])}种商品，其中{real_count}种为真实市场数据')
    lines.append('')
    lines.append('**更新说明**: 每日上午10:00自动更新')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('### 商品分类统计')
    lines.append('')
    # 按分类统计
    categories = {}
    for item in data['commodities'].values():
        cat = item.get('category', '其他')
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        lines.append(f'- **{cat}**: {count}种商品')
    
    lines.append('')
    lines.append('### 价格涨跌统计')
    lines.append('')
    up_count = sum(1 for item in data['commodities'].values() if item['change'] >= 0)
    down_count = len(data['commodities']) - up_count
    lines.append(f'- 📈 上涨: {up_count}种商品')
    lines.append(f'- 📉 下跌: {down_count}种商品')
    
    return '\n'.join(lines)

if __name__ == '__main__':
    report = generate_summary()
    # 保存到文件
    with open('commodity_summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print('Report generated successfully')
    # 尝试输出（不包含emoji以避免编码问题）
    # 简单版本输出
    print('# 大宗商品价格报告')
    print('报告已生成到 commodity_summary_report.md')