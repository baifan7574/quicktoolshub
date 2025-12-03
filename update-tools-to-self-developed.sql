-- 将外部链接工具改为自开发工具的更新脚本
-- 在Supabase SQL Editor中运行此脚本

-- ============================================
-- 更新工具类型：从 external_link 改为 self_developed
-- ============================================

-- 1. PDF Compressor - 改为自开发
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug = 'pdf-compressor';

-- 2. Image Converter - 改为自开发
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug = 'image-converter';

-- ============================================
-- 验证更新结果
-- ============================================
-- 运行这个查询来查看更新后的工具：
SELECT 
  name, 
  slug, 
  tool_type, 
  external_url,
  is_active
FROM tools
WHERE slug IN ('pdf-compressor', 'image-converter')
ORDER BY name;

-- 查看所有自开发工具：
SELECT 
  name, 
  slug, 
  tool_type,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
WHERE tool_type = 'self_developed'
ORDER BY categories.name, tools.name;

