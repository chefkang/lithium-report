#!/usr/bin/env python3
"""
将今日真实价格更新到历史数据库
"""

import json
from datetime import datetime

def update_database():
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
    
    print(f"更新数据库日期: {today}")
    
    # 更新每种商品的价格历史
    updated_count = 0
    for code, item in today_data['commodities'].items():
        if code not in db['commodities']:
            db['commodities'][code] = {
                'name': item['name'],
                'unit': item['unit'],
                'price_history': []
            }
        
        # 检查今天是否已有记录
        existing_today = False
        for entry in db['commodities'][code]['price_history']:
            if entry.get('date') == today:
                existing_today = True
                # 更新现有记录
                entry.update({
                    'price': item['price'],
                    'change': item['change'],
                    'change_percent': item['change_percent'],
                    'is_real': True
                })
                print(f"  更新: {item['name']} - {item['price']} {item['unit']}")
                break
        
        if not existing_today:
            # 添加新记录
            db['commodities'][code]['price_history'].append({
                'date': today,
                'price': item['price'],
                'change': item['change'],
                'change_percent': item['change_percent'],
                'is_real': True
            })
            print(f"  添加: {item['name']} - {item['price']} {item['unit']}")
        
        updated_count += 1
        
        # 只保留最近60天
        db['commodities'][code]['price_history'] = \
            db['commodities'][code]['price_history'][-60:]
    
    db['last_update'] = today
    
    # 更新进度天数
    if db['commodities']:
        sample_code = next(iter(db['commodities']))
        sample_history = db['commodities'][sample_code].get('price_history', [])
        real_days = len(sample_history)
        db['progress_days'] = real_days
        
        print(f"\n真实数据进度: {real_days}/60 天")
        if real_days >= 60:
            print("[OK] 60天真实数据收集完成!")
        else:
            days_needed = 60 - real_days
            estimated_completion = datetime.now().date()
            from datetime import timedelta
            estimated_completion += timedelta(days=days_needed)
            db['estimated_completion'] = estimated_completion.strftime('%Y-%m-%d')
            print(f"  还需 {days_needed} 天，预计完成日期: {estimated_completion}")
    
    # 保存数据库
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 数据库更新完成")
    print(f"[OK] 共更新 {updated_count} 种商品")
    
    return True

def update_website():
    """生成更新后的网站"""
    print("\n更新网站...")
    try:
        import subprocess
        subprocess.run(['uv', 'run', 'python', 'generate_real_website.py'], 
                      cwd='.', check=True)
        print("[OK] 网站已生成")
        
        # Git推送
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Real data update - {datetime.now().strftime("%Y-%m-%d")}'], 
                      check=True)
        subprocess.run(['git', 'push', 'origin', 'master:main'], check=True)
        print("[OK] 已推送到GitHub")
        
    except Exception as e:
        print(f"[WARNING] 网站更新失败: {e}")
        print("请手动运行: uv run python generate_real_website.py")

if __name__ == '__main__':
    print("=" * 60)
    print("更新历史数据库")
    print("=" * 60)
    
    update_database()
    
    # 自动更新网站（非交互式模式）
    print("\n自动生成网站并推送到GitHub...")
    update_website()
    
    print("\n" + "=" * 60)
    print("[OK] 数据库更新流程完成!")
    print("=" * 60)