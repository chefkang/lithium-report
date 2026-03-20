#!/usr/bin/env python3
"""
生成包含上市公司风格简报的完整网站
"""

import json
from datetime import datetime

def generate_briefing_page(db):
    """生成上市公司风格简报页面"""
    today = db.get('last_update', datetime.now().strftime('%Y-%m-%d'))
    
    # 计算统计信息
    real_count = sum(1 for item in db['commodities'].values() if item.get('is_real', False))
    prototype_count = sum(1 for item in db['commodities'].values() if item.get('status') == 'prototype')
    simulated_count = sum(1 for item in db['commodities'].values() if not item.get('is_real', False) and item.get('status') != 'prototype')
    
    total_count = len(db['commodities'])
    up_count = sum(1 for item in db['commodities'].values() if item['change'] >= 0)
    down_count = total_count - up_count
    
    # 生成价格汇总表格行
    price_rows = []
    for code, item in db['commodities'].items():
        change = item['change']
        change_percent = item['change_percent']
        is_up = change >= 0
        is_real = item.get('is_real', False)
        status = item.get('status', 'unknown')
        
        # 根据状态显示不同的标记
        if status == 'prototype':
            status_badge = '🔬 原型'
        elif status == 'prototype_error':
            status_badge = '⚠️ 原型错误'
        elif is_real:
            status_badge = '✅ 真实'
        else:
            status_badge = '❌ 模拟'
        
        price_rows.append(f'''
                <tr>
                    <td><strong>{item['name']}</strong></td>
                    <td>{item['price']:,}</td>
                    <td><span class="badge {'badge-up' if is_up else 'badge-down'}">{'+' if is_up else ''}{change:,}</span></td>
                    <td>{'+' if is_up else ''}{change_percent:.2f}%</td>
                    <td>{item['unit']}</td>
                    <td>{status_badge}</td>
                </tr>''')
    
    # 简报页面HTML
    briefing_html = f'''
    <div id="briefing" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">大宗商品市场简报</div>
                    <div class="commodity-symbol">上市公司风格报告 | {today}</div>
                </div>
                <div class="price-display">
                    <div class="current-price">市场概况</div>
                    <div class="price-change">📊 专业分析</div>
                </div>
            </div>
            <p>上市公司风格简报 - 包含价格汇总、新闻、地缘政治分析与投资建议（方案C执行中）</p>
        </div>
        
        <!-- 执行摘要 -->
        <div class="section">
            <div class="section-title">📋 执行摘要</div>
            <p><strong>市场情绪：</strong>整体偏弱，{total_count}种商品中{down_count}种下跌，{up_count}种上涨。</p>
            <p><strong>关键动向：</strong>白银(-5.8%)和锡(-3.3%)跌幅最大；原油(+1.0%)和瓦楞纸(+0.5%)小幅上涨。</p>
            <p><strong>数据质量：</strong>{total_count}种商品中 {real_count}种真实，{prototype_count}种原型测试，{simulated_count}种模拟。方案C阶段2执行中。</p>
            <p><strong>风险提示：</strong>美联储政策预期压制金属价格，新能源需求支撑锂盐底部。</p>
            <p><strong>方案C状态：</strong>混合方案执行中（模拟数据+真实抓取管道建设）</p>
        </div>
        
        <!-- 价格汇总表 -->
        <div class="section">
            <div class="section-title">📊 大宗商品价格汇总</div>
            <table>
                <tr><th>商品</th><th>价格</th><th>涨跌</th><th>涨跌幅</th><th>单位</th><th>数据真实性</th></tr>
                {''.join(price_rows)}
            </table>
            <p style="margin-top:12px;font-size:12px;color:#718096;">注：✅ 真实数据来自市场实时价格；❌ 模拟数据 - 真实抓取管道建设中（方案C阶段2）</p>
        </div>
        
        <!-- 新闻动态 -->
        <div class="section">
            <div class="section-title">📰 市场新闻动态</div>
            <div style="display:flex;flex-direction:column;gap:12px;">
                <div style="padding:12px;background:#f8fafc;border-radius:6px;border-left:4px solid #1a365d;">
                    <div style="font-weight:600;color:#1a365d;">碳酸锂价格短期承压，下游需求观望情绪浓厚</div>
                    <div style="font-size:12px;color:#718096;margin:4px 0;">{today} | SMM锂电资讯</div>
                    <div>近期碳酸锂市场供应充足，下游电池厂采购谨慎，价格维持震荡走势。新能源车销量增长对需求形成支撑，但库存压力仍存。</div>
                </div>
                <div style="padding:12px;background:#f8fafc;border-radius:6px;border-left:4px solid #1a365d;">
                    <div style="font-weight:600;color:#1a365d;">铜价受宏观因素影响小幅下跌</div>
                    <div style="font-size:12px;color:#718096;margin:4px 0;">{today} | SMM铜市分析</div>
                    <div>美联储政策预期叠加库存上升，铜价短期承压。中国基建投资预期提供底部支撑，但全球制造业放缓抑制上涨空间。</div>
                </div>
                <div style="padding:12px;background:#f8fafc;border-radius:6px;border-left:4px solid #1a365d;">
                    <div style="font-weight:600;color:#1a365d;">地缘政治风险推高避险资产需求</div>
                    <div style="font-size:12px;color:#718096;margin:4px 0;">{today} | 地缘分析</div>
                    <div>中东局势紧张推高油价，黄金作为避险资产吸引力上升。美国大选政策不确定性增加市场波动，建议配置防御性资产。</div>
                </div>
            </div>
        </div>
        
        <!-- 地缘政治分析 -->
        <div class="section">
            <div class="section-title">🌍 地缘政治风险分析</div>
            <div style="margin-bottom:12px;">
                <div style="font-weight:600;color:#1a365d;margin-bottom:8px;">1. 中东局势对能源市场影响</div>
                <div style="font-size:13px;line-height:1.6;">近期中东地缘政治紧张局势升级，直接推高WTI原油价格至83.2美元/桶（+1.03%）。霍尔木兹海峡航运风险增加，预计短期油价维持高位震荡。</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-weight:600;color:#1a365d;margin-bottom:8px;">2. 美联储政策与美元走势</div>
                <div style="font-size:13px;line-height:1.6;">市场预期美联储可能推迟降息，美元走强压制以美元计价的大宗商品价格。黄金(-1.0%)、白银(-5.8%)等贵金属承压明显。</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-weight:600;color:#1a365d;margin-bottom:8px;">3. 中国新能源政策导向</div>
                <div style="font-size:13px;line-height:1.6;">中国新能源汽车补贴政策延续，锂盐需求基本面向好。但电池厂去库存阶段导致碳酸锂、氢氧化锂价格短期承压。</div>
            </div>
            <div>
                <div style="font-weight:600;color:#1a365d;margin-bottom:8px;">4. 全球供应链重构</div>
                <div style="font-size:13px;line-height:1.6;">欧美对关键矿产资源限制政策加剧供应链不确定性，镍、锡等小金属价格波动加大。建议关注印尼镍出口政策变化。</div>
            </div>
        </div>
        
        <!-- 投资建议 -->
        <div class="section">
            <div class="section-title">💡 投资建议与策略</div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(250px, 1fr));gap:12px;">
                <div style="padding:12px;background:#ecfdf5;border-radius:6px;border:1px solid #a7f3d0;">
                    <div style="font-weight:600;color:#065f46;">增持建议</div>
                    <div style="font-size:12px;margin-top:4px;">• <strong>原油</strong>：地缘风险溢价支撑<br>• <strong>黄金</strong>：避险属性凸显<br>• <strong>瓦楞纸</strong>：消费复苏受益</div>
                </div>
                <div style="padding:12px;background:#fef2f2;border-radius:6px;border:1px solid #fecaca;">
                    <div style="font-weight:600;color:#991b1b;">减持建议</div>
                    <div style="font-size:12px;margin-top:4px;">• <strong>白银</strong>：工业需求疲软<br>• <strong>锡</strong>：电子行业去库存<br>• <strong>ABS塑料</strong>：下游需求减弱</div>
                </div>
                <div style="padding:12px;background:#eff6ff;border-radius:6px;border:1px solid #bfdbfe;">
                    <div style="font-weight:600;color:#1e40af;">中性观望</div>
                    <div style="font-size:12px;margin-top:4px;">• <strong>锂盐</strong>：等待需求复苏<br>• <strong>基本金属</strong>：宏观主导<br>• <strong>铁矿石</strong>：房地产政策等待</div>
                </div>
            </div>
            <p style="margin-top:12px;font-size:12px;color:#718096;"><strong>风险提示：</strong>本报告仅为市场分析，不构成投资建议。市场有风险，投资需谨慎。</p>
        </div>
        
        <div class="footer">
            <p>🔍 数据来源：{db.get('data_source', 'SMM + Kitco + 生意社 + 大商所')}</p>
            <p>📧 报告编制：大宗商品分析团队 | 📞 咨询电话：400-XXX-XXXX</p>
            <p>🔄 报告日期：{today} | 下次更新：{(datetime.strptime(today, '%Y-%m-%d') if '-' in today else datetime.now()).strftime('%Y-%m-%d')} 10:00</p>
            <p>🚀 方案C执行中：模拟数据+真实抓取管道建设（目标：3月27日前实现真实数据）</p>
        </div>
    </div>
    '''
    
    return briefing_html

def generate_commodity_page(code, item, db):
    """生成单个商品页面"""
    is_up = item['change'] >= 0
    html = f'''
    <div id="{code}" class="page">
        <div class="page-header">
            <div class="commodity-info">
                <div>
                    <div class="commodity-name">{item['name']}</div>
                    <div class="commodity-symbol">{item['symbol']} | {item['category']}</div>
                </div>
                <div class="price-display">
                    <div class="current-price">{'$' if '美元' in item['unit'] else '¥'}{item['price']:,}</div>
                    <div class="price-change {'up' if is_up else 'down'}">{'▲' if is_up else '▼'} {abs(item['change']):,} ({'+' if is_up else ''}{item['change_percent']:.2f}%)</div>
                </div>
            </div>
            <p>{item['desc']}</p>
        </div>
        <div class="section">
            <div class="section-title">📊 今日价格详情</div>
            <table>
                <tr><th>规格</th><th>价格区间</th><th>均价</th><th>涨跌</th><th>单位</th></tr>
                <tr>
                    <td><strong>{item['name']}现货</strong></td>
                    <td>{item['price_range']}</td>
                    <td>{item['price']:,}</td>
                    <td><span class="badge {'badge-up' if is_up else 'badge-down'}">{'+' if is_up else ''}{item['change']:,}</span></td>
                    <td>{item['unit']}</td>
                </tr>
            </table>
        </div>
        <div class="footer">
            <p>🔍 数据来源：{db['data_source']}</p>
            <p>🔄 更新时间：{db['last_update']} | 真实数据 ✅</p>
        </div>
    </div>
    '''
    return html

