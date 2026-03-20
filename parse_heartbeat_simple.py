#!/usr/bin/env python3
"""
简单解析HEARTBEAT.md文件
"""

import re
from datetime import datetime

def parse_heartbeat_simple():
    """简单解析HEARTBEAT.md文件"""
    with open('HEARTBEAT.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stages = {}
    current_stage = None
    in_stage = False
    current_tasks = []
    
    for line in lines:
        line = line.strip()
        
        # 检查阶段标题
        if line.startswith('### 阶段'):
            # 保存上一个阶段
            if current_stage is not None and current_tasks:
                completed = sum(1 for t in current_tasks if t['status'] == 'completed')
                total = len(current_tasks)
                progress = int((completed / total * 100)) if total > 0 else 0
                
                stages[f'stage{current_stage["number"]}'] = {
                    'number': current_stage['number'],
                    'title': current_stage['title'],
                    'timeframe': current_stage['timeframe'],
                    'tasks': current_tasks.copy(),
                    'completed_tasks': completed,
                    'total_tasks': total,
                    'progress': progress,
                    'status': 'completed' if progress == 100 else 'in_progress' if current_stage['number'] == 1 else 'planned'
                }
            
            # 解析新阶段
            match = re.match(r'###\s*阶段(\d+)[:：]\s*(.+?)\s*\((.*?)\)', line)
            if match:
                stage_num, title, timeframe = match.groups()
                current_stage = {
                    'number': int(stage_num),
                    'title': title.strip(),
                    'timeframe': timeframe.strip()
                }
                current_tasks = []
                in_stage = True
            continue
        
        # 在阶段中解析任务
        if in_stage and line.startswith('- '):
            task_text = line[2:].strip()
            
            # 检查emoji状态
            if '✅' in task_text:
                emoji = '✅'
                status = 'completed'
                task_desc = task_text.replace('✅', '').strip()
            elif '🔄' in task_text:
                emoji = '🔄'
                status = 'in_progress'
                task_desc = task_text.replace('🔄', '').strip()
            elif '📅' in task_text:
                emoji = '📅'
                status = 'planned'
                task_desc = task_text.replace('📅', '').strip()
            elif '📈' in task_text:
                emoji = '📈'
                status = 'planned'
                task_desc = task_text.replace('📈', '').strip()
            elif '🚨' in task_text:
                emoji = '🚨'
                status = 'planned'
                task_desc = task_text.replace('🚨', '').strip()
            elif '📊' in task_text:
                emoji = '📊'
                status = 'planned'
                task_desc = task_text.replace('📊', '').strip()
            elif '🔍' in task_text:
                emoji = '🔍'
                status = 'planned'
                task_desc = task_text.replace('🔍', '').strip()
            elif '📰' in task_text:
                emoji = '📰'
                status = 'planned'
                task_desc = task_text.replace('📰', '').strip()
            elif '🤖' in task_text:
                emoji = '🤖'
                status = 'planned'
                task_desc = task_text.replace('🤖', '').strip()
            elif '⚙️' in task_text:
                emoji = '⚙️'
                status = 'in_progress'
                task_desc = task_text.replace('⚙️', '').strip()
            else:
                emoji = ''
                status = 'planned'
                task_desc = task_text
            
            current_tasks.append({
                'description': task_desc,
                'status': status,
                'emoji': emoji
            })
        
        # 阶段结束条件
        elif in_stage and line.startswith('##'):
            in_stage = False
    
    # 处理最后一个阶段
    if current_stage is not None and current_tasks:
        completed = sum(1 for t in current_tasks if t['status'] == 'completed')
        total = len(current_tasks)
        progress = int((completed / total * 100)) if total > 0 else 0
        
        stages[f'stage{current_stage["number"]}'] = {
            'number': current_stage['number'],
            'title': current_stage['title'],
            'timeframe': current_stage['timeframe'],
            'tasks': current_tasks.copy(),
            'completed_tasks': completed,
            'total_tasks': total,
            'progress': progress,
            'status': 'completed' if progress == 100 else 'in_progress' if current_stage['number'] == 1 else 'planned'
        }
    
    # 解析更新日志
    recent_logs = []
    for line in lines:
        line = line.strip()
        if line.startswith('- **') and '**:' in line:
            # 格式: - **2026-03-20 09:37**: 方案C阶段2开始...
            match = re.match(r'-\s+\*\*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\*\*[:：]\s*(.+)', line)
            if match:
                date_str, log_text = match.groups()
                recent_logs.append({
                    'date': date_str,
                    'text': log_text.strip()
                })
    
    # 只保留最近5条
    recent_logs = recent_logs[:5]
    
    # 系统状态
    system_status = {
        '简报样式': '上市公司风格 ✅',
        '执行方案': '方案C（混合方案）',
        '数据真实性': '4/12原型阶段',
        '自动更新': '每日10:00 ✅',
        '真实数据目标': '3月27日前实现',
        '历史记录': '第5天/目标60天'
    }
    
    return {
        'stages': stages,
        'recent_logs': recent_logs,
        'system_status': system_status,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# 测试函数
if __name__ == '__main__':
    data = parse_heartbeat_simple()
    print(f"解析到 {len(data['stages'])} 个阶段")
    for stage_num, stage in data['stages'].items():
        print(f"阶段{stage_num}: {stage['title']} - {stage['progress']}%")
        for task in stage['tasks']:
            print(f"  {task['emoji']} {task['description']} ({task['status']})")
    
    print(f"\n最近更新:")
    for log in data['recent_logs']:
        print(f"  [{log['date']}] {log['text']}")