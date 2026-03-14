#!/usr/bin/env python3
"""
生成完整网站 - 价格 + 新闻 + 数据分析
"""

import json
import os
from datetime import datetime

def load_data():
    """加载所有数据"""
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    try:
        with open('commodity_news.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except FileNotFoundError:
        news = {'news': [], 'last_update': '未更新', 'source': 'SMM'}
    
    try:
        with open('commodity_analysis.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        # 如果没有分析数据，生成一个
        analysis = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'summary': {
                'total_commodities': len(prices['commodities']),
                'market_sentiment': '未知',
                'market_volatility': '未知',
                'up_count': 0,
                'down_count': 0,
                'stable_count': 0,
                'real_data_ratio': 0
            },
            'top_performers': {'gainers': [], 'losers': []},
            'commodity_analysis': []
        }
    
    return prices, news, analysis

def generate_price_pages(prices):
    """生成商品价格页面"""
    pages = []
    
    for code, item in prices['commodities'].items():
        is_up = item['change'] >= 0
        price_display = '¥' if '元' in item['unit'] else '$'
        real_badge = "✅ 真实数据" if item.get('is_real', False) else "⚠️ 模拟数据"
        badge_class = 'badge-up' if item.get('is_real', False) else 'badge-down'
        
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
                    <td><span class="badge {badge_class}">{real_badge}</span></td>
                </tr>
            </table>
        </div>
        <div class="footer">
            <p>🔍 数据来源：{prices['data_source']}</p>
            <p>🔄 更新时间：{prices['last_update']} | {real_badge}</p>
        </div>
    </div>
    '''
        pages.append(html)
    
    return '\n'.join(pages)

def generate_news_page(news):
    """生成新闻页面"""
    if not news.get('news'):
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
    for i, news_item in enumerate(news['news'], 1):
        news_items_html.append(f'''
            <div class="news-item">
                <div class="news-title">{i}. {news_item['title']}</div>
                <div class="news-meta">📅 {news_item['date']} | 📍 {news_item['category']} | 🏷️ {news_item['source']}</div>
                <div class="news-summary">{news_item['summary']}</div>
                <a href="{news_item['url']}" target="_blank" class="news-link">阅读原文 →</a>
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
            <div class="section-title">📰 今日新闻 ({len(news['news'])}条)</div>
            {news_html}
        </div>
        <div class="footer">
            <p>🔍 新闻来源：{news.get('source', 'SMM上海有色网')}</p>
            <p>🔄 更新时间：{news.get('last_update', '未更新')}</p>
        </div>
    </div>
    '''

def generate_analysis_page(analysis):
    """生成数据分析页面"""
    summary = analysis['summary']
    
    # 生成涨幅前三HTML
    gainers_html = ''
    if analysis['top_performers']['gainers']:
        for i, gainer in enumerate(analysis['top_performers']['gainers'], 1):
            gainers_html += f'''
                <div class="analysis-item">
                    <div class="analysis-rank">#{i}</div>
                    <div class="analysis-details">
                        <div class="analysis-name">{gainer['name']}</div>
                        <div class="analysis-change up">+{gainer['total_change_percent']:.2f}%</div>
                    </div>
                    <div class="analysis-price">当前: {gainer['current_price']:,}</div>
                </div>
            '''
    else:
        gainers_html = '<p>暂无涨幅数据</p>'
    
    # 生成跌幅前三HTML
    losers_html = ''
    if analysis['top_performers']['losers']:
        for i, loser in enumerate(analysis['top_performers']['losers'], 1):
            losers_html += f'''
                <div class="analysis-item">
                    <div class="analysis-rank">#{i}</div>
                    <div class="analysis-details">
                        <div class="analysis-name">{loser['name']}</div>
                        <div class="analysis-change down">{loser['total_change_percent']:.2f}%</div>
                    </div>
                    <div class="analysis-price">当前: {loser['current_price']:,}</div>
                </div>
            '''
    else:
        losers_html = '<p>暂无跌幅数据</p>'
    
    # 市场情绪图标
    sentiment_icon = '📈' if summary['market_sentiment'] == '乐观' else '📉' if summary['market_sentiment'] == '悲观' else '📊'
    volatility_icon = '🌪️' if summary['market_volatility'] == '高' else '🌊' if summary['market_volatility'] == '中' else '🌊'
    
    return f'''
    <div id="analysis" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">数据分析报告</div>
                    <div class="commodity-symbol">市场洞察 | 趋势分析 | 投资参考</div>
                </div>
            </div>
            <p>基于历史数据的深度分析和市场洞察</p>
        </div>
        
        <div class="section">
            <div class="section-title">📈 市场概况</div>
            <div class="market-overview">
                <div class="overview-item">
                    <div class="overview-icon">{sentiment_icon}</div>
                    <div class="overview-content">
                        <div class="overview-title">市场情绪</div>
                        <div class="overview-value {summary['market_sentiment']}">{summary['market_sentiment']}</div>
                    </div>
                </div>
                <div class="overview-item">
                    <div class="overview-icon">{volatility_icon}</div>
                    <div class="overview-content">
                        <div class="overview-title">市场波动</div>
                        <div class="overview-value">{summary['market_volatility']}</div>
                    </div>
                </div>
                <div class="overview-item">
                    <div class="overview-icon">📊</div>
                    <div class="overview-content">
                        <div class="overview-title">真实数据</div>
                        <div class="overview-value">{summary['real_data_ratio']}%</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🏆 今日表现排行</div>
            <div class="performance-grid">
                <div class="performance-col">
                    <h3>📈 涨幅前三</h3>
                    {gainers_html}
                </div>
                <div class="performance-col">
                    <h3>📉 跌幅前三</h3>
                    {losers_html}
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 详细统计</div>
            <table class="stats-table">
                <tr><th>指标</th><th>数值</th><th>说明</th></tr>
                <tr><td>监控商品总数</td><td>{summary['total_commodities']} 种</td><td>覆盖12个大宗商品类别</td></tr>
                <tr><td>上涨商品</td><td>{summary['up_count']} 种</td><td>今日价格上涨</td></tr>
                <tr><td>下跌商品</td><td>{summary['down_count']} 种</td><td>今日价格下跌</td></tr>
                <tr><td>持平商品</td><td>{summary['stable_count']} 种</td><td>价格无明显变化</td></tr>
                <tr><td>数据覆盖天数</td><td>{len(analysis.get('commodity_analysis', []))} 天</td><td>历史数据积累</td></tr>
            </table>
        </div>
        
        <div class="footer">
            <p>🔍 分析报告日期：{analysis['report_date']}</p>
            <p>📈 基于 {summary['total_commodities']} 种商品的历史价格数据分析</p>
            <p>🔄 数据来源：SMM上海有色网 + 历史数据库</p>
        </div>
    </div>
    '''

def generate_nav_items(prices):
    """生成导航项"""
    nav_items = []
    
    # 商品导航
    for code, item in prices['commodities'].items():
        nav_items.append(f'<a href="#{code}" class="nav-item">{item["name"]}</a>')
    
    # 新闻导航
    nav_items.append('<a href="#news" class="nav-item">📰 新闻</a>')
    
    # 数据分析导航
    nav_items.append('<a href="#analysis" class="nav-item">📈 分析</a>')
    
    return '\n'.join(nav_items)

def main():
    print("生成完整网站（价格 + 新闻 + 数据分析）...")
    
    # 加载数据
    prices, news, analysis = load_data()
    
    print(f"价格数据: {len(prices['commodities'])} 种商品")
    print(f"新闻数据: {len(news.get('news', []))} 条新闻")
    print(f"分析数据: {analysis['summary']['total_commodities']} 种商品分析")
    
    # 生成各部分
    price_pages = generate_price_pages(prices)
    news_page = generate_news_page(news)
    analysis_page = generate_analysis_page(analysis)
    nav_items = generate_nav_items(prices)
    
    # 统计
    real_count = sum(1 for item in prices['commodities'].values() if item.get('is_real', False))
    total_count = len(prices['commodities'])
    real_percent = (real_count / total_count * 100) if total_count > 0 else 0
    
    # 生成完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大宗商品监控系统 - 价格 + 新闻 + 数据分析</title>
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
        .market-overview {{ display: flex; gap: 16px; margin-bottom: 20px; }}
        .overview-item {{ flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }}
        .overview-icon {{ font-size: 24px; margin-bottom: 8px; }}
        .overview-title {{ font-size: 12px; color: #718096; margin-bottom: 4px; }}
        .overview-value {{ font-size: 18px; font-weight: 700; }}
        .overview-value.乐观 {{ color: #276749; }}
        .overview-value.悲观 {{ color: #c53030; }}
        .performance-grid {{ display: flex; gap: 20px; }}
        .performance-col {{ flex: 1; }}
        .analysis-item {{ display: flex; align-items: center; padding: 12px; background: white; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 8px; }}
        .analysis-rank {{ font-size: 14px; font-weight: 700; color: #718096; margin-right: 12px; min-width: 30px; }}
        .analysis-details {{ flex: 1; }}
        .analysis-name {{ font-size: 14px; font-weight: 600; color: #1a365d; }}
        .analysis-change {{ font-size: 12px; font-weight: 600; }}
        .analysis-change.up {{ color: #276749; }}
        .analysis-change.down {{ color: #c53030; }}
        .analysis-price {{ font-size: 12px; color: #718096; }}
        .stats-table th, .stats-table td {{ padding: 10px; }}
        .footer {{ text-align: center; padding: 16px; color: #718096; font-size: 12px; }}
        .stats {{ font-size: 11px; background: #f8fafc; padding: 8px; border-radius: 5px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">📊 大宗商品监控系统</div>
        <div class="current-time">
            数据更新: {prices['last_update']} 
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
        {analysis_page}
    </div>
    <div class="footer">
        <div class="stats">
            <p>📈 数据统计: 真实数据占比 {real_percent:.1f}% | 总商品数: {total_count} | 新闻数: {len(news.get('news', []))} | 分析报告: {analysis['report_date']}</p>
            <p>🔧 系统版本: V2.2 (完整版) | 包含价格监控 + 动态新闻 + 数据分析</p>
        </div>
        <p>© 2026 大宗商品监控系统 | 数据来源: {prices['data_source']} + {news.get('source', 'SMM新闻')}</p>
        <p>🔄 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>'''
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] 完整网站已生成: index.html")
    print(f"[INFO] 真实数据: {real_count}/{total_count} ({real_percent:.1f}%)")
    print(f"[INFO] 新闻数量: {len(news.get('news', []))}")
    print(f"[INFO] 市场情绪: {analysis['summary']['market_sentiment']}")
    print(f"[INFO] 网站包含三个主要页面: 价格监控、新闻、数据分析")
    
    return True

if __name__ == '__main__':
    main()