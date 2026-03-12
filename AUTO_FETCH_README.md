# 浏览器自动化数据抓取方案

## 安装步骤

### 1. 安装 Playwright
打开 PowerShell，运行：
```bash
cd C:\Users\陈定平\.openclaw\workspace
uv pip install playwright
playwright install chromium
```

### 2. 运行抓取脚本
```bash
uv run python auto_fetch_data.py
```

### 3. 查看结果
- 脚本会自动打开浏览器
- 访问 SMM 和生意社网站
- 截图保存到当前目录
- 数据保存到 `fetched_data.json`

### 4. 更新网页
如果抓取成功，运行：
```bash
uv run python update_website.py
```

## 注意事项

1. **首次运行需要安装 Chromium**（约100MB）
2. **浏览器可见**：默认会显示浏览器窗口，可以看到抓取过程
3. **反检测**：脚本已添加反自动化检测代码
4. **等待时间**：每个页面加载需要3-5秒，请耐心等待

## 如果抓取失败

可能的原因：
- 网站更新了页面结构
- 需要登录才能查看数据
- 网站有更强的反爬机制

解决方案：
1. 手动打开浏览器查看数据
2. 使用 `data-entry.html` 手动录入
3. 购买商业API（推荐 Wind 或 同花顺）

## 法律说明

浏览器自动化本身不违法，但请遵守：
- 不要过于频繁抓取（建议每天1-2次）
- 不要用于商业目的
- 遵守网站的服务条款