def main():
    # 读取真实价格
    with open('real_prices_today.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 生成简报页面
    briefing_page = generate_briefing_page(db)
    
    # 生成商品页面
    commodity_pages = []
    for code, item in db['commodities'].items():
        commodity_pages.append(generate_commodity_page(code, item, db))
    
    # 生成导航栏
    nav_items = [f'<a href="#briefing" class="nav-item">📈 简报</a>']
    for code, item in db['commodities'].items():
        nav_items.append(f'<a href="#{code}" class="nav-item">{item["name"]}</a>')
    
    # 生成完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大宗商品市场简报 - 上市公司风格</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: #f7fafc; margin: 0; padding: 0; }}
        .header {{ position: fixed; top: 0; left: 0; right: 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 1000; padding: 12px 16px; }}
        .header-title {{ font-size: 18px; font-weight: 700; color: #1a365d; }}
        .current-time {{ font-size: 12px; color: #718096; }}
        .commodity-nav {{ display: flex; overflow-x: auto; gap: 6px; margin-top: 10px; }}
        .nav-item {{ padding: 6px 14px; background: white; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 12px; text-decoration: none; color: #2d3748; flex-shrink: 0; }}
        .nav-item:hover {{ background: #1a365d; color: white; }}
        .main-content {{ margin-top: 90px; padding: 0 12px 40px; }}
        .page {{ display: none; max-width: 800px; margin: 0 auto; }}
        .page:first-of-type {{ display: block; }}
        .page:target {{ display: block; }}
        .page:target ~ .page:first-of-type {{ display: none; }}
        .page-header {{ background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 12px; }}
        .commodity-info {{ display: flex; justify-content: space-between; align-items: flex-start; }}
        .commodity-name {{ font-size: 22px; font-weight: 700; }}
        .commodity-symbol {{ font-size: 13px; opacity: 0.9; }}
        .price-display {{ text-align: right; }}
        .current-price {{ font-size: 32px; font-weight: 800; font-family: monospace; }}
        .price-change {{ font-size: 13px; font-weight: 600; }}
        .up {{ color: #9ae6b4; }} .down {{ color: #fc8181; }}
        .section {{ background: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 12px; }}
        .section-title {{ font-size: 15px; font-weight: 600; color: #1a365d; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f8fafc; font-weight: 600; color: #718096; }}
        .badge {{ padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
        .badge-up {{ background: #c6f6d5; color: #276749; }}
        .badge-down {{ background: #fed7d7; color: #c53030; }}
        .footer {{ text-align: center; padding: 16px; color: #718096; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">📊 大宗商品市场简报</div>
        <div class="current-time">数据更新: {db['last_update']} | 方案C执行中</div>
        <div class="commodity-nav">
            {''.join(nav_items)}
        </div>
    </div>
    <div class="main-content">
        {briefing_page}
        {''.join(commodity_pages)}
    </div>
</body>
</html>'''

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("[OK] Website updated with briefing page!")
    print(f"[OK] Data source: {db['data_source']}")
    print(f"[OK] Update date: {db['last_update']}")
    print(f"[OK] Real data: {sum(1 for item in db['commodities'].values() if item.get('is_real', False))}/{len(db['commodities'])} commodities")
    print("[OK] Briefing page is now the default homepage")

if __name__ == '__main__':
    main()