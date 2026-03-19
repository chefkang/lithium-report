# 创建锂盐报告自动更新任务 - 直接执行版

# 以管理员身份运行PowerShell，然后复制粘贴以下内容执行

$taskName = "LithiumReportAutoUpdate"
$scriptPath = "$env:USERPROFILE\.openclaw\workspace\auto-update.ps1"
$workspace = "$env:USERPROFILE\.openclaw\workspace"

# 创建动作
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`"" `
    -WorkingDirectory $workspace

# 创建触发器 - 每天09:00
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"

# 创建设置
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# 注册任务
Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "每日09:00自动更新锂盐价格报告并推送到GitHub" `
    -Force

Write-Host "✅ 任务创建成功！" -ForegroundColor Green
Write-Host "任务名: $taskName" -ForegroundColor Cyan
Write-Host "运行时间: 每天 09:00" -ForegroundColor Cyan

# 显示任务信息
Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo
