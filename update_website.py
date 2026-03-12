import json
from datetime import datetime

def update_website_with_real_data():
    """读取抓取的数据并更新到网页"""
    
    try:
        with open('fetched_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("✗ 未找到 fetched_data.json，请先运行 auto_fetch_data.py")
        return False
    
    # 这里可以添加将数据更新到 index.html 的逻辑
    # 简化版：显示抓取到的数据
    
    print("\n抓取到的数据：")
    print("=" * 60)
    
    for source, items in data.items():
        if source in ['生意社', 'SMM']:
            print(f"\n【{source}】")
            for commodity, info in items.items():
                if 'error' not in info:
                    print(f"  ✓ {commodity}: {info.get('price', 'N/A')}")
                else:
                    print(f"  ✗ {commodity}: {info.get('error', '失败')}")
    
    print("\n" + "=" * 60)
    print("\n请手动检查 fetched_data.json 文件")
    print("如果数据完整，我可以帮你生成带真实数据的网页")
    
    return True

if __name__ == '__main__':
    update_website_with_real_data()
