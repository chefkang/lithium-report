# 每日价格更新脚本
# 用法: 修改下面的价格，然后运行 uv run python update_today_prices.py

import json
from datetime import datetime

# ============================
# 修改这里：填入今天从SMM网站看到的价格
# ============================

TODAY_PRICES = {
    "lithium-carbonate": {
        "price": 159500,  # 碳酸锂今日价格
        "change": 800,    # 涨跌额
        "change_percent": 0.50  # 涨跌幅%
    },
    "lithium-hydroxide": {
        "price": 153000,
        "change": -700,
        "change_percent": -0.46
    },
    "copper": {
        "price": 72450,
        "change": 180,
        "change_percent": 0.25
    },
    "aluminum": {
        "price": 18580,
        "change": -25,
        "change_percent": -0.13
    },
    "tin": {
        "price": 246200,
        "change": 1500,
        "change_percent": 0.61
    },
    "nickel": {
        "price": 133500,
        "change": -920,
        "change_percent": -0.68
    },
    "gold": {
        "price": 569.2,
        "change": 2.8,
        "change_percent": 0.49
    },
    "silver": {
        "price": 7875,
        "change": 38,
        "change_percent": 0.48
    },
    "iron-ore": {
        "price": 990,
        "change": 15,
        "change_percent": 1.54
    },
    "abs": {
        "price": 12520,
        "change": 95,
        "change_percent": 0.76
    },
    "corrugated-paper": {
        "price": 3140,
        "change": -15,
        "change_percent": -0.48
    },
    "crude-oil": {
        "price": 82.80,
        "change": -0.25,
        "change_percent": -0.30
    }
}

# ============================
# 不要修改下面的代码
# ============================

def update_prices():
    """更新今日价格到数据库"""
    try:
        with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        print("[ERROR] Database not found. Please run record_prices.py first.")
        return False
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for commodity_id, data in TODAY_PRICES.items():
        if commodity_id in db['commodities']:
            # 记录今日价格
            db['commodities'][commodity_id]['daily_records'][today] = {
                'price': data['price'],
                'change': data['change'],
                'change_percent': data['change_percent'],
                'is_real': True,
                'recorded_at': datetime.now().isoformat()
            }
            
            # 添加到历史记录
            if not db['commodities'][commodity_id]['price_history']:
                # 第一天：生成前59天的模拟数据
                from record_prices import generate_historical_prices
                db['commodities'][commodity_id]['price_history'] = \
                    generate_historical_prices(data['price'])
            
            # 添加今日真实价格
            db['commodities'][commodity_id]['price_history'].append({
                'date': today,
                'price': data['price'],
                'is_real': True
            })
            
            # 只保留60天
            db['commodities'][commodity_id]['price_history'] = \
                db['commodities'][commodity_id]['price_history'][-60:]
            
            # 更新基准价格
            db['commodities'][commodity_id]['base_price'] = data['price']
    
    db['last_update'] = today
    
    # 保存
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] {today} prices updated successfully!")
    print(f"[INFO] Real data days: 1 (simulated: 59)")
    print(f"[INFO] After 60 days, all data will be real.")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Daily Price Update")
    print("=" * 60)
    
    # 检查价格是否有修改
    default_price = 159500  # 碳酸锂默认价格
    if TODAY_PRICES['lithium-carbonate']['price'] == default_price:
        print("\n[WARNING] You haven't updated the prices yet!")
        print("Please edit TODAY_PRICES in this file first.")
        print("\nSteps:")
        print("1. Open SMM website (www.smm.cn)")
        print("2. Check today's prices for 12 commodities")
        print("3. Update the prices in TODAY_PRICES above")
        print("4. Run this script again: uv run python update_today_prices.py")
    else:
        update_prices()
        print("\n[OK] Now you can generate the website with real trends!")
        print("Run: uv run python generate_website.py")
    
    print("=" * 60)
