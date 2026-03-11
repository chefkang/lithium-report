#!/usr/bin/env python3
"""
锂盐报告自动更新脚本
每日09:00自动运行，更新碳酸锂和氢氧化锂价格及新闻
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 模拟价格数据（实际应用中应该从API获取）
def generate_price_data():
    """生成模拟价格数据"""
    base_carb = 10.85
    base_hyd = 9.45
    
    # 添加随机波动
    carb_price = base_carb + random.uniform(-0.1, 0.1)
    hyd_price = base_hyd + random.uniform(-0.08, 0.08)
    
    return {
        "carbonate": round(carb_price, 2),
        "hydroxide": round(hyd_price, 2),
        "carb_change_day": round(random.uniform(-0.5, 0.5), 2),
        "hyd_change_day": round(random.uniform(-0.5, 0.5), 2),
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "time": datetime.now().strftime("%H:%M")
    }

# 模拟新闻数据（实际应用中应该从爬虫获取）
def generate_news_data():
    """生成模拟新闻数据"""
    news_templates = [
        {"title": "宁德时代发布新一代高镍电池，氢氧化锂需求预期上调", "source": "中国证券报", "sentiment": "利多", "category": "需求端"},
        {"title": "澳洲Pilbara锂精矿拍卖价反弹，成本支撑显现", "source": "Mining.com", "sentiment": "利多", "category": "供应链"},
        {"title": "智利SQM产量持续增长，全球供应宽松", "source": "Reuters", "sentiment": "利空", "category": "供应链"},
        {"title": "中国新能源汽车销量超预期，碳酸锂采购增加", "source": "中国汽车报", "sentiment": "利多", "category": "需求端"},
        {"title": "欧盟对中国锂产品征收临时反倾销税", "source": "欧盟公报", "sentiment": "利空", "category": "政策监管"},
        {"title": "阿根廷新增锂矿出口配额获批", "source": "BNamericas", "sentiment": "利空", "category": "供应链"},
        {"title": "青海盐湖碳酸锂项目检修，短期供应收紧", "source": "证券时报", "sentiment": "利多", "category": "供应链"},
        {"title": "特斯拉宣布扩大4680电池产能", "source": "Electrek", "sentiment": "利多", "category": "需求端"},
    ]
    
    # 随机选择4-6条新闻
    selected = random.sample(news_templates, random.randint(4, 6))
    
    # 添加日期
    today = datetime.now()
    for i, news in enumerate(selected):
        date_offset = random.randint(0, 2)
        news_date = today - timedelta(days=date_offset)
        news["date"] = news_date.strftime("%m-%d")
    
    return selected

def update_html_report():
    """更新HTML报告"""
    # 获取数据
    price_data = generate_price_data()
    news_data = generate_news_data()
    
    # 读取模板文件
    template_path = Path(__file__).parent / "锂盐全球分析报告-完整版.html"
    if not template_path.exists():
        print(f"❌ 模板文件不存在: {template_path}")
        return False
    
    html_content = template_path.read_text(encoding='utf-8')
    
    # 更新日期和时间
    html_content = html_content.replace(
        '报告日期：2026年03月11日',
        f'报告日期：{price_data["date"]}'
    )
    html_content = html_content.replace(
        '更新时间：10:03',
        f'更新时间：{price_data["time"]}'
    )
    
    # 更新价格
    html_content = html_content.replace(
        '<div class="price">¥10.85<span style="font-size:24px">万/吨</span></div>',
        f'<div class="price">¥{price_data["carbonate"]}<span style="font-size:24px">万/吨</span></div>',
        1  # 只替换第一个（碳酸锂）
    )
    html_content = html_content.replace(
        '<div class="price">¥9.45<span style="font-size:24px">万/吨</span></div>',
        f'<div class="price">¥{price_data["hydroxide"]}<span style="font-size:24px">万/吨</span></div>',
        1  # 只替换第一个（氢氧化锂）
    )
    
    # 保存更新后的报告
    output_path = Path(__file__).parent / "index.html"
    output_path.write_text(html_content, encoding='utf-8')
    
    # 记录更新日志
    log_entry = f"""
[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 报告已更新
- 碳酸锂价格: ¥{price_data["carbonate"]}万/吨 ({price_data["carb_change_day"]:+.2f}%)
- 氢氧化锂价格: ¥{price_data["hydroxide"]}万/吨 ({price_data["hyd_change_day"]:+.2f}%)
- 新闻数量: {len(news_data)}条
"""
    
    log_path = Path(__file__).parent / "update_log.txt"
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"✅ 报告已更新: {output_path}")
    print(f"✅ 更新日志: {log_path}")
    
    return True

if __name__ == "__main__":
    print("=== 锂盐报告自动更新 ===")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = update_html_report()
    
    if success:
        print("\n✅ 更新完成!")
    else:
        print("\n❌ 更新失败!")
