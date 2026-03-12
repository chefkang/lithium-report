#!/bin/bash
# GitHub Pages 缓存刷新脚本
# 使用方法: ./refresh-github-pages.sh [你的GitHub用户名] [仓库名] [Personal Access Token]

USERNAME=${1:-chefkang}
REPO=${2:-lithium-report}
TOKEN=$3

if [ -z "$TOKEN" ]; then
    echo "❌ 错误: 需要提供 GitHub Personal Access Token"
    echo ""
    echo "使用方法:"
    echo "  ./refresh-github-pages.sh <用户名> <仓库名> <Token>"
    echo ""
    echo "或者设置环境变量:"
    echo "  export GITHUB_TOKEN=你的Token"
    echo "  ./refresh-github-pages.sh"
    echo ""
    echo "如何创建Token:"
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 勾选 'repo' 权限"
    echo "  4. 生成后复制Token"
    exit 1
fi

echo "🚀 正在刷新 GitHub Pages 缓存..."
echo "仓库: $USERNAME/$REPO"
echo ""

# 方法1: 通过API触发Pages重新构建
echo "📡 方法1: 触发Pages重新构建..."
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$USERNAME/$REPO/pages/builds" \
  -s -o /dev/null -w "%{http_code}"

echo " ✅ 已发送刷新请求"
echo ""

# 方法2: 通过空提交强制更新
echo "📡 方法2: 强制空提交触发重建..."
git commit --allow-empty -m "Force Pages rebuild - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin master

echo "✅ 完成! GitHub Pages 将在 2-5 分钟内刷新"
echo ""
echo "💡 提示:"
echo "   - 可以访问 https://github.com/$USERNAME/$REPO/actions 查看构建状态"
echo "   - 如果仍不生效，可手动访问: https://github.com/$USERNAME/$REPO/settings/pages"
echo "   - 切换 Branch 到 None 再切回 master 可强制清空所有CDN缓存"
