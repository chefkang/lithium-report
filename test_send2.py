import requests
import time

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=692c31203bf783597e521e8d8001d2571728dc0193b2a7342569e6fae35267a0'

# 发纯文本消息
payload = {
    'msgtype': 'text',
    'text': {
        'content': f'【OpenClaw测试】时间: {time.strftime("%H:%M:%S")} - 如果看到这条消息，说明Webhook工作正常！'
    }
}

try:
    resp = requests.post(webhook, json=payload, timeout=10)
    result = resp.json()
    print(f'状态: {resp.status_code}')
    print(f'结果: {result}')
    
    if result.get('errcode') == 0:
        print('\n✅ 钉钉API返回成功')
        print('如果群里没收到，请检查:')
        print('1. 机器人是否已添加到该群')
        print('2. 机器人是否被禁言')
        print('3. 群设置是否允许机器人发言')
    else:
        print(f'\n❌ 错误: {result}')
except Exception as e:
    print(f'错误: {e}')
