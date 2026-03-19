#!/usr/bin/env python3
"""
每日自动更新脚本 - 主入口
运行时间: 每天09:00
调用完整的每日更新流程
"""

import sys

def main():
    """主函数 - 调用完整更新流程"""
    try:
        # 导入完整更新模块
        from daily_update_complete import main as complete_main
        
        print("=" * 60)
        print("启动完整每日更新流程")
        print("=" * 60)
        
        # 执行完整更新
        complete_main()
        
    except ImportError as e:
        print(f"[ERROR] 无法导入完整更新模块: {e}")
        print("[INFO] 尝试回退到基本更新...")
        
        # 回退到基本更新
        import json
        from datetime import datetime
        import subprocess
        
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"执行基本更新: {today}")
        
        # 基本数据库更新
        try:
            with open('real_prices_today.json', 'r', encoding='utf-8') as f:
                today_data = json.load(f)
            
            with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
                db = json.load(f)
            
            for code, item in today_data['commodities'].items():
                if code not in db['commodities']:
                    db['commodities'][code] = {'name': item['name'], 'unit': item['unit'], 'price_history': []}
                
                db['commodities'][code]['price_history'].append({
                    'date': today,
                    'price': item['price'],
                    'change': item['change'],
                    'change_percent': item['change_percent'],
                    'is_real': item.get('is_real', False)
                })
                
                db['commodities'][code]['price_history'] = db['commodities'][code]['price_history'][-60:]
            
            db['last_update'] = today
            
            with open('commodity_price_db.json', 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            
            print(f"[OK] 数据库更新完成: {today}")
            
        except Exception as e:
            print(f"[ERROR] 基本更新失败: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
