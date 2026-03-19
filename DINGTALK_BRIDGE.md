# 钉钉群机器人配置指南

## 快速开始（5分钟）

### 第1步：创建钉钉群机器人

1. 打开钉钉，进入你想添加机器人的群
2. 点击群设置 → 智能群助手 → 添加机器人
3. 选择 **「自定义机器人」**
4. 设置：
   - 机器人名字：比如 "AI 助手"
   - 安全设置：选择 **「加签」**（推荐）
5. 完成后复制：
   - **Webhook 地址**（如：`https://oapi.dingtalk.com/robot/send?access_token=xxx`）
   - **加签密钥**（如：`SECxxx`）

### 第2步：配置桥接服务

在 PowerShell 中设置环境变量：

```powershell
$env:DINGTALK_WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=你的token"
$env:DINGTALK_SECRET = "SEC你的密钥"
$env:OPENCLAW_GATEWAY_URL = "http://127.0.0.1:18789"
$env:OPENCLAW_TOKEN = "clawx-你的token"
```

从 `~/.openclaw/openclaw.json` 中找到你的 gateway token：
```json
{
  "gateway": {
    "auth": {
      "token": "clawx-4ecc4bf0461efae23ea16f10f1e6e996"
    }
  }
}
```

### 第3步：启动桥接服务

```bash
cd ~/.openclaw/workspace
uv run python dingtalk-bridge.py
```

看到以下输出说明启动成功：
```
============================================================
🤖 钉钉群机器人 → OpenClaw 桥接服务
============================================================

📡 监听地址: http://0.0.0.0:3001
📋 Webhook 地址: http://你的IP:3001/webhook
🔍 健康检查: http://localhost:3001/
```

### 第4步：配置钉钉回调（关键）

**问题**：钉钉需要公网地址才能推送消息，但你电脑在内网。

**解决方案**：使用内网穿透工具

#### 方案 A：使用 ngrok（推荐，简单）

1. 注册 ngrok：https://ngrok.com
2. 下载并安装
3. 运行：
```bash
ngrok http 3001
```
4. 你会得到一个公网地址，如 `https://abc123.ngrok.io`
5. 在钉钉机器人设置中，添加回调地址：
   ```
   https://abc123.ngrok.io/webhook
   ```

#### 方案 B：使用花生壳（国内）

1. 注册花生壳：https://hsk.oray.com
2. 配置内网映射：端口 3001
3. 获得域名，填入钉钉回调

#### 方案 C：部署到服务器（最稳定）

把桥接服务部署到有公网IP的服务器上运行。

---

## 测试

配置完成后，在钉钉群里 @机器人 发送消息：

```
@AI助手 你好
```

如果一切正常，机器人会回复：
```
收到你的消息：你好

（钉钉桥接测试 - 完整集成需要进一步开发）
```

---

## 常见问题

### Q: 消息发出去没有回复？

1. 检查桥接服务是否运行（看窗口有没有日志输出）
2. 检查 ngrok/内网穿透是否正常
3. 检查钉钉机器人设置里的回调地址是否正确
4. 检查加签密钥是否正确（如果开启了加签）

### Q: 如何查看日志？

桥接服务会实时打印日志，看看有没有收到消息。

### Q: 重启电脑后需要重新启动？

是的，目前需要手动启动。可以配置为 Windows 服务自动启动（进阶）。

---

## 进阶：完整集成 OpenClaw

当前版本是简化版，只能回复固定消息。完整集成需要：

1. 通过 OpenClaw Gateway API 创建会话
2. 将用户消息转发到 agent
3. 接收 agent 回复并返回钉钉

这部分需要更多开发，如果需要可以进一步实现。

