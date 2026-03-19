import json
from datetime import datetime

# 读取数据库
with open('commodity_price_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 清理每个商品的价格历史，只保留真实数据
cleaned_count = 0
for commodity_id, commodity_data in db['commodities'].items():
    if 'price_history' in commodity_data:
        # 只保留 is_real: true 的记录
        real_history = [record for record in commodity_data['price_history'] if record.get('is_real', False)]
        commodity_data['price_history'] = real_history
        cleaned_count += len(real_history)
        print(f"[OK] {commodity_data['name']}: 保留 {len(real_history)} 条真实数据")

# 更新元数据
db['start_date'] = '2026-03-12'  # 真实数据开始日期
db['last_update'] = '2026-03-13'  # 最后一次更新日期
db['progress_days'] = 2  # 真实数据天数
db['total_days_needed'] = 60  # 总需要天数
db['estimated_completion'] = '2026-05-10'  # 预计完成日期（2 + 58天）

# 保存清理后的数据库
with open('commodity_price_db_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"\n[OK] 数据清理完成！")
print(f"[INFO] 真实数据条数: {cleaned_count}")
print(f"[INFO] 数据开始日期: {db['start_date']}")
print(f"[INFO] 最后更新日期: {db['last_update']}")
print(f"[INFO] 进度: {db['progress_days']}/{db['total_days_needed']} 天")
print(f"[INFO] 预计完成: {db['estimated_completion']} (需要 {db['total_days_needed'] - db['progress_days']} 天)")
print(f"[INFO] 保存到: commodity_price_db_cleaned.json")

# 备份原文件
import shutil
shutil.copy2('commodity_price_db.json', 'commodity_price_db_backup.json')
print(f"📁 原文件已备份: commodity_price_db_backup.json")