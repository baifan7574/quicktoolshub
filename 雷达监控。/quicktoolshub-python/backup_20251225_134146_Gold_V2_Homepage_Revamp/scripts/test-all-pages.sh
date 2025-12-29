#!/bin/bash

# 测试所有页面和链接的脚本

BASE_URL="http://localhost:3000"

echo "========================================="
echo "开始测试所有页面和链接"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_url() {
    local url=$1
    local name=$2
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✓${NC} $name: $url (状态码: $status_code)"
        return 0
    else
        echo -e "${RED}✗${NC} $name: $url (状态码: $status_code)"
        return 1
    fi
}

# 统计
total=0
passed=0
failed=0

# 测试基础页面
echo "=== 基础页面 ==="
test_url "$BASE_URL/" "首页" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/health" "健康检查" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/tools" "工具列表" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/blog" "博客列表" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/search" "搜索页面" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/categories" "分类页面" && ((passed++)) || ((failed++)); ((total++))

echo ""
echo "=== 静态页面 ==="
test_url "$BASE_URL/about" "关于我们" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/contact" "联系我们" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/privacy-policy" "隐私政策" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/terms-of-service" "服务条款" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/cookie-policy" "Cookie政策" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/disclaimer" "免责声明" && ((passed++)) || ((failed++)); ((total++))

echo ""
echo "=== API 端点 ==="
test_url "$BASE_URL/api/health" "API健康检查" && ((passed++)) || ((failed++)); ((total++))

echo ""
echo "=== 工具分类页面（示例）==="
test_url "$BASE_URL/categories/pdf-tools" "PDF工具分类" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/categories/image-tools" "图片工具分类" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/categories/text-tools" "文本工具分类" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/categories/developer-tools" "开发者工具分类" && ((passed++)) || ((failed++)); ((total++))

echo ""
echo "=== 工具列表筛选 ==="
test_url "$BASE_URL/tools?category=all" "所有工具" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/tools?sort=popular" "热门工具" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/tools?sort=recent" "最新工具" && ((passed++)) || ((failed++)); ((total++))
test_url "$BASE_URL/tools?sort=alphabetical" "字母排序" && ((passed++)) || ((failed++)); ((total++))

echo ""
echo "========================================="
echo "测试结果汇总"
echo "========================================="
echo -e "总计: ${total} 个页面"
echo -e "${GREEN}通过: ${passed}${NC}"
echo -e "${RED}失败: ${failed}${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ 所有页面测试通过！${NC}"
    exit 0
else
    echo -e "${RED}✗ 有 ${failed} 个页面测试失败${NC}"
    exit 1
fi

