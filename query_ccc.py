import requests
import json
import time
import re
from datetime import datetime

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

print("="*80)
print("CCC证书批量查询结果")
print("="*80)
print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"证书总数: {len(cert_numbers)}")
print("="*80)
print()

for i, cert_no in enumerate(cert_numbers, 1):
    print(f"{i}. 证书编号: {cert_no}")
    print(f"   状态: 需要手动查询 (官网反爬机制)")
    print(f"   查询链接: http://cx.cnca.cn/CertECloud/qts/qtsPage?currentPosition=2")
    print()
    time.sleep(0.1)

print("="*80)
print("查询说明: 由于CCC官网有反爬虫机制，请手动访问上述链接查询")
print("="*80)
