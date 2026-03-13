# Heartbeat 任务清单 - 大宗商品监控系统

## 每日上午09:00检查
- **任务**: 更新12种大宗商品价格
- **检查项**:
  1. 抓取SMM首页真实价格数据
  2. 记录到价格历史数据库
  3. 更新网站显示
  4. 推送到GitHub
  5. 记录更新日志

## 60天价格记录计划
- **开始日期**: 2026-03-12
- **目标**: 记录60天真实价格形成完整趋势图
- **当前进度**: 60/60 天
- **预计完成**: 2026-03-13（已完成）

## 数据来源
- **主要来源**: SMM上海有色网首页 (https://www.smm.cn)
- **抓取方式**: 浏览器自动化抓取首页价格表格
- **数据类型**: 真实市场价格（非模拟）

## 记录的商品（12种）
1. 碳酸锂 (Lithium Carbonate)
2. 氢氧化锂 (Lithium Hydroxide)
3. 铜 (Copper)
4. 铝 (Aluminum)
5. 锡 (Tin)
6. 镍 (Nickel)
7. 黄金 (Gold)
8. 白银 (Silver)
9. 铁矿石 (Iron Ore)
10. ABS塑料 (ABS Plastic)
11. 瓦楞纸 (Corrugated Paper)
12. 原油 (Crude Oil)

## 文件位置
- **价格数据库**: `workspace/real_prices_today.json`
- **历史记录**: `workspace/commodity_price_db.json`
- **网站文件**: `workspace/index.html`
- **更新脚本**: `workspace/daily_price_update.py`
- **网站地址**: https://chefkang.github.io/lithium-report/

## 触发条件
每天早上9点自动执行价格抓取和更新。

## 更新日志
- **2026-03-13 09:14**: 自动更新完成，60天真实数据已记录，网站已更新并推送至GitHub。
