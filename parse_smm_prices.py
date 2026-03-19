#!/usr/bin/env python3
"""
解析SMM快照中的价格数据
"""

import json
import re
from datetime import datetime

def parse_prices_from_text(text):
    """从文本中解析价格数据"""
    # 模式：商品名+合约 价格 涨跌
    pattern = r'([\u4e00-\u9fff]+)(\d+)\s+(\d+)\s+([+-]?\d+)'
    matches = re.findall(pattern, text)
    
    prices = {}
    
    for name, contract, price_str, change_str in matches:
        try:
            price = float(price_str)
            change = float(change_str)
            change_percent = (change / (price - change)) * 100 if price - change != 0 else 0
            
            # 映射到我们的商品代码
            code_map = {
                '沪铜': 'copper',
                '沪铝': 'aluminum', 
                '沪锡': 'tin',
                '沪镍': 'nickel',
                '沪锌': 'zinc',
                '沪铅': 'lead',
                '黄金': 'gold',  # 可能在其他地方
                '白银': 'silver',  # 可能在其他地方
            }
            
            if name in code_map:
                code = code_map[name]
                prices[code] = {
                    'name': name,
                    'contract': contract,
                    'price': price,
                    'change': change,
                    'change_percent': round(change_percent, 2)
                }
                print(f"✓ {name}{contract}: {price} ({change:+.0f})")
        except ValueError as e:
            print(f"✗ 解析错误 {name}{contract}: {e}")
    
    return prices

def update_today_prices(smm_prices):
    """用SMM数据更新今日价格"""
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    data['last_update'] = today
    data['data_source'] = 'SMM上海有色网期货数据'
    
    # 单位映射（期货通常是元/吨）
    unit_map = {
        'copper': '元/吨',
        'aluminum': '元/吨',
        'tin': '元/吨',
        'nickel': '元/吨',
        'zinc': '元/吨',
        'lead': '元/吨',
        'gold': '元/克',
        'silver': '元/千克',
        'lithium-carbonate': '元/吨',
        'lithium-hydroxide': '元/吨',
        'iron-ore': '元/吨',
        'abs': '元/吨',
        'corrugated-paper': '元/吨',
        'crude-oil': '美元/桶',
    }
    
    updated_count = 0
    
    # 先更新从SMM获取的数据
    for code, smm_info in smm_prices.items():
        if code in data['commodities']:
            old_price = data['commodities'][code]['price']
            new_price = smm_info['price']
            change = smm_info['change']
            change_percent = smm_info['change_percent']
            
            data['commodities'][code]['price'] = new_price
            data['commodities'][code]['change'] = change
            data['commodities'][code]['change_percent'] = change_percent
            data['commodities'][code]['date'] = today
            data['commodities'][code]['is_real'] = True
            
            # 更新价格范围（基于涨跌估算）
            if 'price_range' in data['commodities'][code]:
                old_range = data['commodities'][code]['price_range']
                if old_range and '~' in old_range:
                    try:
                        low, high = old_range.split('~')
                        low = float(low.replace(',', ''))
                        high = float(high.replace(',', ''))
                        avg_old = (low + high) / 2
                        if avg_old != 0:
                            ratio = new_price / avg_old
                            new_low = round(low * ratio, 2)
                            new_high = round(high * ratio, 2)
                            data['commodities'][code]['price_range'] = f"{new_low}~{new_high}"
                    except:
                        pass
            
            updated_count += 1
            print(f"  更新 {data['commodities'][code]['name']}: {new_price} ({change:+.0f})")
    
    # 对于SMM没有的数据，保持原样但标记为模拟
    for code, item in data['commodities'].items():
        if code not in smm_prices:
            # 标记为模拟数据
            data['commodities'][code]['is_real'] = False
            print(f"  注意: {item['name']} 无SMM数据，保持模拟值")
    
    # 保存
    with open('real_prices_today.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 更新了 {updated_count} 种商品价格")
    print(f"[OK] 数据已保存到 real_prices_today.json")
    
    return data

def main():
    print("=" * 60)
    print("SMM价格数据解析")
    print("=" * 60)
    
    # 这里应该提供快照文本
    # 由于无法直接获取，我们手动输入从快照中看到的数据
    
    print("\n从快照中提取的数据:")
    
    # 手动输入从快照中看到的价格
    smm_data = {
        'copper': {'price': 99730, 'change': -870, 'change_percent': -0.87},
        'aluminum': {'price': 24965, 'change': -320, 'change_percent': -1.27},
        'lead': {'price': 16395, 'change': -190, 'change_percent': -1.15},
        'zinc': {'price': 24080, 'change': -140, 'change_percent': -0.58},
        'tin': {'price': 372860, 'change': -12770, 'change_percent': -3.31},
        'nickel': {'price': 135900, 'change': -2630, 'change_percent': -1.90},
    }
    
    for code, info in smm_data.items():
        print(f"  {code}: {info['price']} ({info['change']:+.0f})")
    
    # 更新今日价格
    print("\n更新今日价格...")
    data = update_today_prices(smm_data)
    
    # 询问是否更新数据库
    choice = input("\n是否更新到历史数据库? (y/n): ").strip().lower()
    if choice == 'y':
        # 运行数据库更新脚本
        import subprocess
        subprocess.run(['uv', 'run', 'python', 'update_database_with_real_prices.py'], 
                      cwd='.', check=True)
        print("[OK] 数据库已更新")

if __name__ == '__main__':
    main()