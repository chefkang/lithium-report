# 使用Playwright自动化浏览器获取数据
# 需要先安装: uv pip install playwright
# 然后运行: playwright install chromium

import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_with_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("正在访问生意社...")
            await page.goto('https://www.100ppi.com/v/sell/list-718-1.html', wait_until='networkidle')
            await page.wait_for_timeout(3000)  # 等待页面加载
            
            # 获取页面内容
            content = await page.content()
            
            # 保存截图
            await page.screenshot(path='100ppi_screenshot.png')
            
            # 尝试提取数据
            prices = await page.query_selector_all('.price')
            print(f"找到 {len(prices)} 个价格元素")
            
            # 获取第一个价格
            if prices:
                price_text = await prices[0].text_content()
                print(f"第一个价格: {price_text}")
            
            await browser.close()
            return True
            
        except Exception as e:
            print(f"错误: {e}")
            await browser.close()
            return False

if __name__ == '__main__':
    result = asyncio.run(fetch_with_browser())
    if result:
        print("\n✓ 浏览器自动化成功")
    else:
        print("\n✗ 浏览器自动化失败")
