#!/usr/bin/env python3
"""
使用Playwright进行高级浏览器自动化抓取
需要安装: uv pip install playwright
然后运行: playwright install chromium
"""

import asyncio
from playwright.async_api import async_playwright
import json
import re
from datetime import datetime

async def fetch_smm_prices():
    """使用Playwright抓取SMM价格"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            print("访问SMM数据看板...")
            await page.goto('https://hq.smm.cn/data', wait_until='networkidle')
            
            # 等待页面加载
            await page.wait_for_timeout(5000)
            
            # 截图保存
            await page.screenshot(path='smm_screenshot.png')
            
            # 获取页面内容
            content = await page.content()
            
            # 提取价格数据
            prices = {}
            
            # 查找期货价格表格
            price_elements = await page.query_selector_all('.price-item, .futures-item, [class*="price"]')
            
            print(f"找到 {len(price_elements)} 个价格元素")
            
            # 这里需要根据实际页面结构编写提取逻辑
            # 示例：查找包含"碳酸锂"的元素
            for i in range(min(20, len(price_elements))):
                try:
                    text = await price_elements[i].text_content()
                    if text and ('碳酸锂' in text or '铜' in text or '铝' in text):
                        print(f"元素 {i}: {text[:50]}...")
                except:
                    pass
            
            await browser.close()
            
            # 解析内容
            patterns = [
                (r'碳酸锂2605.*?(\d+).*?([+-]\d+)', 'lithium-carbonate'),
                (r'沪铜2604.*?(\d+).*?([+-]\d+)', 'copper'),
                # 添加更多模式...
            ]
            
            for pattern, code in patterns:
                match = re.search(pattern, content)
                if match:
                    prices[code] = {
                        'price': float(match.group(1)),
                        'change': float(match.group(2))
                    }
            
            return prices
            
        except Exception as e:
            print(f"Playwright抓取失败: {e}")
            await browser.close()
            return {}

if __name__ == '__main__':
    print("开始Playwright抓取...")
    prices = asyncio.run(fetch_smm_prices())
    print(f"抓取到 {len(prices)} 种商品价格")
    print(json.dumps(prices, indent=2, ensure_ascii=False))
