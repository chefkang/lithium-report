import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright

async def fetch_smm_data():
    """Fetch data from SMM"""
    print("Starting browser...")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
        except Exception as e:
            print(f"[ERROR] Browser launch failed: {e}")
            print("Please run: uv run playwright install chromium")
            return {}
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        # Anti-detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        
        results = {}
        
        try:
            print("\nVisiting SMM lithium carbonate page...")
            await page.goto('https://www.smm.cn/lithium-carbonate', 
                          wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(3000)
            
            # Save screenshot
            await page.screenshot(path='smm_lithium.png')
            print("[OK] Screenshot saved to smm_lithium.png")
            
            # Get page title
            title = await page.title()
            print(f"Page title: {title}")
            
            # Try to extract price data
            # Note: Selectors need to be adjusted based on actual page structure
            html = await page.content()
            with open('smm_lithium.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("[OK] HTML saved to smm_lithium.html")
            
            results['lithium_carbonate'] = {
                'source': 'SMM',
                'timestamp': datetime.now().isoformat(),
                'status': 'fetched'
            }
            
        except Exception as e:
            print(f"[ERROR] Failed: {e}")
            results['lithium_carbonate'] = {'error': str(e)}
        
        await browser.close()
        return results

async def main():
    print("=" * 60)
    print("Commodity Data Auto Fetch (Browser Automation)")
    print("=" * 60)
    
    # Check playwright
    try:
        import playwright
        print("[OK] Playwright installed")
    except ImportError:
        print("[ERROR] Playwright not installed")
        print("Run: uv pip install playwright")
        print("Then: uv run playwright install chromium")
        return
    
    # Fetch from SMM
    print("\nFetching from SMM...")
    results = await fetch_smm_data()
    
    # Save results
    with open('fetched_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("Fetch complete!")
    print("=" * 60)
    print("\nResults saved to: fetched_data.json")
    print("Screenshots saved to current directory")
    print("\nPlease check the screenshot and HTML files.")
    print("If data is successfully fetched, I can help update the website.")

if __name__ == '__main__':
    asyncio.run(main())
