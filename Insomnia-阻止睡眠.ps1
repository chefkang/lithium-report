# 使用 Insomnia 阻止电脑睡眠（推荐用于长时间运行）
# 将此脚本保存为 .ps1 文件运行，或复制到 PowerShell 中执行

Write-Host "=== 启动 Insomnia 模式 - 阻止电脑睡眠 ===" -ForegroundColor Cyan
Write-Host "此脚本将保持电脑24小时运行，不会进入睡眠状态" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 可以停止" -ForegroundColor Yellow
Write-Host ""

# 使用 Windows API 阻止睡眠
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Power {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
    public const uint ES_CONTINUOUS = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED = 0x00000001;
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;
}
"@

# 设置执行状态，阻止睡眠
[Power]::SetThreadExecutionState([Power]::ES_CONTINUOUS -bor [Power]::ES_SYSTEM_REQUIRED -bor [Power]::ES_DISPLAY_REQUIRED)

Write-Host "✅ 已阻止电脑睡眠！AI 现在可以24小时自动运行" -ForegroundColor Green
Write-Host ""

# 保持运行
try {
    while($true) { 
        Start-Sleep -Seconds 60
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
} finally {
    # 恢复默认设置
    [Power]::SetThreadExecutionState([Power]::ES_CONTINUOUS)
    Write-Host ""
    Write-Host "已恢复默认电源设置" -ForegroundColor Yellow
}
