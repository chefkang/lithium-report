schtasks /create /tn "锂盐报告自动更新" /tr "powershell.exe -ExecutionPolicy Bypass -File %USERPROFILE%\.openclaw\workspace\auto-update.ps1" /sc daily /st 09:00 /ru SYSTEM /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo ✅ 自动任务创建成功！
    echo 每天09:00会自动更新锂盐报告并推送到GitHub
    echo 查看任务: 任务计划程序 -^> 锂盐报告自动更新
) else (
    echo ❌ 创建失败，请确保以管理员身份运行此批处理
)

pause
