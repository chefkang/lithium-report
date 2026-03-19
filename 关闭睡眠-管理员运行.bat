# 关闭电脑睡眠 - 请右键以管理员身份运行此脚本

Write-Host "=== 正在配置电脑不休眠设置 ===" -ForegroundColor Green

# 关闭睡眠（插电）
powercfg /change standby-timeout-ac 0
Write-Host "✅ 已关闭插电时的睡眠" -ForegroundColor Green

# 关闭睡眠（电池）
powercfg /change standby-timeout-dc 0
Write-Host "✅ 已关闭电池时的睡眠" -ForegroundColor Green

# 关闭显示器（可选）
powercfg /change monitor-timeout-ac 0
Write-Host "✅ 已关闭显示器自动关闭" -ForegroundColor Green

# 关闭硬盘休眠
powercfg /change disk-timeout-ac 0
Write-Host "✅ 已关闭硬盘休眠" -ForegroundColor Green

Write-Host ""
Write-Host "=== 所有设置已完成 ===" -ForegroundColor Green
Write-Host "电脑将24小时保持运行，AI可以自动更新报告" -ForegroundColor Cyan
Write-Host ""
Write-Host "如需恢复默认设置，请运行:" -ForegroundColor Yellow
Write-Host "powercfg /change standby-timeout-ac 30" -ForegroundColor Gray
Write-Host "(30表示30分钟后睡眠)" -ForegroundColor Gray

pause
