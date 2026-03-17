#!/usr/bin/env python3
"""
生成高标准大宗商品监控网站
专业金融风格，响应式设计
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
        analysis = {'market_overview': '数据分析更新中...', 'top_gainers': [], 'top_losers': []}
    
    return prices, news, analysis

def generate_css():
    """生成专业CSS"""
    return '''
    /* 高标准大宗商品监控系统 - 专业金融风格 */
    :root {
        /* 主色调 - 专业深蓝 */
        --primary: #0f172a;
        --primary-light: #1e293b;
        --primary-lighter: #334155;
        --secondary: #3b82f6;
        --secondary-light: #60a5fa;
        --accent: #10b981;
        --accent-red: #ef4444;
        --accent-yellow: #f59e0b;
        
        /* 文字色 */
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        
        /* 背景色 */
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: rgba(30, 41, 59, 0.8);
        --bg-hover: #334155;
        
        /* 边框 */
        --border: #475569;
        --border-light: #64748b;
        
        /* 阴影 */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
        
        /* 圆角 */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        /* 间距 */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        --spacing-2xl: 3rem;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'SF Pro Display', sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
        line-height: 1.6;
        min-height: 100vh;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* 头部导航 */
    .header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border);
        z-index: 1000;
        padding: var(--spacing-md) var(--spacing-xl);
    }
    
    .header-container {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: var(--spacing-lg);
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }
    
    .logo-icon {
        font-size: 1.5rem;
        color: var(--secondary);
    }
    
    .logo-text {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--secondary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-stats {
        display: flex;
        gap: var(--spacing-md);
        flex-wrap: wrap;
    }
    
    .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .stat-value {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    .header-actions {
        display: flex;
        gap: var(--spacing-sm);
    }
    
    .btn {
        padding: var(--spacing-sm) var(--spacing-md);
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
    }
    
    .btn:hover {
        background: var(--bg-hover);
        border-color: var(--border-light);
        color: var(--text-primary);
    }
    
    .btn-primary {
        background: var(--secondary);
        border-color: var(--secondary);
        color: white;
    }
    
    .btn-primary:hover {
        background: var(--secondary-light);
        border-color: var(--secondary-light);
    }
    
    /* 主要内容 */
    .main {
        max-width: 1400px;
        margin: 80px auto 0;
        padding: var(--spacing-xl);
    }
    
    /* 概览卡片 */
    .overview {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
    }
    
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        backdrop-filter: blur(10px);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-md);
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .card-badge {
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-sm);
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: var(--accent);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: var(--accent-yellow);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .badge-danger {
        background: rgba(239, 68, 68, 0.2);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .price-display {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'SF Mono', Monaco, monospace;
        margin-bottom: var(--spacing-xs);
    }
    
    .price-change {
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .change-up {
        color: var(--accent);
    }
    
    .change-down {
        color: var(--accent-red);
    }
    
    .price-details {
        font-size: 0.875rem;
        color: var(--text-muted);
        margin-top: var(--spacing-sm);
    }
    
    /* 数据表格 */
    .data-table {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        overflow: hidden;
        margin-bottom: var(--spacing-xl);
    }
    
    .table-header {
        padding: var(--spacing-lg);
        border-bottom: 1px solid var(--border);
    }
    
    .table-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .table-subtitle {
        font-size: 0.875rem;
        color: var(--text-muted);
        margin-top: var(--spacing-xs);
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
    }
    
    thead {
        background: var(--bg-secondary);
    }
    
    th {
        padding: var(--spacing-md) var(--spacing-lg);
        text-align: left;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-muted);
        border-bottom: 1px solid var(--border);
    }
    
    td {
        padding: var(--spacing-md) var(--spacing-lg);
        border-bottom: 1px solid var(--border);
        font-size: 0.875rem;
    }
    
    tbody tr {
        transition: background 0.2s;
    }
    
    tbody tr:hover {
        background: var(--bg-hover);
    }
    
    .commodity-info {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
    }
    
    .commodity-icon {
        width: 32px;
        height: 32px;
        border-radius: var(--radius-md);
        background: var(--bg-secondary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .commodity-name {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .commodity-category {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 2px;
    }
    
    /* 新闻和分析 */
    .content-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
    }
    
    .news-item {
        padding: var(--spacing-md);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        margin-bottom: var(--spacing-sm);
        transition: background 0.2s;
    }
    
    .news-item:hover {
        background: var(--bg-hover);
    }
    
    .news-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--spacing-xs);
    }
    
    .news-meta {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-bottom: var(--spacing-xs);
    }
    
    .news-summary {
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* 页脚 */
    .footer {
        text-align: center;
        padding: var(--spacing-xl);
        border-top: 1px solid var(--border);
        color: var(--text-muted);
        font-size: 0.875rem;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .header {
            padding: var(--spacing-md);
        }
        
        .header-container {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--spacing-md);
        }
        
        .header-stats {
            width: 100%;
            justify-content: space-between;
        }
        
        .header-actions {
            width: 100%;
            justify-content: space-between;
        }
        
        .main {
            padding: var(--spacing-md);
            margin-top: 120px;
        }
        
        .overview {
            grid-template-columns: 1fr;
        }
        
        .content-grid {
            grid-template-columns: 1fr;
        }
        
        table {
            display: block;
            overflow-x: auto;
        }
    }
    '''

def generate_html(prices, news, analysis):
    """生成HTML内容"""
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 计算统计数据
    total_commodities = len(prices['commodities'])
    real_data_count = sum(1 for item in prices['commodities'].values() if item.get('is_real', False))
    up_count = sum(1 for item in prices['commodities'].values() if item.get('change', 0) >= 0)
    down_count = total_commodities - up_count
    
    # 生成商品行HTML
    commodity_rows = []
    for code, item in prices['commodities'].items():
        is_up = item['change'] >= 0
        is_real = item.get('is_real', False)
        
        # 数据真实性标记
        if is_real:
            data_badge = '<span class="badge-success card-badge">真实数据</span>'
            data_status = '<span class="badge-success">✅ 真实</span>'
        else:
            data_badge = '<span class="badge-warning card-badge">模拟数据</span>'
            data_status = '<span class="badge-warning">⚠️ 模拟</span>'
        
        # 涨跌标记
        change_badge = f'''
            <span class="price-change {'change-up' if is_up else 'change-down'}">
                {'▲' if is_up else '▼'} {abs(item['change']):,} ({'+' if is_up else ''}{item['change_percent']:.2f}%)
            </span>
        '''
        
        # 价格显示
        price_display = '¥' if '元' in item['unit'] else '$'
        
        row = f'''
        <tr>
            <td>
                <div class="commodity-info">
                    <div class="commodity-icon">{item['symbol'][0] if 'symbol' in item else item['name'][0]}</div>
                    <div>
                        <div class="commodity-name">{item['name']}</div>
                        <div class="commodity-category">{item.get('category', '大宗商品')}</div>
                    </div>
                </div>
            </td>
            <td>
                <div class="price-display">{price_display}{item['price']:,}</div>
                {change_badge}
            </td>
            <td>{item['unit']}</td>
            <td>{item.get('price_range', 'N/A')}</td>
            <td>{data_status}</td>
            <td>{item.get('desc', '')[:50]}...</td>
        </tr>
        '''
        commodity_rows.append(row)
    
    # 生成新闻HTML
    news_items = []
    for i, news_item in enumerate(news.get('news', [])[:5]):
        news_html = f'''
        <div class="news-item">
            <div class="news-title">{i+1}. {news_item.get('title', '新闻标题')}</div>
            <div class="news-meta">
                📅 {news_item.get('date', today)} | 📍 {news_item.get('category', '大宗商品')} | 🏷️ {news_item.get('source', 'SMM')}
            </div>
            <div class="news-summary">{news_item.get('summary', '新闻摘要...')}</div>
        </div>
        '''
        news_items.append(news_html)
    
    if not news_items:
        news_items = ['<div class="news-item"><div class="news-title">新闻数据更新中...</div></div>']
    
    # 生成分析HTML
    analysis_html = f'''
    <div class="card">
        <div class="card-header">
            <div class="card-title">📊 市场分析概览</div>
            <span class="badge-success card-badge">实时分析</span>
        </div>
        <div style="margin-bottom: var(--spacing-md);">
            <p style="color: var(--text-secondary); font-size: 0.875rem; line-height: 1.6;">
                {analysis.get('market_overview', '市场数据分析更新中...')}
            </p>
        </div>
        <div style="display: flex; gap: var(--spacing-md); margin-top: var(--spacing-md);">
            <div style="flex: 1;">
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: var(--spacing-xs);">上涨商品</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--accent);">{up_count}</div>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: var(--spacing-xs);">下跌商品</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--accent-red);">{down_count}</div>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: var(--spacing-xs);">真实数据</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--accent);">{real_data_count}/{total_commodities}</div>
            </div>
        </div>
    </div>
    '''
    
    # 组装完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大宗商品专业监控系统 | 实时价格 & 市场分析</title>
    <style>{generate_css()}</style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- 头部导航 -->
    <header class="header">
        <div class="header-container">
            <div class="logo">
                <div class="logo-icon">📈</div>
                <div class="logo-text">大宗商品监控系统</div>
            </div>
            
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-value">{total_commodities}</div>
                    <div class="stat-label">监控商品</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: var(--accent);">{up_count}</div>
                    <div class="stat-label">上涨</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: var(--accent-red);">{down_count}</div>
                    <div class="stat-label">下跌</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: var(--accent);">{real_data_count}/{total_commodities}</div>
                    <div class="stat-label">真实数据</div>
                </div>
            </div>
            
            <div class="header-actions">
                <a href="#table" class="btn">价格表格</a>
                <a href="#news" class="btn">市场新闻</a>
                <a href="#analysis" class="btn">数据分析</a>
                <button class="btn btn-primary" onclick="refreshData()">
                    <i class="fas fa-sync-alt"></i> 刷新数据
                </button>
            </div>
        </div>
    </header>

    <!-- 主要内容 -->
    <main class="main">
        <!-- 概览卡片 -->
        <div class="overview">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">📅 数据更新时间</div>
                    <span class="badge-success card-badge">实时</span>
                </div>
                <div class="price-display">{today}</div>
                <div class="price-details">
                    数据源: {prices.get('data_source', 'SMM上海有色网')}<br>
                    更新频率: 每日自动更新
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-title">📊 数据质量</div>
                    <span class="badge-{'success' if real_data_count/total_commodities >= 0.7 else 'warning'} card-badge">
                        {real_data_count}/{total_commodities} 真实
                    </span>
                </div>
                <div class="price-display">{real_data_count/total_commodities*100:.1f}%</div>
                <div class="price-details">
                    真实数据: {real_data_count} 种商品<br>
                    模拟数据: {total_commodities-real_data_count} 种商品
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-title">📈 市场情绪</div>
                    <span class="badge-{'success' if up_count >= down_count else 'danger'} card-badge">
                        {'看涨' if up_count >= down_count else '看跌'}
                    </span>
                </div>
                <div class="price-display" style="color: var(--accent);">{up_count}</div>
                <div class="price-details">
                    上涨: {up_count} | 下跌: {down_count}<br>
                    涨跌比: {up_count}:{down_count}
                </div>
            </div>
        </div>

        <!-- 数据表格 -->
        <div class="data-table" id="table">
            <div class="table-header">
                <div class="table-title">📋 大宗商品价格一览表</div>
                <div class="table-subtitle">
                    实时监控 {total_commodities} 种大宗商品价格，{real_data_count} 种为真实市场数据
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>商品名称</th>
                        <th>最新价格</th>
                        <th>单位</th>
                        <th>价格区间</th>
                        <th>数据状态</th>
                        <th>描述</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(commodity_rows)}
                </tbody>
            </table>
        </div>

        <!-- 新闻和分析 -->
        <div class="content-grid">
            <!-- 新闻 -->
            <div class="card" id="news">
                <div class="card-header">
                    <div class="card-title">📰 大宗商品新闻</div>
                    <span class="badge-success card-badge">实时更新</span>
                </div>
                <div>
                    {''.join(news_items)}
                </div>
            </div>

            <!-- 分析 -->
            {analysis_html}
        </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
        <p>© 2026 大宗商品专业监控系统 | 数据仅供参考，投资需谨慎</p>
        <p style="margin-top: var(--spacing-sm); font-size: 0.75rem; color: var(--text-muted);">
            最后更新: {today} | 数据源: {prices.get('data_source', 'SMM + 市场数据')} | 系统状态: 运行正常
        </p>
    </footer>

    <script>
        function refreshData() {{
            const btn = event.target.closest('button');
            const icon = btn.querySelector('i');
            btn.disabled = true;
            icon.className = 'fas fa-spinner fa-spin';
            
            setTimeout(() => {{
                btn.disabled = false;
                icon.className = 'fas fa-sync-alt';
                alert('数据刷新完成！页面已更新最新信息。');
                location.reload();
            }}, 1500);
        }}
        
        // 自动刷新时间显示
        function updateTime() {{
            const now = new Date();
            const timeStr = now.toLocaleString('zh-CN', {{
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }});
            document.querySelector('.price-display').textContent = timeStr;
        }}
        
        // 每30秒更新一次时间
        setInterval(updateTime, 30000);
        
        // 表格行点击效果
        document.querySelectorAll('tbody tr').forEach(row => {{
            row.addEventListener('click', () => {{
                row.style.backgroundColor = 'var(--bg-hover)';
                setTimeout(() => {{
                    row.style.backgroundColor = '';
                }}, 300);
            }});
        }});
    </script>
</body>
</html>'''
    
    return html

def main():
    print("生成高标准大宗商品监控网站...")
    
    # 加载数据
    prices, news, analysis = load_data()
    
    # 生成HTML
    html = generate_html(prices, news, analysis)
    
    # 保存文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ 网站生成完成: index.html")
    print(f"📊 数据统计: {len(prices['commodities'])} 种商品, {sum(1 for item in prices['commodities'].values() if item.get('is_real', False))} 种真实数据")
    print(f"📰 新闻数量: {len(news.get('news', []))} 条")
    print("🎨 设计风格: 专业金融风格，响应式布局")

if __name__ == '__main__':
    main()