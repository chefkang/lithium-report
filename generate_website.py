#!/usr/bin/env python3
"""
生成包含真实价格趋势的网站
从今天开始积累真实数据，60天后全部真实
"""

import json
from datetime import datetime

def generate_website():
    """生成完整的HTML网站"""
    
    # 读取价格数据库
    try:
        with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        print("[ERROR] Price database not found!")
        print("Please run: uv run python update_today_prices.py")
        return False
    
    # 生成商品页面
    pages_html = []
    is_first = True
    
    for commodity_id, data in db['commodities'].items():
        # 获取20天价格趋势
        history = data['price_history'][-20:] if data['price_history'] else []
        
        if not history:
            continue
        
        # 计算统计数据
        current_price = history[-1]['price']
        prev_price = history[-2]['price'] if len(history) > 1 else current_price
        change = current_price - prev_price
        change_percent = (change / prev_price * 100) if prev_price else 0
        is_up = change >= 0
        
        # 生成价格数据JSON用于Chart.js
        dates = [p['date'][5:] for p in history]  # 只取月-日
        prices = [p['price'] for p in history]
        
        page_html = f'''
        <!-- {data['name']} -->
        <div id="{commodity_id}" class="page{' active' if is_first else ''}">
            <div class="page-header">
                <div class="commodity-info">
                    <div>
                        <div class="commodity-name">{data['name']}</div>
                        <div class="commodity-symbol">{commodity_id.replace('-', ' ').title()} | {data.get('category', '商品')}</div>
                    </div>
                    <div class="price-display">
                        <div class="current-price">{'$' if 'oil' in commodity_id else '¥'}{current_price:,.2f}</div>
                        <div class="price-change {'up' if is_up else 'down'}">{'▲' if is_up else '▼'} {abs(change):,.2f} ({'+' if is_up else ''}{change_percent:.2f}%)</div>
                    </div>
                </div>
                <p>价格趋势数据：真实1天 + 模拟59天。从今天开始每天更新，60天后全部为真实数据。</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">今日涨跌</div>
                    <div class="stat-value">{'+' if is_up else ''}{change:,.0f}</div>
                    <div class="stat-change {'up' if is_up else 'down'}">{'+' if is_up else ''}{change_percent:.2f}%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">20天最高</div>
                    <div class="stat-value">{max(prices):,.0f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">20天最低</div>
                    <div class="stat-value">{min(prices):,.0f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">数据状态</div>
                    <div class="stat-value">{len([p for p in history if p.get('is_real')])}/60</div>
                    <div class="stat-change">真实天数</div>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="section-title">📈 近20天价格趋势</div>
                <canvas id="chart-{commodity_id}"></canvas>
            </div>
            
            <script>
                // {data['name']} 价格趋势图
                new Chart(document.getElementById('chart-{commodity_id}'), {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(dates)},
                        datasets: [{{
                            label: '{data['name']}价格 ({data['unit']})',
                            data: {json.dumps(prices)},
                            borderColor: '#3182ce',
                            backgroundColor: 'rgba(49, 130, 206, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: function(context) {{
                                const index = context.dataIndex;
                                const isReal = {json.dumps([p.get('is_real', False) for p in history])};
                                return isReal[index] ? '#e53e3e' : '#3182ce';  // 真实数据红色，模拟数据蓝色
                            }}
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    afterLabel: function(context) {{
                                        const isReal = {json.dumps([p.get('is_real', False) for p in history])};
                                        return isReal[context.dataIndex] ? '真实数据' : '模拟数据';
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{ grid: {{ display: false }} }},
                            y: {{ grid: {{ color: '#e2e8f0' }} }}
                        }}
                    }}
                }});
            </script>
            
            <div class="section">
                <div class="section-title">📊 价格数据说明</div>
                <div class="analysis-card">
                    <h4>数据来源</h4>
                    <p>从今天开始每天记录SMM真实价格。当前显示：</p>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        <li>真实数据：{len([p for p in history if p.get('is_real')])} 天</li>
                        <li>模拟数据：{len([p for p in history if not p.get('is_real')])} 天</li>
                        <li>累计记录：{len(history)} 天</li>
                        <li>预计完成：{60 - len([p for p in history if p.get('is_real')])} 天后全部为真实数据</li>
                    </ul>
                    <p style="margin-top: 10px;"><strong>提示：</strong>红色数据点为今日及之后记录的真实价格，蓝色为基于历史波动生成的模拟数据。</p>
                </div>
            </div>
            
            <div class="footer">
                <p>🔍 数据来源：SMM上海有色网（每日更新）</p>
                <p>🔄 数据记录：{db['last_update']} | 真实数据累计：{len([p for p in history if p.get('is_real')])}/60 天</p>
            </div>
        </div>
        '''
        
        pages_html.append(page_html)
        is_first = False
    
    # 生成完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>大宗商品监控系统 - 真实价格趋势</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f7fafc; color: #2d3748; line-height: 1.6; }}
        .header {{ position: fixed; top: 0; left: 0; right: 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 1000; }}
        .header-content {{ max-width: 1400px; margin: 0 auto; padding: 12px 16px; }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .header-title {{ font-size: 18px; font-weight: 700; color: #1a365d; }}
        .current-time {{ font-size: 12px; color: #718096; }}
        .commodity-nav {{ display: flex; overflow-x: auto; gap: 6px; scrollbar-width: none; }}
        .commodity-nav::-webkit-scrollbar {{ display: none; }}
        .nav-item {{ padding: 6px 14px; background: white; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 12px; font-weight: 500; white-space: nowrap; cursor: pointer; flex-shrink: 0; text-decoration: none; color: #2d3748; }}
        .nav-item:hover, .nav-item.active {{ background: #1a365d; color: white; border-color: #1a365d; }}
        .main-content {{ margin-top: 90px; padding: 0 12px 40px; }}
        .page {{ display: none; max-width: 1400px; margin: 0 auto; }}
        .page:target {{ display: block; }}
        .page:first-of-type {{ display: block; }}
        .page:target ~ .page:first-of-type {{ display: none; }}
        .page-header {{ background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 12px; }}
        .commodity-info {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; flex-wrap: wrap; gap: 8px; }}
        .commodity-name {{ font-size: 22px; font-weight: 700; }}
        .commodity-symbol {{ font-size: 13px; opacity: 0.9; }}
        .price-display {{ text-align: right; }}
        .current-price {{ font-size: 32px; font-weight: 800; font-family: monospace; }}
        .price-change {{ font-size: 13px; font-weight: 600; }}
        .up {{ color: #9ae6b4; }} .down {{ color: #fc8181; }}
        .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 12px; }}
        .stat-card {{ background: white; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0; }}
        .stat-label {{ font-size: 11px; color: #718096; margin-bottom: 4px; }}
        .stat-value {{ font-size: 16px; font-weight: 700; color: #1a365d; font-family: monospace; }}
        .stat-change {{ font-size: 11px; margin-top: 2px; }}
        .chart-container {{ background: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 12px; height: 350px; }}
        .section {{ background: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 12px; }}
        .section-title {{ font-size: 15px; font-weight: 600; color: #1a365d; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }}
        .analysis-card {{ background: #f8fafc; padding: 14px; border-radius: 6px; border: 1px solid #e2e8f0; }}
        .analysis-card h4 {{ font-size: 13px; margin-bottom: 6px; color: #1a365d; }}
        .analysis-card p, .analysis-card ul {{ font-size: 12px; line-height: 1.6; }}
        .footer {{ text-align: center; padding: 16px; color: #718096; font-size: 10px; }}
        @media (min-width: 768px) {{
            .header-content {{ padding: 16px 24px; }}
            .main-content {{ margin-top: 110px; padding: 0 24px 40px; }}
            .page-header {{ padding: 32px 40px; }}
            .commodity-name {{ font-size: 28px; }}
            .current-price {{ font-size: 42px; }}
            .stats {{ grid-template-columns: repeat(4, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="header-top">
                <div class="header-title">📊 大宗商品监控系统</div>
                <div class="current-time">数据更新: {db['last_update']} | 真实数据累计中</div>
            </div>
            <div class="commodity-nav">
                <a href="#lithium-carbonate" class="nav-item active">碳酸锂</a>
                <a href="#lithium-hydroxide" class="nav-item">氢氧化锂</a>
                <a href="#copper" class="nav-item">铜</a>
                <a href="#aluminum" class="nav-item">铝</a>
                <a href="#tin" class="nav-item">锡</a>
                <a href="#nickel" class="nav-item">镍</a>
                <a href="#gold" class="nav-item">黄金</a>
                <a href="#silver" class="nav-item">白银</a>
                <a href="#iron-ore" class="nav-item">铁矿石</a>
                <a href="#abs" class="nav-item">ABS塑料</a>
                <a href="#corrugated-paper" class="nav-item">瓦楞纸</a>
                <a href="#crude-oil" class="nav-item">原油</a>
            </div>
        </div>
    </div>

    <div class="main-content">
        {''.join(pages_html)}
    </div>
</body>
</html>'''
    
    # 保存HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] Website generated successfully!")
    print(f"[INFO] Generated: {len(pages_html)} commodity pages")
    print(f"[INFO] Real data days: 1 (today)")
    print(f"[INFO] Simulated days: 59 (historical)")
    print(f"[INFO] Next update: tomorrow with new real data")
    print(f"\n[OK] File saved: index.html")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Generate Website with Real Price Trends")
    print("=" * 60)
    
    if generate_website():
        print("\n[OK] Now you can deploy to GitHub:")
        print("  git add index.html")
        print("  git commit -m 'Update with real price trends'")
        print("  git push origin master:main")
    
    print("=" * 60)
