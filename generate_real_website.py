import json

# 读取真实价格
with open('real_prices_today.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 生成商品HTML
pages = []
for code, item in db['commodities'].items():
    is_up = item['change'] >= 0
    html = f'''
    <div id="{code}" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">{item['name']}</div>
                    <div class="commodity-symbol">{item['symbol']} | {item['category']}</div>
                </div>
                <div class="price-display">
                    <div class="current-price">{'$' if '美元' in item['unit'] else '¥'}{item['price']:,}</div>
                    <div class="price-change {'up' if is_up else 'down'}">{'▲' if is_up else '▼'} {abs(item['change']):,} ({'+' if is_up else ''}{item['change_percent']:.2f}%)</div>
                </div>
            </div>
            <p>{item['desc']}</p>
        </div>
        <div class="section">
            <div class="section-title">📊 今日价格详情</div>
            <table>
                <tr><th>规格</th><th>价格区间</th><th>均价</th><th>涨跌</th><th>单位</th></tr>
                <tr>
                    <td><strong>{item['name']}现货</strong></td>
                    <td>{item['price_range']}</td>
                    <td>{item['price']:,}</td>
                    <td><span class="badge {'badge-up' if is_up else 'badge-down'}">{'+' if is_up else ''}{item['change']:,}</span></td>
                    <td>{item['unit']}</td>
                </tr>
            </table>
        </div>
        <div class="footer">
            <p>🔍 数据来源：{db['data_source']}</p>
            <p>🔄 更新时间：{db['last_update']} | 真实数据 ✅</p>
        </div>
    </div>
    '''
    pages.append(html)

# 生成完整HTML
html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大宗商品监控系统 - 真实数据</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: #f7fafc; margin: 0; padding: 0; }}
        .header {{ position: fixed; top: 0; left: 0; right: 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 1000; padding: 12px 16px; }}
        .header-title {{ font-size: 18px; font-weight: 700; color: #1a365d; }}
        .current-time {{ font-size: 12px; color: #718096; }}
        .commodity-nav {{ display: flex; overflow-x: auto; gap: 6px; margin-top: 10px; }}
        .nav-item {{ padding: 6px 14px; background: white; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 12px; text-decoration: none; color: #2d3748; flex-shrink: 0; }}
        .nav-item:hover {{ background: #1a365d; color: white; }}
        .main-content {{ margin-top: 90px; padding: 0 12px 40px; }}
        .page {{ display: none; max-width: 800px; margin: 0 auto; }}
        .page:first-of-type {{ display: block; }}
        .page:target {{ display: block; }}
        .page:target ~ .page:first-of-type {{ display: none; }}
        .page-header {{ background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 12px; }}
        .commodity-info {{ display: flex; justify-content: space-between; align-items: flex-start; }}
        .commodity-name {{ font-size: 22px; font-weight: 700; }}
        .commodity-symbol {{ font-size: 13px; opacity: 0.9; }}
        .price-display {{ text-align: right; }}
        .current-price {{ font-size: 32px; font-weight: 800; font-family: monospace; }}
        .price-change {{ font-size: 13px; font-weight: 600; }}
        .up {{ color: #9ae6b4; }} .down {{ color: #fc8181; }}
        .section {{ background: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 12px; }}
        .section-title {{ font-size: 15px; font-weight: 600; color: #1a365d; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f8fafc; font-weight: 600; color: #718096; }}
        .badge {{ padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
        .badge-up {{ background: #c6f6d5; color: #276749; }}
        .badge-down {{ background: #fed7d7; color: #c53030; }}
        .footer {{ text-align: center; padding: 16px; color: #718096; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">📊 大宗商品监控系统</div>
        <div class="current-time">数据更新: {db['last_update']} ✅ 真实数据</div>
        <div class="commodity-nav">
            {''.join([f'<a href="#{code}" class="nav-item">{item["name"]}</a>' for code, item in db['commodities'].items()])}
        </div>
    </div>
    <div class="main-content">
        {''.join(pages)}
    </div>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[OK] Website updated with real data!")
print(f"[OK] Data source: {db['data_source']}")
print(f"[OK] Update date: {db['last_update']}")
