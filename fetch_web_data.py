import requests
from bs4 import BeautifulSoup
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def fetch_commodity_prices():
    """从多个来源获取商品价格"""
    
    data = {}
    
    # 尝试1: 新浪财经期货行情页面
    try:
        print("正在获取新浪财经数据...")
        url = "https://finance.sina.com.cn/futures/quotes.shtml"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"新浪财经状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 保存页面内容用于分析
            with open('sina_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✓ 新浪财经页面已保存")
    except Exception as e:
        print(f"✗ 新浪财经失败: {e}")
    
    # 尝试2: 生意社大宗商品页面
    try:
        print("\n正在获取生意社数据...")
        url = "https://www.100ppi.com/v/sell/list-718-1.html"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"生意社状态码: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找价格数据
            price_elements = soup.find_all('td', class_='price')
            print(f"  找到 {len(price_elements)} 个价格元素")
            
            # 保存页面
            with open('100ppi_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✓ 生意社页面已保存")
    except Exception as e:
        print(f"✗ 生意社失败: {e}")
    
    # 尝试3: 我的钢铁网
    try:
        print("\n正在获取我的钢铁网数据...")
        url = "https://www.mysteel.com/"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"我的钢铁网状态码: {response.status_code}")
        
        if response.status_code == 200:
            with open('mysteel_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✓ 我的钢铁网页面已保存")
    except Exception as e:
        print(f"✗ 我的钢铁网失败: {e}")
    
    # 尝试4: 上海有色网SMM
    try:
        print("\n正在获取SMM数据...")
        url = "https://www.smm.cn/news"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"SMM状态码: {response.status_code}")
        
        if response.status_code == 200:
            with open('smm_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✓ SMM页面已保存")
    except Exception as e:
        print(f"✗ SMM失败: {e}")
    
    return data

if __name__ == '__main__':
    print("=" * 60)
    print("开始抓取商品数据...")
    print("=" * 60)
    
    data = fetch_commodity_prices()
    
    print("\n" + "=" * 60)
    print("抓取完成，页面已保存到本地")
    print("=" * 60)
    print("\n请检查以下文件：")
    print("- sina_page.html (新浪财经)")
    print("- 100ppi_page.html (生意社)")
    print("- mysteel_page.html (我的钢铁网)")
    print("- smm_page.html (SMM)")
