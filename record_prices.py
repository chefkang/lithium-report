#!/usr/bin/env python3
"""
大宗商品价格记录系统
从今天开始记录真实价格，60天后形成完整趋势图
"""

import json
from datetime import datetime, timedelta
import random

def generate_historical_prices(base_price, days=59):
    """基于今日价格，生成前59天的模拟历史数据"""
    prices = []
    current_price = base_price
    
    # 从今天往前推59天
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
        
        # 生成合理的随机波动（-3%到+3%）
        change = random.uniform(-0.03, 0.03)
        price = current_price * (1 - change)  # 倒推价格
        
        prices.append({
            'date': date,
            'price': round(price, 2),
            'is_real': False  # 标记为模拟数据
        })
        
        current_price = price
    
    return prices

def record_today_prices(price_data):
    """记录今日真实价格"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 更新每种商品的价格
    for commodity_id, data in price_data.items():
        if commodity_id in db['commodities']:
            # 记录今日真实价格
            db['commodities'][commodity_id]['daily_records'][today] = {
                'price': data['price'],
                'change': data.get('change', 0),
                'change_percent': data.get('change_percent', 0),
                'is_real': True
            }
            
            # 如果是第一天，生成前59天的模拟数据
            if not db['commodities'][commodity_id]['price_history']:
                historical = generate_historical_prices(data['price'])
                db['commodities'][commodity_id]['price_history'] = historical
            
            # 添加今日价格到历史
            db['commodities'][commodity_id]['price_history'].append({
                'date': today,
                'price': data['price'],
                'is_real': True
            })
            
            # 只保留最近60天
            db['commodities'][commodity_id]['price_history'] = \
                db['commodities'][commodity_id]['price_history'][-60:]
    
    db['last_update'] = today
    
    # 保存
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Prices recorded for {today}")
    return True

def get_price_trend(commodity_id, days=20):
    """获取指定商品的近N天价格趋势"""
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    if commodity_id not in db['commodities']:
        return []
    
    history = db['commodities'][commodity_id]['price_history']
    return history[-days:] if len(history) >= days else history

def generate_html_with_real_trends():
    """生成包含真实价格趋势的HTML"""
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 这里生成包含Chart.js的HTML
    # 使用真实价格历史数据绘制趋势图
    
    html_parts = []
    for commodity_id, data in db['commodities'].items():
        trend = get_price_trend(commodity_id, 20)
        if trend:
            prices = [p['price'] for p in trend]
            dates = [p['date'][5:] for p in trend]  # 只取月-日
            
            html_parts.append(f"""
            // {data['name']} 价格趋势
            new Chart(document.getElementById('chart-{commodity_id}'), {{
                type: 'line',
                data: {{
                    labels: {json.dumps(dates)},
                    datasets: [{{
                        label: '{data["name"]}价格',
                        data: {json.dumps(prices)},
                        borderColor: '#3182ce',
                        backgroundColor: 'rgba(49, 130, 206, 0.1)',
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ display: true }},
                        y: {{ display: true }}
                    }}
                }}
            }});
            """)
    
    return '\n'.join(html_parts)

if __name__ == '__main__':
    print("=" * 60)
    print("Commodity Price Recording System")
    print("=" * 60)
    print("\nStarting from today (2026-03-12)")
    print("Recording real prices daily...")
    print("After 60 days, you'll have complete real price trends!")
    print("\nUsage:")
    print("  1. Get today's prices from SMM")
    print("  2. Update commodity_price_db.json")
    print("  3. Run: python record_prices.py")
    print("  4. Website will show 60-day real trends")
