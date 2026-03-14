#!/usr/bin/env python3
"""
从新浪财经获取期货数据
"""

import requests
import json
import re
from datetime import datetime

# 新浪财经期货代码映射
SINA_CODES = {
    'copper': 'hf_CU0',      # 铜期货
    'aluminum': 'hf_AL0',    # 铝期货
    'zinc': 'hf_ZN0',        # 锌期货
    'lead': 'hf_PB0',        # 铅期货
    'nickel': 'hf_NI0',      # 镍期货
    'tin': 'hf_SN0',         # 锡期货
    'gold': 'hf_AU0',        # 黄金期货
    'silver': 'hf_AG0',      # 白银期货
    'crude-oil': 'hf_SC0',   # 原油期货
}

def get_sina_futures():
    """从新浪财经获取期货数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://finance.sina.com.cn/'
    }
    
    results = {}
    
    for code, sina_code in SINA_CODES.items():
        url = f'https://hq.sinajs.cn/list={sina_code}'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'gbk'  # 新浪使用GBK编码
            
            # 解析响应，格式如: var hq_str_hf_CU0="铜连续,72450.000,72450.000,72450.000,0.000,0.000,0.000,2024-03-07,15:00:00,0";
            content = response.text
            
            # 提取数据部分
            match = re.search(r'="([^"]+)"', content)
            if match:
                data_str = match.group(1)
                parts = data_str.split(',')
                
                if len(parts) >= 9:
                    name = parts[0]
                    latest_price = float(parts[1])  # 最新价
                    # 开盘价 = parts[2], 最高价 = parts[3], 最低价 = parts[4]
                    # 涨跌 = parts[5] (可能是0，需要计算)
                    # 涨跌幅 = parts[6]
                    
                    # 计算涨跌（如果未提供）
                    if float(parts[5]) == 0 and len(parts) > 7:
                        # 尝试从名称中提取
                        pass
                    
                    # 简单的涨跌计算（基于前一日收盘价假设）
                    change = 0  # 默认
                    change_percent = 0
                    
                    results[code] = {
                        'name': name,
                        'price': latest_price,
                        'change': change,
                        'change_percent': change_percent,
                        'source': 'sina'
                    }
                    
                    print(f"✓ {name}: {latest_price}")
                else:
                    print(f"✗ {sina_code}: 数据格式错误")
            else:
                print(f"✗ {sina_code}: 未找到数据")
                
        except Exception as e:
            print(f"✗ {sina_code}: {e}")
    
    return results

def update_with_sina_data(sina_data):
    """用新浪数据更新今日价格"""
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    data['last_update'] = today
    
    updated_count = 0
    
    # 单位映射
    unit_map = {
        'copper': '元/吨',
        'aluminum': '元/吨',
        'zinc': '元/吨',
        'lead': '元/吨',
        'nickel': '元/吨',
        'tin': '元/吨',
        'gold': '元/克',
        'silver': '元/千克',
        'crude-oil': '美元/桶',
    }
    
    for code, sina_info in sina_data.items():
        if code in data['commodities']:
            old_price = data['commodities'][code]['price']
            new_price = sina_info['price']
            
            # 计算涨跌（如果新浪未提供）
            change = sina_info.get('change', new_price - old_price)
            change_percent = sina_info.get('change_percent', 
                                         (change / old_price * 100) if old_price != 0 else 0)
            
            data['commodities'][code]['price'] = new_price
            data['commodities'][code]['change'] = round(change, 2)
            data['commodities'][code]['change_percent'] = round(change_percent, 2)
            data['commodities'][code]['date'] = today
            data['commodities'][code]['is_real'] = True
            
            # 更新数据来源
            data['data_source'] = f"新浪财经期货 + SMM历史数据"
            
            updated_count += 1
            print(f"  更新 {data['commodities'][code]['name']}: {new_price} {unit_map.get(code, '')}")
    
    # 保存
    with open('real_prices_today.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updated_count

def main():
    print("=" * 60)
    print("新浪财经期货数据抓取")
    print("=" * 60)
    
    print("\n正在获取数据...")
    sina_data = get_sina_futures()
    
    if sina_data:
        print(f"\n获取到 {len(sina_data)} 种期货数据")
        
        # 更新今日价格
        updated = update_with_sina_data(sina_data)
        print(f"\n[OK] 更新了 {updated} 种商品价格")
        
        # 询问是否更新数据库
        choice = input("\n是否更新到历史数据库? (y/n): ").strip().lower()
        if choice == 'y':
            # 运行数据库更新脚本
            import subprocess
            subprocess.run(['uv', 'run', 'python', 'update_database_with_real_prices.py'], 
                          cwd='.', check=True)
    else:
        print("\n[ERROR] 未能获取期货数据")
        print("请检查网络连接或尝试其他数据源")

if __name__ == '__main__':
    main()