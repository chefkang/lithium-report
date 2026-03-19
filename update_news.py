#!/usr/bin/env python3
"""
每日新闻更新脚本
从SMM等来源获取大宗商品新闻
"""

import json
from datetime import datetime

def fetch_commodity_news():
    """获取大宗商品新闻"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 模拟新闻数据 - 实际应该从SMM新闻页面抓取
    news_items = [
        {
            'date': today,
            'title': '碳酸锂价格短期承压，下游需求观望情绪浓厚',
            'source': 'SMM锂电资讯',
            'summary': '近期碳酸锂市场供应充足，下游电池厂采购谨慎，价格维持震荡走势。',
            'category': '锂盐',
            'url': 'https://news.smm.cn/lithium'
        },
        {
            'date': today,
            'title': '铜价受宏观因素影响小幅下跌',
            'source': 'SMM铜市分析',
            'summary': '美联储政策预期叠加库存上升，铜价短期承压。',
            'category': '基本金属',
            'url': 'https://hq.smm.cn/copper'
        },
        {
            'date': today,
            'title': '新能源车销量持续增长，带动锂电材料需求',
            'source': 'SMM新能源汽车',
            'summary': '3月新能源车销量环比增长，对锂盐需求形成支撑。',
            'category': '新能源',
            'url': 'https://new-energy.smm.cn'
        }
    ]
    
    # 保存新闻数据
    news_data = {
        'last_update': today,
        'source': 'SMM上海有色网',
        'news': news_items
    }
    
    with open('commodity_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 新闻数据已更新: {len(news_items)} 条")
    return True

if __name__ == '__main__':
    fetch_commodity_news()
