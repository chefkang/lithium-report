@echo off
chcp 65001 >nul
echo ==========================================
echo   锂盐报告自动更新任务创建工具
echo ==========================================
echo.

:: 检查是否管理员
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 请以管理员身份运行此批处理！
    echo    右键点击此文件 → 以管理员身份运行
    pause
    exit /b 1
)

echo ✅ 管理员权限检查通过
echo.

:: 创建任务
schtasks /create /tn "锂盐报告每日更新" /tr "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File %USERPROFILE%\.openclaw\workspace\auto-update.ps1" /sc daily /st 09:00 /ru SYSTEM /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo ✅ 任务创建成功！
    echo.
    echo 📋 任务详情：
    echo    - 任务名称: 锂盐报告每日更新
    echo    - 运行时间: 每天 09:00
    echo    - 执行文件: auto-update.ps1
    echo    - 更新目标: https://chefkang.github.io/lithium-report/
    echo.
    echo 📝 查看任务：
    echo    任务计划程序 → 任务计划程序库 → 锂盐报告每日更新
    echo.
    echo 🔄 立即测试运行：
    echo    schtasks /run /tn "锂盐报告每日更新"
) else (
    echo ❌ 任务创建失败，错误代码: %errorlevel%
)

echo.
pause
