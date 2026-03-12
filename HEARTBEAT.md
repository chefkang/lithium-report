# Heartbeat 任务清单 - 锂盐报告自动更新

## 每日上午09:00检查
- **任务**: 更新锂盐全球深度分析报告
- **检查项**:
  1. 获取最新碳酸锂价格数据
  2. 获取最新氢氧化锂价格数据
  3. 抓取最新行业新闻（SMM、百川、Reuters等）
  4. 更新HTML报告中的价格、新闻、分析
  5. 保存更新记录到 memory/lithium-report-updates.md

## 触发条件
每天早上9点自动检查并更新。

## 文件位置
- 报告: `workspace/index.html` (12种大宗商品监控系统)
- 更新日志: `memory/lithium-report-updates.md`
