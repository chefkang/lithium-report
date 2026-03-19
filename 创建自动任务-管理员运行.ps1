# 创建Windows定时任务 - 以管理员身份运行此脚本

Write-Host "=== 创建锂盐报告自动更新任务 ===" -ForegroundColor Cyan
Write-Host ""

# 任务参数
$taskName = "锂盐报告自动更新"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$env:USERPROFILE\.openclaw\workspace\auto-update.ps1`"" -WorkingDirectory "$env:USERPROFILE\.openclaw\workspace"

# 每天09:00触发
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"

# 设置：无论是否插电都运行，即使任务运行时间较长也不停止
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# 注册任务
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "每日09:00自动更新锂盐全球分析报告并推送到GitHub" -Force

Write-Host "✅ 任务创建成功！" -ForegroundColor Green
Write-Host ""
Write-Host "任务详情:" -ForegroundColor Yellow
Write-Host "  - 任务名称: $taskName" -ForegroundColor Gray
Write-Host "  - 运行时间: 每天 09:00" -ForegroundColor Gray
Write-Host "  - 执行脚本: $env:USERPROFILE\.openclaw\workspace\auto-update.ps1" -ForegroundColor Gray
Write-Host "  - 目标网站: https://chefkang.github.io/lithium-report/" -ForegroundColor Gray
Write-Host ""
Write-Host "查看任务: 打开 任务计划程序 → 任务计划程序库 → $taskName" -ForegroundColor Cyan

pause
