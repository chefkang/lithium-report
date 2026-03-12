import requests
import json
import time

# 证书编号列表
cert_numbers = [
    "2025200915004088",
    "A2025CCC0914-4718205",
    "A2024CCC0914-4661906",
    "S2023CCC0915-001499",
    "S2025CCC0915-000029",
    "A2024CCC0915-4435612",
    "A2024CCC0915-4435613",
    "A2024CCC0914-4584030",
    "A2025CCC0914-4810806",
    "A2025CCC0907-4732245",
    "A2025CCC0914-4923042",
    "T2025CCC0915-013585",
    "T2025CCC0915-011957",
    "T2025CCC0915-013586",
    "T2024CCC0915-010467",
    "A2025CCC0915-4830614",
    "A2025CCC0915-4751306",
    "A2025CCC0915-4830611",
    "A2025CCC0915-4830608",
    "A2025CCC0915-4830613",
    "A2025CCC0915-4830612"
]

# 查询URL
url = "http://cx.cnca.cn/CertECloud/qts/qtsPage?currentPosition=2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
}

# 尝试访问页面获取session
try:
    session = requests.Session()
    response = session.get(url, headers=headers, timeout=30)
    print(f"页面状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)}")
    
    # 保存页面内容以便分析
    with open("page_content.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("页面内容已保存到 page_content.html")
    
except Exception as e:
    print(f"请求失败: {e}")
