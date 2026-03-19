#!/usr/bin/env python3
"""
更新PRICE_TRACKING.md文件
添加今天的价格数据
"""

import json
import re
from datetime import datetime

def load_prices():
    """加载今日价格数据"""
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 映射代码到中文名称（按照PRICE_TRACKING.md中的顺序）
    code_to_name = {
        'lithium-carbonate': '碳酸锂',
        'lithium-hydroxide': '氢氧化锂',
        'copper': '铜',
        'aluminum': '铝',
        'tin': '锡',
        'nickel': '镍',
        'gold': '黄金',
        'silver': '白银',
        'iron-ore': '铁矿石',
        'abs': 'ABS',
        'corrugated-paper': '瓦楞纸',
        'crude-oil': '原油'
    }
    
    prices = {}
    for code, name in code_to_name.items():
        if code in data['commodities']:
            prices[name] = data['commodities'][code]['price']
        else:
            print(f"警告: 未找到商品 {name} ({code})")
            prices[name] = ''
    
    return prices

def update_tracking_file(prices):
    """更新PRICE_TRACKING.md文件"""
    today = datetime.now().strftime('%Y-%m-%d')
    weekday = datetime.now().strftime('%a')
    
    # 读取文件内容
    with open('PRICE_TRACKING.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到表格开始位置
    table_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('| 日期 | 星期 |'):
            table_start = i
            break
    
    if table_start == -1:
        print("错误: 未找到表格开始位置")
        return False
    
    # 构建今天的行
    today_row = f"| {today} | {weekday} | "
    today_row += f"{prices['碳酸锂']} | " if prices['碳酸锂'] else " | "
    today_row += f"{prices['氢氧化锂']} | " if prices['氢氧化锂'] else " | "
    today_row += f"{prices['铜']} | " if prices['铜'] else " | "
    today_row += f"{prices['铝']} | " if prices['铝'] else " | "
    today_row += f"{prices['锡']} | " if prices['锡'] else " | "
    today_row += f"{prices['镍']} | " if prices['镍'] else " | "
    today_row += f"{prices['黄金']} | " if prices['黄金'] else " | "
    today_row += f"{prices['白银']} | " if prices['白银'] else " | "
    today_row += f"{prices['铁矿石']} | " if prices['铁矿石'] else " | "
    today_row += f"{prices['ABS']} | " if prices['ABS'] else " | "
    today_row += f"{prices['瓦楞纸']} | " if prices['瓦楞纸'] else " | "
    today_row += f"{prices['原油']} | " if prices['原油'] else " | "
    today_row += "✅ |\n"
    
    print(f"今天的数据行: {today_row}")
    
    # 查找今天是否已存在
    today_pattern = re.compile(rf'^\| {today} \|')
    today_found = False
    
    for i in range(table_start + 2, len(lines)):
        if today_pattern.match(lines[i].strip()):
            # 更新现有行
            lines[i] = today_row
            today_found = True
            print(f"更新第 {i+1} 行的数据")
            break
    
    if not today_found:
        # 找到第一个空行或状态为⏳的行插入
        insert_pos = -1
        for i in range(table_start + 2, len(lines)):
            if '⏳' in lines[i] or not lines[i].strip() or lines[i].strip() == '|':
                insert_pos = i
                break
        
        if insert_pos == -1:
            # 在表格末尾插入
            insert_pos = len(lines)
        
        lines.insert(insert_pos, today_row)
        print(f"在第 {insert_pos+1} 行插入新数据")
    
    # 更新进度统计
    total_days = 60
    completed_days = 0
    
    for line in lines:
        if '✅' in line:
            completed_days += 1
    
    # 找到进度统计部分
    for i, line in enumerate(lines):
        if line.strip().startswith('- **已完成**:'):
            # 更新已完成天数
            lines[i] = f"- **已完成**: {completed_days} 天\n"
        elif line.strip().startswith('- **剩余**:'):
            # 更新剩余天数
            remaining = total_days - completed_days
            lines[i] = f"- **剩余**: {remaining} 天\n"
        elif line.strip().startswith('- **完成率**:'):
            # 更新完成率
            completion_rate = (completed_days / total_days * 100) if total_days > 0 else 0
            lines[i] = f"- **完成率**: {completion_rate:.1f}%\n"
    
    # 写回文件
    with open('PRICE_TRACKING.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n✅ PRICE_TRACKING.md 更新完成")
    print(f"📊 进度: {completed_days}/{total_days} 天 ({completed_days/total_days*100:.1f}%)")
    
    return True

def main():
    """主函数"""
    print("更新PRICE_TRACKING.md文件...")
    
    try:
        # 加载价格数据
        prices = load_prices()
        
        # 检查是否所有价格都有值
        missing = [name for name, price in prices.items() if not price]
        if missing:
            print(f"警告: 以下商品缺少价格数据: {', '.join(missing)}")
        
        # 更新文件
        success = update_tracking_file(prices)
        
        if success:
            print("\n🎯 价格跟踪表更新成功!")
            return True
        else:
            print("\n❌ 价格跟踪表更新失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    main()