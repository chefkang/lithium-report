"""
钉钉群机器人 Webhook 测试工具
可以主动发送消息到钉钉群
"""

import os
import json
import time
import hmac
import hashlib
import base64
import requests


def send_dingtalk_message(webhook_url, secret, message):
    """发送消息到钉钉群"""
    try:
        # 构建签名（如果配置了 SECRET）
        timestamp = str(round(time.time() * 1000))
        
        if secret:
            string_to_sign = f"{timestamp}\n{secret}"
            sign = hmac.new(
                secret.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
            sign = base64.b64encode(sign).decode('utf-8')
            
            from urllib.parse import quote
            url = f"{webhook_url}&timestamp={timestamp}&sign={quote(sign)}"
        else:
            url = webhook_url
        
        # 构建消息
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OpenClaw 连接测试",
                "text": f"## 🤖 OpenClaw 钉钉连接测试\n\n{message}\n\n---\n发送时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }
        
        print(f"正在发送消息到钉钉...")
        resp = requests.post(url, json=payload, timeout=10)
        result = resp.json()
        
        if result.get('errcode') == 0:
            print("✅ 消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_connection():
    """测试钉钉连接"""
    print("=" * 50)
    print("钉钉机器人 Webhook 测试")
    print("=" * 50)
    
    webhook_url = input("\n请输入钉钉机器人的 Webhook 地址:\n> ").strip()
    
    if not webhook_url:
        print("错误: Webhook 地址不能为空")
        return
    
    secret = input("\n请输入加签密钥 (如果没有加签直接回车):\n> ").strip()
    
    message = input("\n请输入要发送的消息 (默认: OpenClaw 已连接):\n> ").strip()
    if not message:
        message = "OpenClaw 已成功连接！🎉\n\n现在你可以：\n1. 在本窗口跟我对话\n2. 我会把回复通过机器人发到钉钉群"
    
    print("\n" + "=" * 50)
    send_dingtalk_message(webhook_url, secret, message)
    print("=" * 50)


if __name__ == "__main__":
    test_connection()
