#!/usr/bin/env python3
"""
Generate Full Website - High Standard Design
Modern UI/UX with professional layout
"""

import json
from datetime import datetime

def load_data():
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    try:
        with open('commodity_news.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except:
        news = {'news': [], 'last_update': 'N/A', 'source': 'SMM'}
    
    try:
        with open('commodity_analysis.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except:
        analysis = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'summary': {
                'total_commodities': len(prices['commodities']),
                'market_sentiment': 'N/A',
                'up_count': 0,
                'down_count': 0,
                'stable_count': 0,
                'real_data_ratio': 100
            },
            'top_performers': {'gainers': [], 'losers': []}
        }
    
    return prices, news, analysis

def generate_css():
    return """
:root {
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --success: #10b981;
    --danger: #ef4444;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-2xl: 1.5rem;
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
    background: linear-gradient(135deg, var(--gray-50), var(--gray-100));
    color: var(--gray-800);
    line-height: 1.6;
    min-height: 100vh;
}

/* Header */
.header {
    position: sticky;
    top: 0;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--gray-200);
    box-shadow: var(--shadow-md);
    z-index: 1000;
    padding: var(--spacing-md) 0;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--spacing-md);
}

.header-brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.header-icon {
    font-size: 1.75rem;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gray-900);
}

.header-stats {
    display: flex;
    gap: var(--spacing-sm);
}

.stat-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--gray-100);
    border-radius: var(--radius-md);
    font-size: 0.75rem;
    font-weight: 500;
}

.stat-badge.real {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    color: #059669;
    border: 1px solid #a7f3d0;
}

/* Navigation */
.nav-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-sm) var(--spacing-md);
}

.commodity-nav {
    display: flex;
    gap: var(--spacing-xs);
    overflow-x: auto;
    scrollbar-width: none;
    padding-bottom: var(--spacing-xs);
}

.commodity-nav::-webkit-scrollbar { display: none; }

.nav-item {
    padding: var(--spacing-xs) var(--spacing-md);
    background: var(--gray-100);
    border-radius: var(--radius-lg);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--gray-700);
    text-decoration: none;
    white-space: nowrap;
    transition: all 150ms ease;
}

.nav-item:hover {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.nav-item.active {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
}

/* Main Content */
.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-2xl) var(--spacing-md);
}

.page { display: none; animation: fadeIn 0.4s ease; }
.page:first-of-type { display: block; }
.page:target { display: block; }
.page:target ~ .page:first-of-type { display: none; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Page Header */
.page-header {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border-radius: var(--radius-2xl);
    padding: var(--spacing-2xl);
    margin-bottom: var(--spacing-xl);
    color: white;
    box-shadow: var(--shadow-xl);
    position: relative;
    overflow: hidden;
}

.page-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 50%;
}

.commodity-info {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--spacing-lg);
    position: relative;
    z-index: 1;
}

.commodity-meta h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: var(--spacing-sm);
    letter-spacing: -0.02em;
}

.commodity-meta .symbol {
    font-size: 1.125rem;
    opacity: 0.9;
    font-weight: 500;
}

.price-display { text-align: right; }

.current-price {
    font-size: 3.5rem;
    font-weight: 800;
    font-family: 'SF Mono', Monaco, Consolas, monospace;
    letter-spacing: -0.02em;
    margin-bottom: var(--spacing-sm);
}

.price-change {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-md);
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border-radius: var(--radius-lg);
    font-size: 1rem;
    font-weight: 600;
}

.price-change.up { background: rgba(16, 185, 129, 0.3); }
.price-change.down { background: rgba(239, 68, 68, 0.3); }

.page-desc {
    margin-top: var(--spacing-lg);
    padding-top: var(--spacing-lg);
    border-top: 1px solid rgba(255,255,255,0.2);
    font-size: 0.9375rem;
    opacity: 0.9;
    position: relative;
    z-index: 1;
}

/* Cards */
.card {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--gray-100);
    transition: all 300ms ease;
}

.card:hover {
    box-shadow: var(--shadow-xl);
    transform: translateY(-4px);
}

.card-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-md);
    border-bottom: 2px solid var(--gray-100);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--gray-900);
}

/* Data Table */
.data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.data-table th {
    background: var(--gray-50);
    color: var(--gray-600);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: var(--spacing-md);
    text-align: left;
    border-bottom: 2px solid var(--gray-200);
}

.data-table td {
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--gray-100);
    font-size: 0.9375rem;
}

.data-table tr:hover td { background: var(--gray-50); }

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-md);
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-up {
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
}

.badge-down {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
}

.badge-real {
    background: #ecfdf5;
    color: #059669;
}

/* News */
.news-list { display: flex; flex-direction: column; gap: var(--spacing-lg); }

.news-item {
    padding: var(--spacing-lg);
    background: var(--gray-50);
    border-radius: var(--radius-lg);
    border: 1px solid var(--gray-200);
    transition: all 300ms ease;
}

.news-item:hover {
    background: white;
    border-color: #bfdbfe;
    transform: translateX(8px);
    box-shadow: var(--shadow-md);
}

.news-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--gray-900);
    margin-bottom: var(--spacing-sm);
    line-height: 1.4;
}

.news-meta {
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
    font-size: 0.875rem;
    color: var(--gray-500);
}

.news-summary {
    color: var(--gray-600);
    line-height: 1.7;
    margin-bottom: var(--spacing-md);
}

.news-link {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 150ms ease;
}

.news-link:hover {
    color: var(--primary-dark);
    gap: var(--spacing-sm);
}

/* Overview Grid */
.overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.overview-card {
    background: linear-gradient(135deg, white, var(--gray-50));
    border-radius: var(--radius-xl);
    padding: var(--spacing-xl);
    text-align: center;
    border: 1px solid var(--gray-200);
    box-shadow: var(--shadow-md);
    transition: all 300ms ease;
}

.overview-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.overview-icon { font-size: 2.5rem; margin-bottom: var(--spacing-sm); }
.overview-label { font-size: 0.875rem; color: var(--gray-500); margin-bottom: var(--spacing-xs); }
.overview-value { font-size: 1.75rem; font-weight: 700; color: var(--gray-900); }
.overview-value.up { color: var(--success); }
.overview-value.down { color: var(--danger); }

/* Rankings */
.ranking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-xl);
}

.ranking-section h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    padding-left: var(--spacing-md);
    border-left: 4px solid currentColor;
}

.ranking-section.gainers h3 { color: var(--success); border-color: var(--success); }
.ranking-section.losers h3 { color: var(--danger); border-color: var(--danger); }

.ranking-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: var(--gray-50);
    border-radius: var(--radius-lg);
    margin-bottom: var(--spacing-sm);
    transition: all 150ms ease;
}

.ranking-item:hover {
    background: white;
    box-shadow: var(--shadow-md);
    transform: translateX(4px);
}

.ranking-rank {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--gray-400);
    min-width: 40px;
    text-align: center;
}

.ranking-info { flex: 1; }
.ranking-name { font-weight: 600; color: var(--gray-900); margin-bottom: var(--spacing-xs); }
.ranking-change { font-size: 0.875rem; font-weight: 600; }
.ranking-change.up { color: var(--success); }
.ranking-change.down { color: var(--danger); }

/* Footer */
.footer {
    margin-top: var(--spacing-2xl);
    padding: var(--spacing-xl) 0;
    border-top: 1px solid var(--gray-200);
    background: var(--gray-50);
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
    text-align: center;
    color: var(--gray-600);
}

.footer-stats {
    display: flex;
    justify-content: center;
    gap: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
    flex-wrap: wrap;
}

.footer-stat { text-align: center; }
.footer-stat-value { font-size: 1.5rem; font-weight: 700; color: var(--primary); }
.footer-stat-label { font-size: 0.75rem; color: var(--gray-500); text-transform: uppercase; }

/* Responsive */
@media (max-width: 768px) {
    .header-content { flex-direction: column; align-items: flex-start; }
    .commodity-meta h1 { font-size: 1.75rem; }
    .current-price { font-size: 2.5rem; }
    .commodity-info { flex-direction: column; }
    .price-display { text-align: left; }
    .overview-grid { grid-template-columns: 1fr; }
    .ranking-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
    .page-header { padding: var(--spacing-lg); }
    .card { padding: var(--spacing-lg); }
    .current-price { font-size: 2rem; }
}
"""

def generate_price_pages(prices):
    pages = []
    for code, item in prices['commodities'].items():
        is_up = item['change'] >= 0
        price_display = 'CNY ' if '元' in item['unit'] else 'USD '
        
        html = f'''
    <div id="{code}" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div class="commodity-meta">
                    <h1>{item['name']}</h1>
                    <div class="symbol">{item['symbol']} / {item['category']}</div>
                </div>
                <div class="price-display">
                    <div class="current-price">{price_display}{item['price']:,}</div>
                    <div class="price-change {'up' if is_up else 'down'}">
                        {'+' if is_up else ''}{item['change']:,} ({'+' if is_up else ''}{item['change_percent']:.2f}%)
                    </div>
                </div>
            </div>
            <div class="page-desc">
                {item['desc']} <span class="badge badge-real">Real Data</span>
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">Price Details</span>
            </div>
            <table class="data-table">
                <thead>
                    <tr><th>Spec</th><th>Price Range</th><th>Avg Price</th><th>Change</th><th>Unit</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>{item['name']} Spot</strong></td>
                        <td>{item['price_range']}</td>
                        <td>{item['price']:,}</td>
                        <td><span class="badge badge-{'up' if is_up else 'down'}">{'+' if is_up else ''}{item['change']:,}</span></td>
                        <td>{item['unit']}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    '''
        pages.append(html)
    return '\n'.join(pages)

def generate_news_page(news):
    if not news.get('news'):
        return '''
    <div id="news" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div class="commodity-meta">
                    <h1>Commodity News</h1>
                    <div class="symbol">Daily Market Updates / Industry News</div>
                </div>
            </div>
        </div>
        <div class="card"><p>News updating...</p></div>
    </div>
    '''
    
    items = []
    for item in news['news']:
        items.append(f'''
            <div class="news-item">
                <div class="news-title">{item['title']}</div>
                <div class="news-meta">
                    <span>{item['date']}</span>
                    <span>{item['category']}</span>
                    <span>{item['source']}</span>
                </div>
                <div class="news-summary">{item['summary']}</div>
                <a href="{item['url']}" target="_blank" class="news-link">Read More</a>
            </div>
        ''')
    
    return f'''
    <div id="news" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div class="commodity-meta">
                    <h1>Commodity News</h1>
                    <div class="symbol">Daily Market Updates / Industry News</div>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">Latest News ({len(news['news'])})</span>
            </div>
            <div class="news-list">{''.join(items)}</div>
        </div>
    </div>
    '''

def generate_analysis_page(analysis):
    summary = analysis['summary']
    
    gainers = ''
    if analysis['top_performers']['gainers']:
        for i, g in enumerate(analysis['top_performers']['gainers'], 1):
            gainers += f'<div class="ranking-item"><div class="ranking-rank">#{i}</div><div class="ranking-info"><div class="ranking-name">{g["name"]}</div><div class="ranking-change up">+{g["total_change_percent"]:.2f}%</div></div><div>{g["current_price"]:,}</div></div>'
    
    losers = ''
    if analysis['top_performers']['losers']:
        for i, l in enumerate(analysis['top_performers']['losers'], 1):
            losers += f'<div class="ranking-item"><div class="ranking-rank">#{i}</div><div class="ranking-info"><div class="ranking-name">{l["name"]}</div><div class="ranking-change down">{l["total_change_percent"]:.2f}%</div></div><div>{l["current_price"]:,}</div></div>'
    
    return f'''
    <div id="analysis" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div class="commodity-meta">
                    <h1>Market Analysis</h1>
                    <div class="symbol">Market Insights / Trend Analysis</div>
                </div>
            </div>
        </div>
        <div class="overview-grid">
            <div class="overview-card">
                <div class="overview-icon">Trend</div>
                <div class="overview-label">Market Sentiment</div>
                <div class="overview-value">{summary['market_sentiment']}</div>
            </div>
            <div class="overview-card">
                <div class="overview-icon">Data</div>
                <div class="overview-label">Real Data Ratio</div>
                <div class="overview-value">{summary['real_data_ratio']:.0f}%</div>
            </div>
            <div class="overview-card">
                <div class="overview-icon">Up</div>
                <div class="overview-label">Rising</div>
                <div class="overview-value up">{summary['up_count']}</div>
            </div>
            <div class="overview-card">
                <div class="overview-icon">Down</div>
                <div class="overview-label">Falling</div>
                <div class="overview-value down">{summary['down_count']}</div>
            </div>
        </div>
        <div class="ranking-grid">
            <div class="ranking-section gainers">
                <h3>Top Gainers</h3>
                {gainers if gainers else '<p>No data</p>'}
            </div>
            <div class="ranking-section losers">
                <h3>Top Losers</h3>
                {losers if losers else '<p>No data</p>'}
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">Statistics</span>
            </div>
            <table class="data-table">
                <thead><tr><th>Metric</th><th>Value</th><th>Notes</th></tr></thead>
                <tbody>
                    <tr><td>Total Commodities</td><td>{summary['total_commodities']}</td><td>12 categories</td></tr>
                    <tr><td>Rising</td><td>{summary['up_count']}</td><td>Price up today</td></tr>
                    <tr><td>Falling</td><td>{summary['down_count']}</td><td>Price down today</td></tr>
                    <tr><td>Stable</td><td>{summary['stable_count']}</td><td>No significant change</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    '''

def generate_nav_items(prices):
    items = [f'<a href="#{code}" class="nav-item">{item["name"]}</a>' for code, item in prices['commodities'].items()]
    items.extend(['<a href="#news" class="nav-item">News</a>', '<a href="#analysis" class="nav-item">Analysis</a>'])
    return '\n'.join(items)

def main():
    print("Generating high-standard website design...")
    
    prices, news, analysis = load_data()
    print(f"Prices: {len(prices['commodities'])} commodities")
    print(f"News: {len(news.get('news', []))} articles")
    
    css = generate_css()
    price_pages = generate_price_pages(prices)
    news_page = generate_news_page(news)
    analysis_page = generate_analysis_page(analysis)
    nav_items = generate_nav_items(prices)
    
    real_count = sum(1 for item in prices['commodities'].values() if item.get('is_real', False))
    total_count = len(prices['commodities'])
    real_percent = (real_count / total_count * 100) if total_count > 0 else 0
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commodity Monitor - Prices + News + Analysis</title>
    <style>{css}</style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-brand">
                <span class="header-icon">CM</span>
                <div>
                    <div class="header-title">Commodity Monitor</div>
                </div>
            </div>
            <div class="header-stats">
                <span class="stat-badge real">Real Data: {real_count}/{total_count}</span>
            </div>
        </div>
        <div class="nav-wrapper">
            <nav class="commodity-nav">
                {nav_items}
            </nav>
        </div>
    </header>
    
    <main class="main-content">
        {price_pages}
        {news_page}
        {analysis_page}
    </main>
    
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-stats">
                <div class="footer-stat"><div class="footer-stat-value">{real_percent:.0f}%</div><div class="footer-stat-label">Real Data</div></div>
                <div class="footer-stat"><div class="footer-stat-value">{total_count}</div><div class="footer-stat-label">Commodities</div></div>
                <div class="footer-stat"><div class="footer-stat-value">{len(news.get('news', []))}</div><div class="footer-stat-label">News</div></div>
            </div>
            <p>2026 Commodity Monitor | Data: {prices['data_source']}</p>
            <p>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </footer>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\nGenerated: index.html")
    print(f"Real data: {real_count}/{total_count} ({real_percent:.0f}%)")
    print("\nDesign features:")
    print("  - Modern gradient colors")
    print("  - Card-based layout")
    print("  - Hover animations")
    print("  - Responsive design")
    print("  - Glass morphism effects")

if __name__ == '__main__':
    main()
