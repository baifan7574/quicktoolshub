-- 将所有自开发工具更新为 self_developed 类型的脚本
-- 在Supabase SQL Editor中运行此脚本
-- 这个脚本会更新所有已开发完成的工具

-- ============================================
-- 第一步：查看当前工具状态（用于验证）
-- ============================================
-- 运行这个查询来查看所有工具及其类型：
SELECT 
  tools.name, 
  tools.slug, 
  tools.tool_type, 
  tools.external_url,
  tools.is_active,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
ORDER BY categories.name, tools.name;

-- ============================================
-- 第二步：更新所有自开发工具
-- ============================================

-- PDF Tools 分类的自开发工具
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug IN (
  'pdf-merger',
  'pdf-splitter',
  'pdf-compressor'
);

-- Image Tools 分类的自开发工具
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug IN (
  'image-compressor',
  'image-resizer',
  'image-converter',
  'background-remover'
);

-- Text Tools 分类的自开发工具
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug IN (
  'word-counter',
  'text-case-converter',
  'lorem-ipsum-generator'
);

-- Developer Tools 分类的自开发工具
UPDATE tools
SET 
  tool_type = 'self_developed',
  external_url = NULL
WHERE slug IN (
  'json-formatter',
  'base64-encoder',
  'url-encoder'
);

-- ============================================
-- 第三步：验证更新结果
-- ============================================
-- 查看所有自开发工具：
SELECT 
  tools.name, 
  tools.slug, 
  tools.tool_type,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
WHERE tools.tool_type = 'self_developed'
ORDER BY categories.name, tools.name;

-- 查看所有外部链接工具（应该只剩下 PDF to Word）：
SELECT 
  tools.name, 
  tools.slug, 
  tools.tool_type,
  tools.external_url,
  categories.name as category
FROM tools
LEFT JOIN categories ON tools.category_id = categories.id
WHERE tools.tool_type = 'external_link'
ORDER BY categories.name, tools.name;

-- 统计：
SELECT 
  tool_type,
  COUNT(*) as count
FROM tools
WHERE is_active = true
GROUP BY tool_type;

