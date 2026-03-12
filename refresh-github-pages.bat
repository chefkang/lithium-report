@echo off
chcp 65001 >nul
cls
echo ==========================================
echo    GitHub Pages 自动刷新工具
echo ==========================================
echo.

:: 检查是否提供了Token
if "%~1"=="" (
    echo ❌ 错误: 需要提供 GitHub Personal Access Token
    echo.
    echo 使用方法:
    echo   refresh-github-pages.bat ^<你的Token^>
    echo.
    echo 如何创建Token:
    echo   1. 访问 https://github.com/settings/tokens
    echo   2. 点击 "Generate new token (classic)"
    echo   3. 勾选 "repo" 权限
    echo   4. 生成后复制Token
    echo.
    echo 示例:
    echo   refresh-github-pages.bat ghp_xxxxxxxxxxxx
    pause
    exit /b 1
)

set TOKEN=%~1
set USERNAME=chefkang
set REPO=lithium-report

echo 🚀 正在刷新 GitHub Pages 缓存...
echo 仓库: %USERNAME%/%REPO%
echo.

:: 方法1: 触发Pages重新构建
echo 📡 方法1: 触发Pages重新构建...
curl -X POST -H "Authorization: token %TOKEN%" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/repos/%USERNAME%/%REPO%/pages/builds" -s -o nul -w "%%{http_code}"
echo  ✅ 已发送刷新请求
echo.

:: 方法2: 更新时间戳并推送
echo 📡 方法2: 更新文件时间戳...

:: 获取当前时间
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set YEAR=%datetime:~0,4%
set MONTH=%datetime:~4,2%
set DAY=%datetime:~6,2%
set HOUR=%datetime:~8,2%
set MINUTE=%datetime:~10,2%
set TIMESTAMP=%YEAR%-%MONTH%-%DAY% %HOUR%:%MINUTE%:00

echo 当前时间: %TIMESTAMP%

:: 使用时间戳更新文件
powershell -Command "(Get-Content index.html) -replace '<div class=\"current-time\">.*?</div>', '<div class=\"current-time\">%TIMESTAMP% CST</div>' | Set-Content index.html"

echo  ✅ 已更新时间戳
echo.

:: Git提交
echo 📡 方法3: Git推送...
git add index.html
git commit -m "Auto refresh - %TIMESTAMP%"
git push origin master

echo.
echo ==========================================
echo ✅ 完成! GitHub Pages 将在 2-5 分钟内刷新
echo ==========================================
echo.
echo 💡 提示:
echo    - 可以访问 https://github.com/%USERNAME%/%REPO%/actions 查看状态
echo    - 网站地址: https://%USERNAME%.github.io/%REPO%/
echo    - 如果仍不生效，访问设置页手动切换Branch:
echo      https://github.com/%USERNAME%/%REPO%/settings/pages
echo.
pause
