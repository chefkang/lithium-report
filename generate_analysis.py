#!/usr/bin/env python3
"""
生成大宗商品数据分析报告
"""

import json
from datetime import datetime, timedelta

def load_data():
    """加载价格数据和新闻数据"""
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        price_db = json.load(f)
    
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        today_prices = json.load(f)
    
    try:
        with open('commodity_news.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except FileNotFoundError:
        news = {'news': []}
    
    return price_db, today_prices, news

def analyze_price_trends(price_db):
    """分析价格趋势"""
    analysis = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_commodities': len(price_db['commodities']),
        'trends': [],
        'top_gainers': [],
        'top_losers': [],
        'market_sentiment': '中性',
        'volatility': '低'
    }
    
    # 分析每种商品的趋势
    for code, commodity in price_db['commodities'].items():
        if len(commodity['price_history']) >= 2:
            history = commodity['price_history']
            latest = history[-1]
            oldest = history[0]
            
            # 计算总体变化
            if 'price' in latest and 'price' in oldest:
                total_change = latest['price'] - oldest['price']
                total_change_percent = (total_change / oldest['price']) * 100 if oldest['price'] != 0 else 0
                
                # 计算最近3天的平均波动
                recent_changes = []
                for i in range(1, min(4, len(history))):
                    if 'change_percent' in history[-i]:
                        recent_changes.append(abs(history[-i]['change_percent']))
                
                avg_volatility = sum(recent_changes) / len(recent_changes) if recent_changes else 0
                
                trend = '上涨' if total_change > 0 else '下跌' if total_change < 0 else '持平'
                
                analysis['trends'].append({
                    'name': commodity['name'],
                    'code': code,
                    'current_price': latest.get('price', 0),
                    'total_change': total_change,
                    'total_change_percent': round(total_change_percent, 2),
                    'trend': trend,
                    'volatility': round(avg_volatility, 2),
                    'is_real': latest.get('is_real', False)
                })
    
    # 找出涨跌幅最大的商品
    if analysis['trends']:
        # 涨幅前3
        gainers = sorted([t for t in analysis['trends'] if t['total_change'] > 0], 
                        key=lambda x: x['total_change_percent'], reverse=True)[:3]
        analysis['top_gainers'] = gainers
        
        # 跌幅前3
        losers = sorted([t for t in analysis['trends'] if t['total_change'] < 0], 
                       key=lambda x: x['total_change_percent'])[:3]
        analysis['top_losers'] = losers
        
        # 计算市场情绪
        up_count = sum(1 for t in analysis['trends'] if t['total_change'] > 0)
        down_count = sum(1 for t in analysis['trends'] if t['total_change'] < 0)
        total_count = len(analysis['trends'])
        
        if up_count > total_count * 0.6:
            analysis['market_sentiment'] = '乐观'
        elif down_count > total_count * 0.6:
            analysis['market_sentiment'] = '悲观'
        else:
            analysis['market_sentiment'] = '中性'
        
        # 计算总体波动率
        avg_vol = sum(t['volatility'] for t in analysis['trends']) / total_count if total_count > 0 else 0
        if avg_vol > 3:
            analysis['volatility'] = '高'
        elif avg_vol > 1:
            analysis['volatility'] = '中'
        else:
            analysis['volatility'] = '低'
    
    return analysis

def generate_daily_report(today_prices, analysis, news_data):
    """生成每日分析报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = {
        'report_date': today,
        'summary': {
            'total_commodities': analysis['total_commodities'],
            'market_sentiment': analysis['market_sentiment'],
            'market_volatility': analysis['volatility'],
            'up_count': sum(1 for t in analysis['trends'] if t['total_change'] > 0),
            'down_count': sum(1 for t in analysis['trends'] if t['total_change'] < 0),
            'stable_count': sum(1 for t in analysis['trends'] if t['total_change'] == 0),
            'real_data_ratio': round(sum(1 for t in analysis['trends'] if t['is_real']) / len(analysis['trends']) * 100, 1) if analysis['trends'] else 0
        },
        'top_performers': {
            'gainers': analysis['top_gainers'],
            'losers': analysis['top_losers']
        },
        'commodity_analysis': analysis['trends'],
        'news_summary': {
            'total_news': len(news_data.get('news', [])),
            'by_category': {}
        }
    }
    
    # 按类别统计新闻
    for news_item in news_data.get('news', []):
        category = news_item.get('category', '其他')
        if category not in report['news_summary']['by_category']:
            report['news_summary']['by_category'][category] = 0
        report['news_summary']['by_category'][category] += 1
    
    return report

def save_report(report):
    """保存分析报告"""
    with open('commodity_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分析报告已保存: commodity_analysis.json")
    return True

def print_report_summary(report):
    """打印报告摘要"""
    print("\n" + "=" * 60)
    print("大宗商品数据分析报告")
    print("=" * 60)
    
    summary = report['summary']
    print(f"报告日期: {report['report_date']}")
    print(f"市场概况:")
    print(f"   商品总数: {summary['total_commodities']} 种")
    print(f"   市场情绪: {summary['market_sentiment']}")
    print(f"   市场波动: {summary['market_volatility']}")
    print(f"   上涨: {summary['up_count']} 下跌: {summary['down_count']} 持平: {summary['stable_count']}")
    print(f"   真实数据比例: {summary['real_data_ratio']}%")
    
    if report['top_performers']['gainers']:
        print(f"\n[TOP] 今日涨幅前三:")
        for i, gainer in enumerate(report['top_performers']['gainers'], 1):
            print(f"   {i}. {gainer['name']}: +{gainer['total_change_percent']:.2f}% ({'+' if gainer['total_change'] > 0 else ''}{gainer['total_change']:.2f})")
    
    if report['top_performers']['losers']:
        print(f"\n[DOWN] 今日跌幅前三:")
        for i, loser in enumerate(report['top_performers']['losers'], 1):
            print(f"   {i}. {loser['name']}: {loser['total_change_percent']:.2f}% ({loser['total_change']:.2f})")
    
    print(f"\n[NEWS] 新闻摘要:")
    print(f"   新闻总数: {report['news_summary']['total_news']}")
    for category, count in report['news_summary']['by_category'].items():
        print(f"   - {category}: {count} 条")

def main():
    print("开始生成数据分析报告...")
    
    # 加载数据
    price_db, today_prices, news_data = load_data()
    
    # 分析价格趋势
    analysis = analyze_price_trends(price_db)
    
    # 生成报告
    report = generate_daily_report(today_prices, analysis, news_data)
    
    # 保存报告
    save_report(report)
    
    # 打印摘要
    print_report_summary(report)
    
    print("\n" + "=" * 60)
    print("[OK] 数据分析完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()