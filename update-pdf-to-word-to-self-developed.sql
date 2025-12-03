-- 将 PDF to Word 工具更新为自开发工具
-- 在 Supabase SQL Editor 中运行此脚本

-- ============================================
-- 更新 PDF to Word 工具
-- ============================================

UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug = 'pdf-to-word';

-- ============================================
-- 验证更新结果
-- ============================================

-- 查看更新后的工具信息
SELECT 
  tools.name, 
  tools.slug, 
  tools.tool_type,
  tools.external_url,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
WHERE tools.slug = 'pdf-to-word';

-- 查看所有自开发工具
SELECT 
  tools.name, 
  tools.slug, 
  tools.tool_type,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
WHERE tools.tool_type = 'self_developed'
ORDER BY categories.name, tools.name;

