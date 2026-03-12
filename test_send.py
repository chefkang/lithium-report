import requests
import json
import time

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=692c31203bf783597e521e8d8001d2571728dc0193b2a7342569e6fae35267a0'

payload = {
    'msgtype': 'markdown',
    'markdown': {
        'title': 'OpenClaw 连接测试',
        'text': '## 🤖 OpenClaw 钉钉连接测试\n\n✅ **消息发送成功！**\n\n现在你可以：\n- 在钉钉群里 @我 进行对话\n- 我会通过回复消息与你互动\n\n---\n时间: ' + time.strftime('%Y-%m-%d %H:%M:%S')
    }
}

resp = requests.post(webhook, json=payload, timeout=10)
print('状态码:', resp.status_code)
print('响应:', resp.json())
