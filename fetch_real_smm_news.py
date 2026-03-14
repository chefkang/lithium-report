#!/usr/bin/env python3
"""
从SMM上海有色网抓取真实新闻
"""

import json
import re
from datetime import datetime

def parse_news_from_snapshot(snapshot_text):
    """从SMM快照中解析新闻"""
    news_items = []
    
    # 提取新闻标题和链接
    # 从快照中我们看到类似这样的结构:
    # link "中东局势扰动、宏微观博弈下 伦沪铜连跌两周之后将如何表现？【SMM评论】" [ref=e81] [cursor=pointer]:
    #   - /url: /news/103805781
    
    # 使用正则表达式提取新闻
    pattern = r'link "([^"]+)" \[ref=[^\]]+\] \[cursor=pointer\]:\s*- /url: ([^\s]+)'
    matches = re.findall(pattern, snapshot_text)
    
    for title, url in matches:
        # 过滤掉一些非新闻的链接
        if len(title) < 10 or 'img' in title or '上一篇' in title or '下一篇' in title:
            continue
        
        # 确定新闻类别
        category = '其他'
        if '铜' in title:
            category = '铜'
        elif '铝' in title:
            category = '铝'
        elif '锡' in title:
            category = '锡'
        elif '镍' in title:
            category = '镍'
        elif '锂' in title:
            category = '锂盐'
        elif '黄金' in title or '白银' in title:
            category = '贵金属'
        elif '原油' in title:
            category = '能源'
        elif '新能源' in title or '电池' in title:
            category = '新能源'
        elif '宏观' in title or '金融' in title:
            category = '宏观'
        elif 'SMM评论' in title:
            category = '分析评论'
        
        # 确保URL完整
        if url.startswith('/'):
            url = f'https://news.smm.cn{url}'
        
        news_items.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'title': title,
            'source': 'SMM上海有色网',
            'summary': f'{title[:50]}...',  # 简短的摘要
            'category': category,
            'url': url
        })
    
    return news_items

def save_news(news_items):
    """保存新闻数据"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    news_data = {
        'last_update': today,
        'source': 'SMM上海有色网（真实抓取）',
        'news': news_items[:10]  # 只保存前10条
    }
    
    with open('commodity_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 保存了 {len(news_items[:10])} 条真实新闻")
    return news_data

def main():
    print("=" * 60)
    print("SMM真实新闻抓取")
    print("=" * 60)
    
    print("\n注意: 这个脚本需要配合browser工具使用")
    print("请先使用browser访问 https://news.smm.cn")
    print("然后获取页面快照")
    
    # 这里应该从browser工具获取快照内容
    # 由于无法直接在此获取，我们提供指导
    
    print("\n使用步骤:")
    print("1. 运行: browser(action='open', targetUrl='https://news.smm.cn')")
    print("2. 运行: browser(action='snapshot', targetId='...', maxChars=10000)")
    print("3. 将快照文本保存到文件，如 smm_news_snapshot.txt")
    print("4. 运行此脚本解析新闻")
    
    # 如果有保存的快照文件，可以尝试解析
    try:
        with open('smm_news_snapshot.txt', 'r', encoding='utf-8') as f:
            snapshot_text = f.read()
        
        print("\n从文件中读取快照...")
        news_items = parse_news_from_snapshot(snapshot_text)
        
        if news_items:
            news_data = save_news(news_items)
            print("\n抓取的新闻:")
            for i, news in enumerate(news_data['news'], 1):
                print(f"  {i}. {news['title']} ({news['category']})")
        else:
            print("\n[WARNING] 未能从快照中解析出新闻")
            print("使用模拟新闻数据作为后备")
            
            # 使用模拟数据
            from update_news import fetch_commodity_news
            fetch_commodity_news()
            
    except FileNotFoundError:
        print("\n[INFO] 未找到快照文件，使用模拟新闻数据")
        print("运行 update_news.py 生成模拟新闻")
        
        import subprocess
        subprocess.run(['uv', 'run', 'python', 'update_news.py'], 
                      cwd='.', check=True)

if __name__ == '__main__':
    main()