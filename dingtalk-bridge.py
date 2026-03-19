"""
钉钉群机器人 → OpenClaw 桥接服务
使用钉钉群机器人 Webhook 方式
"""

import os
import json
import time
import hmac
import hashlib
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests

# ============ 配置 ============

# 钉钉群机器人配置（从钉钉群设置里获取）
DINGTALK_WEBHOOK_URL = os.getenv("DINGTALK_WEBHOOK_URL", "")
DINGTALK_SECRET = os.getenv("DINGTALK_SECRET", "")  # 加签密钥（如果开启了加签）

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789")
OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN", "")

# 桥接服务端口
BRIDGE_PORT = int(os.getenv("BRIDGE_PORT", "3001"))

# 存储 webhook URL（用于回复）
webhook_cache = {}


class DingTalkBridgeHandler(BaseHTTPRequestHandler):
    """处理钉钉 Webhook 请求"""
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {args[0]}")
    
    def do_GET(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "service": "dingtalk-bridge",
            "features": ["群机器人消息接收", "自动回复"]
        }, ensure_ascii=False).encode())
    
    def do_POST(self):
        """处理钉钉消息推送"""
        parsed_path = urlparse(self.path)
        
        # 只处理 /webhook 路径
        if parsed_path.path != '/webhook':
            self._send_error(404, "Not found")
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            print(f"\n{'='*50}")
            print(f"收到钉钉消息: {json.dumps(data, ensure_ascii=False, indent=2)}")
            print(f"{'='*50}")
            
            # 处理消息
            self._handle_message(data)
            
            # 钉钉要求返回 success
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"errcode": 0, "errmsg": "ok"}).encode())
            
        except Exception as e:
            print(f"处理消息出错: {e}")
            import traceback
            traceback.print_exc()
            self._send_error(500, str(e))
    
    def _handle_message(self, data):
        """处理钉钉消息"""
        # 获取消息类型
        msg_type = data.get('msgtype')
        
        if msg_type == 'text':
            self._handle_text(data)
        else:
            print(f"暂不处理的消息类型: {msg_type}")
    
    def _handle_text(self, data):
        """处理文本消息"""
        sender = data.get('senderStaffId', 'unknown')
        sender_name = data.get('senderStaffName', sender)
        content = data.get('text', {}).get('content', '').strip()
        
        # 移除 @机器人的部分（如果有）
        at_users = data.get('atUsers', [])
        for user in at_users:
            at_text = f"@{user.get('name', '')}"
            content = content.replace(at_text, '').strip()
        
        print(f"用户 {sender_name}({sender}) 说: {content}")
        
        # 发送到 OpenClaw
        reply = self._send_to_openclaw(content, sender, sender_name)
        
        if reply:
            # 回复到钉钉
            self._send_reply(reply)
        else:
            self._send_reply("抱歉，我现在无法处理消息，请稍后再试。")
    
    def _send_to_openclaw(self, message, user_id, user_name):
        """发送消息到 OpenClaw 并获取回复"""
        try:
            # 构建发送到 OpenClaw 的请求
            # 使用 OpenClaw 的 HTTP API 或 WebSocket
            
            headers = {
                "Content-Type": "application/json"
            }
            if OPENCLAW_TOKEN:
                headers["Authorization"] = f"Bearer {OPENCLAW_TOKEN}"
            
            # 这里我们需要调用 OpenClaw 的 API
            # 由于 OpenClaw 主要是 WebSocket，我们用一种变通方式：
            # 创建一个特殊的会话，消息会被转发到 agent
            
            # 简化版本：直接返回测试消息
            # 实际使用时需要接入 OpenClaw 的消息处理流程
            
            return f"收到你的消息：{message}\n\n（钉钉桥接测试 - 完整集成需要进一步开发）"
            
        except Exception as e:
            print(f"发送到 OpenClaw 失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _send_reply(self, message):
        """发送回复到钉钉群"""
        if not DINGTALK_WEBHOOK_URL:
            print("错误: 未配置 DINGTALK_WEBHOOK_URL")
            return
        
        try:
            # 构建签名（如果配置了 SECRET）
            timestamp = str(round(time.time() * 1000))
            
            if DINGTALK_SECRET:
                string_to_sign = f"{timestamp}\n{DINGTALK_SECRET}"
                sign = hmac.new(
                    DINGTALK_SECRET.encode('utf-8'),
                    string_to_sign.encode('utf-8'),
                    hashlib.sha256
                ).digest()
                sign = base64.b64encode(sign).decode('utf-8')
                
                url = f"{DINGTALK_WEBHOOK_URL}&timestamp={timestamp}&sign={requests.utils.quote(sign)}"
            else:
                url = DINGTALK_WEBHOOK_URL
            
            # 构建消息
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            print(f"发送回复到钉钉: {message[:100]}...")
            
            resp = requests.post(url, json=payload, timeout=10)
            result = resp.json()
            
            if result.get('errcode') == 0:
                print("✅ 回复发送成功")
            else:
                print(f"❌ 发送失败: {result}")
                
        except Exception as e:
            print(f"发送回复失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _send_error(self, code, message):
        """返回错误响应"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"errcode": code, "errmsg": message}).encode())


def run_bridge():
    """启动桥接服务"""
    server = HTTPServer(('0.0.0.0', BRIDGE_PORT), DingTalkBridgeHandler)
    
    print("=" * 60)
    print("🤖 钉钉群机器人 → OpenClaw 桥接服务")
    print("=" * 60)
    print(f"\n📡 监听地址: http://0.0.0.0:{BRIDGE_PORT}")
    print(f"📋 Webhook 地址: http://你的IP:{BRIDGE_PORT}/webhook")
    print(f"🔍 健康检查: http://localhost:{BRIDGE_PORT}/")
    print("\n" + "=" * 60)
    print("环境变量检查:")
    print(f"  DINGTALK_WEBHOOK_URL: {'✅ 已设置' if DINGTALK_WEBHOOK_URL else '❌ 未设置'}")
    print(f"  DINGTALK_SECRET: {'✅ 已设置' if DINGTALK_SECRET else '⚪ 未设置(无加签)'}")
    print(f"  OPENCLAW_GATEWAY_URL: {OPENCLAW_GATEWAY_URL}")
    print(f"  OPENCLAW_TOKEN: {'✅ 已设置' if OPENCLAW_TOKEN else '⚪ 未设置'}")
    print("=" * 60)
    print("\n使用说明:")
    print("1. 在钉钉群中添加机器人")
    print("2. 复制 Webhook 地址，设置到 DINGTALK_WEBHOOK_URL")
    print("3. 设置钉钉机器人的回调地址为: http://你的IP:3001/webhook")
    print("4. 重启服务，开始接收消息\n")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务已停止")
        server.shutdown()


if __name__ == "__main__":
    run_bridge()
