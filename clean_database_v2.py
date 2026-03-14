#!/usr/bin/env python3
"""
清理数据库，删除重复的模拟数据
"""

import json
from datetime import datetime

def clean_database():
    # 读取数据库
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    print(f"开始清理数据库...")
    print(f"原始数据开始日期: {db.get('start_date')}")
    print(f"上次更新: {db.get('last_update')}")
    
    # 清理每种商品的价格历史
    cleaned_count = 0
    for code, commodity in db['commodities'].items():
        if 'price_history' not in commodity:
            continue
            
        original_count = len(commodity['price_history'])
        
        # 使用字典去重，以日期为键
        unique_entries = {}
        for entry in commodity['price_history']:
            date = entry.get('date')
            if not date:
                continue
                
            # 只保留每个日期的第一个记录
            if date not in unique_entries:
                unique_entries[date] = entry
        
        # 转换为列表并按日期排序
        unique_list = list(unique_entries.values())
        unique_list.sort(key=lambda x: x.get('date', ''))
        
        commodity['price_history'] = unique_list
        cleaned = original_count - len(unique_list)
        cleaned_count += cleaned
        
        if cleaned > 0:
            print(f"  {commodity['name']}: 删除 {cleaned} 个重复记录，剩余 {len(unique_list)} 个")
    
    # 更新进度天数（基于实际唯一日期数）
    if db['commodities']:
        sample_code = next(iter(db['commodities']))
        sample_history = db['commodities'][sample_code].get('price_history', [])
        real_days = len(sample_history)
        db['progress_days'] = real_days
        print(f"实际真实数据天数: {real_days}/60")
    
    # 保存清理后的数据库
    with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 清理完成，共删除 {cleaned_count} 个重复记录")
    print(f"[OK] 数据库已保存")
    
    return True

def verify_cleanup():
    """验证清理结果"""
    with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    print("\n验证清理结果:")
    for code, commodity in list(db['commodities'].items())[:5]:  # 只检查前5个
        dates = [entry.get('date') for entry in commodity.get('price_history', [])]
        unique_dates = set(dates)
        print(f"  {commodity['name']}: {len(dates)} 个记录, {len(unique_dates)} 个唯一日期")
        
        # 检查重复
        if len(dates) != len(unique_dates):
            print(f"  ⚠️  仍有重复!")
            from collections import Counter
            duplicates = Counter(dates)
            for date, count in duplicates.items():
                if count > 1:
                    print(f"    {date}: {count} 次")
    
    print(f"\n总进度: {db.get('progress_days', 0)}/60 天真实数据")

if __name__ == '__main__':
    print("=" * 60)
    print("清理商品价格数据库")
    print("=" * 60)
    
    clean_database()
    verify_cleanup()
    
    print("\n" + "=" * 60)
    print("清理完成!")
    print("=" * 60)