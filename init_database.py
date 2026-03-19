#!/usr/bin/env python3
"""初始化价格数据库，生成60天数据"""

import json
from datetime import datetime, timedelta
import random

def init_database():
    """初始化数据库，生成前59天模拟数据 + 今天真实数据"""
    
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for commodity_id, data in db['commodities'].items():
        base_price = data['base_price']
        history = []
        
        # 生成前59天的模拟数据
        current_price = base_price
        for i in range(59):
            date = (datetime.now() - timedelta(days=59-i)).strftime('%Y-%m-%d')
            change = random.uniform(-0.025, 0.025)  # ±2.5%波动
            price = current_price * (1 - change)
            
            history.append({
                'date': date,
                'price': round(price, 2),
                'is_real': False
            })
            current_price = price
        
        # 添加今天的价格（标记为真实数据）
        history.append({
            'date': today,
            'price': base_price,
            'is_real': True
        })
        
        # 保存到数据库
        db['commodities'][commodity_id]['price_history'] = history
        db['commodities'][commodity_id]['daily_records'][today] = {
            'price': base_price,
            'change': 0,
            'change_percent': 0,
            'is_real': True
        }
    
    db['last_update'] = today
    
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Database initialized with 60 days data")
    print(f"  - 59 days: simulated historical data")
    print(f"  - 1 day (today): real data")
    print(f"  - Start recording from: {today}")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Initialize Price Database")
    print("=" * 60)
    init_database()
    print("\n[OK] Now run: uv run python generate_website.py")
    print("=" * 60)
