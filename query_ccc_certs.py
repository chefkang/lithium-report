#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCC证书批量查询工具
查询国家认监委公开数据
"""

import urllib.request
import urllib.parse
import json
import ssl
import time
from datetime import datetime

# 禁用SSL验证警告
ssl._create_default_https_context = ssl._create_unverified_context

# 证书列表
certificates = [
    {"no": "2025200915004088", "name": "电芯", "folder": "T2025CCC0915-015832-F606080-2000"},
    {"no": "T2025CCC0915-015832", "name": "电池组", "folder": "T2025CCC0915-015832-F606080-2000"},
    {"no": "A2025CCC0914-4718205", "name": "移动电源", "folder": "011ccc认证"},
    {"no": "A2024CCC0914-4661906", "name": "移动电源", "folder": "013CCC认证"},
    {"no": "S2023CCC0915-001499", "name": "电池组", "folder": "018CCC认证"},
    {"no": "S2025CCC0915-000029", "name": "电池组", "folder": "3C认证资料(1)"},
    {"no": "A2024CCC0915-4435612", "name": "聚合物电池组", "folder": "嘉森CCC证书+报告"},
    {"no": "A2024CCC0915-4435613", "name": "聚合物电池组", "folder": "嘉森CCC证书+报告"},
    {"no": "A2024CCC0914-4584030", "name": "移动电源", "folder": "007+证书"},
    {"no": "A2025CCC0914-4810806", "name": "移动电源", "folder": "015(D6)CCC证书"},
    {"no": "A2025CCC0907-4732245", "name": "电源适配器", "folder": "19V2A电源适配器CCC认证"},
    {"no": "A2025CCC0914-4923042", "name": "移动电源", "folder": "007-ccc认证资料"},
    {"no": "T2025CCC0915-013585", "name": "电池组", "folder": "敬恒CCC证书"},
    {"no": "T2025CCC0915-011957", "name": "电池组", "folder": "敬恒CCC证书"},
    {"no": "T2025CCC0915-013586", "name": "电池组", "folder": "敬恒CCC证书"},
    {"no": "T2024CCC0915-010467", "name": "电池组", "folder": "敬恒CCC证书"},
    {"no": "A2025CCC0915-4830614", "name": "电池组", "folder": "聚合物8267100电芯CCC"},
    {"no": "A2025CCC0915-4751306", "name": "电池组", "folder": "报告&证书"},
    {"no": "A2025CCC0915-4830611", "name": "电池组", "folder": "聚合物8267100电芯CCC"},
    {"no": "A2025CCC0915-4830608", "name": "电池组", "folder": "聚合物8267100电芯CCC"},
    {"no": "A2025CCC0915-4830613", "name": "电池组", "folder": "聚合物8267100电芯CCC"},
    {"no": "A2025CCC0915-4830612", "name": "电池组", "folder": "聚合物8267100电芯CCC"},
]

def query_cert(cert_no):
    """查询单个证书"""
    try:
        # 尝试调用CCC查询接口
        url = f"http://cx.cnca.cn/CertECloud/qts/qtsPage?currentPosition=2&certNumber={urllib.parse.quote(cert_no)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('utf-8')
        
        # 检查是否包含有效信息
        if '证书编号' in html or cert_no in html:
            return {"status": "查询成功", "found": True}
        elif '验证码' in html or 'captcha' in html.lower():
            return {"status": "需要验证码", "found": None}
        else:
            return {"status": "未找到", "found": False}
            
    except Exception as e:
        return {"status": f"查询失败: {str(e)}", "found": None}

def main():
    print("="*80)
    print(" "*25 + "CCC证书批量查询")
    print("="*80)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"证书总数: {len(certificates)}")
    print("="*80)
    print()
    
    results = []
    for i, cert in enumerate(certificates, 1):
        print(f"[{i}/{len(certificates)}] 查询中: {cert['no']}")
        result = query_cert(cert['no'])
        cert['query_result'] = result
        results.append(cert)
        print(f"      结果: {result['status']}")
        print()
        time.sleep(1)  # 避免请求过快
    
    # 生成报告
    print("="*80)
    print(" "*25 + "查询结果汇总")
    print("="*80)
    
    success_count = sum(1 for r in results if r['query_result']['found'] == True)
    captcha_count = sum(1 for r in results if '验证码' in r['query_result']['status'])
    fail_count = len(results) - success_count - captcha_count
    
    print(f"查询成功: {success_count}")
    print(f"需要验证码: {captcha_count}")
    print(f"查询失败: {fail_count}")
    print()
    
    # 输出详细结果
    print("详细结果:")
    print("-"*80)
    for r in results:
        status_icon = "✓" if r['query_result']['found'] == True else "✗"
        print(f"{status_icon} {r['no']}")
        print(f"  产品: {r['name']}")
        print(f"  位置: {r['folder']}")
        print(f"  状态: {r['query_result']['status']}")
        print()
    
    # 保存到文件
    report_file = f"CCC查询结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("CCC证书查询结果\n")
        f.write("="*80 + "\n")
        f.write(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"证书总数: {len(certificates)}\n\n")
        for r in results:
            f.write(f"证书编号: {r['no']}\n")
            f.write(f"产品类型: {r['name']}\n")
            f.write(f"文件夹: {r['folder']}\n")
            f.write(f"查询状态: {r['query_result']['status']}\n")
            f.write("-"*40 + "\n")
    
    print(f"\n报告已保存至: {report_file}")

if __name__ == "__main__":
    main()
