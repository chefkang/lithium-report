@echo off
chcp 65001 >nul
title GitHub 网络优化工具

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 请以管理员身份运行此脚本！
    echo 右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ==========================================
echo      GitHub 网络优化工具
echo ==========================================
echo.

:: 备份hosts文件
echo [1/4] 备份当前hosts文件...
copy /Y C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.bak.%date:~0,4%%date:~5,2%%date:~8,2% >nul 2>&1
echo ✓ 备份完成

:: 清理旧GitHub条目
echo.
echo [2/4] 清理旧GitHub配置...
findstr /V "github.com githubusercontent githubassets codeload" C:\Windows\System32\drivers\etc\hosts > %TEMP%\hosts_temp.txt
copy /Y %TEMP%\hosts_temp.txt C:\Windows\System32\drivers\etc\hosts >nul
echo ✓ 清理完成

:: 添加GitHub加速IP
echo.
echo [3/4] 添加GitHub加速IP...
echo. >> C:\Windows\System32\drivers\etc\hosts
echo # GitHub 加速配置 - %date% %time% >> C:\Windows\System32\drivers\etc\hosts

:: 使用多个IP源
echo 140.82.114.4 github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 www.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.113.4 github.com >> C:\Windows\System32\drivers\etc\hosts
echo 20.205.243.166 github.com >> C:\Windows\System32\drivers\etc\hosts
echo 20.205.243.166 api.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.108.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.109.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.110.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.111.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.108.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.109.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.110.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.111.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.112.21 central.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.108.133 raw.githubusercontent.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.109.133 raw.githubusercontent.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.110.133 raw.githubusercontent.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.111.133 raw.githubusercontent.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.9 codeload.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 52.216.114.35 github-cloud.s3.amazonaws.com >> C:\Windows\System32\drivers\etc\hosts
echo 20.205.243.166 gist.github.com >> C:\Windows\System32\drivers\etc\hosts

echo ✓ 加速IP添加完成

:: 刷新DNS
echo.
echo [4/4] 刷新DNS缓存...
ipconfig /flushdns >nul
echo ✓ DNS缓存已刷新

echo.
echo ==========================================
echo      优化完成！
echo ==========================================
echo.
echo 建议操作：
echo 1. 重启浏览器
echo 2. 如果仍无法访问，尝试重启电脑
echo 3. 定期运行此脚本更新IP（IP可能失效）
echo.
echo 备份文件位置：
echo C:\Windows\System32\drivers\etc\hosts.bak.%date:~0,4%%date:~5,2%%date:~8,2%
echo.
pause
