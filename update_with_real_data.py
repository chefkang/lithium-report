# 用真实数据更新网站的脚本
import json

# 读取真实价格数据
with open('real_prices_today.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("真实数据已加载！")
print(f"数据来源: {data['data_source']}")
print(f"更新日期: {data['last_update']}")
print(f"商品数量: {len(data['commodities'])}")

for code, item in data['commodities'].items():
    print(f"  {item['name']}: {item['price']} {item['unit']} ({'+' if item['change'] >= 0 else ''}{item['change']})")
