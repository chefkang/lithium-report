#!/usr/bin/env python3
"""
生成包含新闻的完整网站
"""

import json
import os
from datetime import datetime

def load_prices():
    """加载价格数据"""
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_news():
    """加载新闻数据"""
    try:
        with open('commodity_news.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'news': [], 'last_update': '未更新', 'source': 'SMM'}

def generate_price_pages(db):
    """生成商品价格页面"""
    pages = []
    
    for code, item in db['commodities'].items():
        is_up = item['change'] >= 0
        price_display = '¥' if '元' in item['unit'] else '$'
        
        # 数据真实性标记
        real_badge = "✅ 真实数据" if item.get('is_real', False) else "⚠️ 模拟数据"
        
        html = f'''
    <div id="{code}" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">{item['name']}</div>
                    <div class="commodity-symbol">{item['symbol']} | {item['category']}</div>
                </div>
                <div class="price-display">
                    <div class="current-price">{price_display}{item['price']:,}</div>
                    <div class="price-change {'up' if is_up else 'down'}">{'▲' if is_up else '▼'} {abs(item['change']):,} ({'+' if is_up else ''}{item['change_percent']:.2f}%)</div>
                </div>
            </div>
            <p>{item['desc']} | {real_badge}</p>
        </div>
        <div class="section">
            <div class="section-title">📊 今日价格详情</div>
            <table>
                <tr><th>规格</th><th>价格区间</th><th>均价</th><th>涨跌</th><th>单位</th><th>数据状态</th></tr>
                <tr>
                    <td><strong>{item['name']}现货</strong></td>
                    <td>{item['price_range']}</td>
                    <td>{item['price']:,}</td>
                    <td><span class="badge {'badge-up' if is_up else 'badge-down'}">{'+' if is_up else ''}{item['change']:,}</span></td>
                    <td>{item['unit']}</td>
                    <td><span class="badge {'badge-up' if item.get('is_real', False) else 'badge-down'}">{real_badge}</span></td>
                </tr>
            </table>
        </div>
        <div class="footer">
            <p>🔍 数据来源：{db['data_source']}</p>
            <p>🔄 更新时间：{db['last_update']} | {real_badge}</p>
        </div>
    </div>
    '''
        pages.append(html)
    
    return '\n'.join(pages)

def generate_news_page(news_data):
    """生成新闻页面"""
    if not news_data.get('news'):
        return '''
    <div id="news" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">大宗商品新闻</div>
                    <div class="commodity-symbol">每日市场动态 | 行业资讯</div>
                </div>
            </div>
            <p>暂无最新新闻，请稍后查看...</p>
        </div>
        <div class="section">
            <div class="section-title">📰 新闻更新中</div>
            <p>新闻数据正在更新，请稍后刷新页面。</p>
        </div>
    </div>
    '''
    
    news_items_html = []
    for i, news in enumerate(news_data['news'], 1):
        news_items_html.append(f'''
            <div class="news-item">
                <div class="news-title">{i}. {news['title']}</div>
                <div class="news-meta">📅 {news['date']} | 📍 {news['category']} | 🏷️ {news['source']}</div>
                <div class="news-summary">{news['summary']}</div>
                <a href="{news['url']}" target="_blank" class="news-link">阅读原文 →</a>
            </div>
        ''')
    
    news_html = '\n'.join(news_items_html)
    
    return f'''
    <div id="news" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">大宗商品新闻</div>
                    <div class="commodity-symbol">每日市场动态 | 行业资讯</div>
                </div>
            </div>
            <p>最新市场动态和行业资讯</p>
        </div>
        <div class="section">
            <div class="section-title">📰 今日新闻 ({len(news_data['news'])}条)</div>
            {news_html}
        </div>
        <div class="footer">
            <p>🔍 新闻来源：{news_data.get('source', 'SMM上海有色网')}</p>
            <p>🔄 更新时间：{news_data.get('last_update', '未更新')}</p>
        </div>
    </div>
    '''

def generate_nav_items(db):
    """生成导航项"""
    nav_items = []
    
    # 商品导航
    for code, item in db['commodities'].items():
        nav_items.append(f'<a href="#{code}" class="nav-item">{item["name"]}</a>')
    
    # 新闻导航
    nav_items.append('<a href="#news" class="nav-item">📰 新闻</a>')
    
    return '\n'.join(nav_items)

def main():
    print("生成包含新闻的网站...")
    
    # 加载数据
    db = load_prices()
    news_data = load_news()
    
    print(f"价格数据: {len(db['commodities'])} 种商品")
    print(f"新闻数据: {len(news_data.get('news', []))} 条新闻")
    
    # 生成各部分
    price_pages = generate_price_pages(db)
    news_page = generate_news_page(news_data)
    nav_items = generate_nav_items(db)
    
    # 统计真实数据比例
    real_count = sum(1 for item in db['commodities'].values() if item.get('is_real', False))
    total_count = len(db['commodities'])
    real_percent = (real_count / total_count * 100) if total_count > 0 else 0
    
    # 生成完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大宗商品监控系统 - 价格 + 新闻</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: #f7fafc; margin: 0; padding: 0; }}
        .header {{ position: fixed; top: 0; left: 0; right: 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 1000; padding: 12px 16px; }}
        .header-title {{ font-size: 18px; font-weight: 700; color: #1a365d; }}
        .current-time {{ font-size: 12px; color: #718096; }}
        .data-status {{ font-size: 11px; background: #e2e8f0; padding: 2px 6px; border-radius: 3px; margin-left: 8px; }}
        .data-status.real {{ background: #c6f6d5; color: #276749; }}
        .data-status.sim {{ background: #fed7d7; color: #c53030; }}
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
        .news-item {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; }}
        .news-title {{ font-size: 16px; font-weight: 600; color: #1a365d; margin-bottom: 6px; }}
        .news-meta {{ font-size: 12px; color: #718096; margin-bottom: 8px; }}
        .news-summary {{ font-size: 14px; line-height: 1.5; color: #4a5568; margin-bottom: 10px; }}
        .news-link {{ font-size: 12px; color: #4299e1; text-decoration: none; }}
        .news-link:hover {{ text-decoration: underline; }}
        .footer {{ text-align: center; padding: 16px; color: #718096; font-size: 12px; }}
        .stats {{ font-size: 11px; background: #f8fafc; padding: 8px; border-radius: 5px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">📊 大宗商品监控系统</div>
        <div class="current-time">
            数据更新: {db['last_update']} 
            <span class="data-status real">真实数据: {real_count}/{total_count}</span>
            <span class="data-status sim">模拟数据: {total_count-real_count}/{total_count}</span>
        </div>
        <div class="commodity-nav">
            {nav_items}
        </div>
    </div>
    <div class="main-content">
        {price_pages}
        {news_page}
    </div>
    <div class="footer">
        <div class="stats">
            <p>📈 数据统计: 真实数据占比 {real_percent:.1f}% | 总商品数: {total_count} | 新闻数: {len(news_data.get('news', []))}</p>
            <p>🔧 系统版本: V2.1 (增强版) | 包含价格监控 + 动态新闻</p>
        </div>
        <p>© 2026 大宗商品监控系统 | 数据来源: {db['data_source']} + {news_data.get('source', 'SMM新闻')}</p>
        <p>🔄 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>'''
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] 网站已生成: index.html")
    print(f"[INFO] 真实数据: {real_count}/{total_count} ({real_percent:.1f}%)")
    print(f"[INFO] 新闻数量: {len(news_data.get('news', []))}")
    print(f"[INFO] 网站包含新闻页面，可通过导航栏访问")
    
    return True

if __name__ == '__main__':
    main()