import requests
import json
import re
from datetime import datetime, timedelta

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://quote.eastmoney.com/',
}

def get_shfe_data():
    """获取上海期货交易所数据"""
    # 上海期货交易所公开API
    url = "http://www.shfe.com.cn/data/dailydata/2026/20260312"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"上期所状态码: {response.status_code}")
        return response.text[:1000]
    except Exception as e:
        print(f"上期所获取失败: {e}")
        return None

def get_sina_futures():
    """获取新浪财经期货数据"""
    # 新浪财经期货行情
    codes = [
        ('碳酸锂', 'LC0'),      # 碳酸锂期货
        ('铜', 'CU0'),          # 铜期货
        ('铝', 'AL0'),          # 铝期货
        ('锡', 'SN0'),          # 锡期货
        ('镍', 'NI0'),          # 镍期货
        ('黄金', 'AU0'),        # 黄金期货
        ('白银', 'AG0'),        # 白银期货
        ('铁矿石', 'I0'),       # 铁矿石期货
        ('原油', 'SC0'),        # 原油期货
    ]
    
    results = {}
    for name, code in codes:
        url = f"https://hq.sinajs.cn/list=hf_{code}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            # 新浪返回的是JavaScript变量格式
            match = re.search(r'"([^"]+)"', response.text)
            if match:
                data = match.group(1).split(',')
                if len(data) >= 8:
                    results[name] = {
                        'name': name,
                        'price': data[0],           # 最新价
                        'change': data[1],          # 涨跌额
                        'change_percent': data[2],  # 涨跌幅
                        'open': data[5],            # 开盘价
                        'high': data[6],            # 最高价
                        'low': data[7],             # 最低价
                    }
                    print(f"✓ {name}: {data[0]}")
        except Exception as e:
            print(f"✗ {name}: {e}")
    
    return results

def get_eastmoney_data():
    """获取东方财富数据"""
    # 东方财富商品期货API
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        'secid': '113.lc2507',  # 碳酸锂期货
        'fields': 'f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f107',
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        print(f"东方财富数据: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
        return data
    except Exception as e:
        print(f"东方财富获取失败: {e}")
        return None

if __name__ == '__main__':
    print("=" * 60)
    print("大宗商品数据抓取")
    print("=" * 60)
    
    print("\n【1】新浪财经期货数据:")
    sina_data = get_sina_futures()
    
    print("\n【2】上海期货交易所:")
    shfe_data = get_shfe_data()
    
    print("\n【3】东方财富:")
    eastmoney_data = get_eastmoney_data()
    
    print("\n" + "=" * 60)
    print("抓取完成")
    print("=" * 60)
    
    # 保存结果
    if sina_data:
        with open('commodity_data.json', 'w', encoding='utf-8') as f:
            json.dump(sina_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 数据已保存到 commodity_data.json")
        print(f"  共获取 {len(sina_data)} 种商品数据")
