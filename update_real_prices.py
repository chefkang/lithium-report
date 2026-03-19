#!/usr/bin/env python3
"""
更新 real_prices_today.json 为今日价格（模拟数据）
"""

import json
import random
from datetime import datetime

def update_today_prices():
    # 读取原有数据
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    data['last_update'] = today
    
    # 读取数据库获取昨日价格
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    for code, item in data['commodities'].items():
        if code in db['commodities']:
            history = db['commodities'][code].get('price_history', [])
            if history:
                latest = history[-1]
                old_price = latest['price']
                # 随机波动 -1% 到 +1%
                change_percent = random.uniform(-0.01, 0.01)
                new_price = round(old_price * (1 + change_percent), 2)
                change = new_price - old_price
                # 更新字段
                item['price'] = new_price
                item['change'] = round(change, 2)
                item['change_percent'] = round(change_percent * 100, 2)
                item['date'] = today
                # 价格范围也相应调整（简单模拟）
                if 'price_range' in item and item['price_range']:
                    # 假设范围宽度不变，中心值调整
                    pass  # 保持原样
            else:
                print(f"Warning: No history for {code}")
        else:
            print(f"Warning: {code} not in database")
    
    # 写入文件
    with open('real_prices_today.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Updated real_prices_today.json for {today}")
    return True

if __name__ == '__main__':
    update_today_prices()