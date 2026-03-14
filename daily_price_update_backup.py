#!/usr/bin/env python3
"""
每日自动抓取SMM首页价格并更新网站
运行时间: 每天09:00
"""

import json
from datetime import datetime
import subprocess

def record_daily_prices():
    """记录每日价格到历史数据库"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 读取今日价格
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        today_data = json.load(f)
    
    # 读取历史数据库
    try:
        with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {'start_date': today, 'last_update': today, 'commodities': {}}
    
    # 更新每种商品的价格历史
    for code, item in today_data['commodities'].items():
        if code not in db['commodities']:
            db['commodities'][code] = {
                'name': item['name'],
                'unit': item['unit'],
                'price_history': []
            }
        
        # 添加今日价格到历史
        db['commodities'][code]['price_history'].append({
            'date': today,
            'price': item['price'],
            'change': item['change'],
            'change_percent': item['change_percent'],
            'is_real': True
        })
        
        # 只保留最近60天
        db['commodities'][code]['price_history'] = \
            db['commodities'][code]['price_history'][-60:]
    
    db['last_update'] = today
    
    # 保存
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] {today} prices recorded to database")
    
    # 生成网站
    subprocess.run(['uv', 'run', 'python', 'generate_real_website.py'], check=True)
    print("[OK] Website generated with latest prices")
    
    # Git推送
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Daily price update - {today}'], check=True)
    subprocess.run(['git', 'push', 'origin', 'master:main'], check=True)
    print(f"[OK] Pushed to GitHub: {today}")
    
    # 计算真实数据天数
    real_days = len(db['commodities'].get('copper', {}).get('price_history', []))
    print(f"[INFO] Real data days: {real_days}/60")
    
    if real_days >= 60:
        print("[OK] 60 days of real data complete!")
    else:
        print(f"[INFO] {60 - real_days} more days needed")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Daily Price Update - SMM")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    try:
        record_daily_prices()
        print("\n" + "=" * 60)
        print("[OK] Daily update completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("Please check SMM website availability")
