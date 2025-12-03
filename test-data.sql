-- 测试数据插入脚本（自动获取分类ID版本）
-- 在Supabase SQL Editor中运行此脚本
-- 这个脚本会自动根据分类slug获取category_id，无需手动修改

-- ============================================
-- 第一步：先查询分类ID（用于验证）
-- ============================================
-- 运行这个查询来查看所有分类及其ID：
SELECT id, name, slug FROM categories ORDER BY id;

-- ============================================
-- 第二步：插入测试工具数据（自动获取分类ID）
-- ============================================

-- PDF Tools 分类的工具（自动获取category_id）
INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'PDF Merger', 
  'pdf-merger', 
  'Merge multiple PDF files into one document', 
  'Combine multiple PDF files into a single document quickly and easily. No registration required, completely free to use.', 
  (SELECT id FROM categories WHERE slug = 'pdf-tools'), 
  'self_developed', 
  true, 
  150, 
  45, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'pdf-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'PDF Splitter', 
  'pdf-splitter', 
  'Split PDF files into separate pages', 
  'Extract pages from your PDF files. Split by page range or extract specific pages.', 
  (SELECT id FROM categories WHERE slug = 'pdf-tools'), 
  'self_developed', 
  true, 
  120, 
  30, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'pdf-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'PDF Compressor', 
  'pdf-compressor', 
  'Reduce PDF file size without losing quality', 
  'Compress large PDF files to reduce their size while maintaining quality. Perfect for email attachments.', 
  (SELECT id FROM categories WHERE slug = 'pdf-tools'), 
  'external_link', 
  true, 
  200, 
  60, 
  NULL, 
  'https://www.ilovepdf.com/compress-pdf'
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'pdf-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'PDF to Word', 
  'pdf-to-word', 
  'Convert PDF files to editable Word documents', 
  'Transform your PDF files into editable Word documents. Preserve formatting and layout.', 
  (SELECT id FROM categories WHERE slug = 'pdf-tools'), 
  'external_link', 
  true, 
  180, 
  50, 
  NULL, 
  'https://www.ilovepdf.com/pdf-to-word'
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'pdf-tools')
ON CONFLICT (slug) DO NOTHING;

-- Image Tools 分类的工具（自动获取category_id）
INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Image Compressor', 
  'image-compressor', 
  'Compress images to reduce file size', 
  'Reduce image file size without significant quality loss. Support JPG, PNG, and other formats.', 
  (SELECT id FROM categories WHERE slug = 'image-tools'), 
  'self_developed', 
  true, 
  300, 
  100, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'image-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Image Resizer', 
  'image-resizer', 
  'Resize images to any dimensions', 
  'Resize your images to any size. Maintain aspect ratio or set custom dimensions.', 
  (SELECT id FROM categories WHERE slug = 'image-tools'), 
  'self_developed', 
  true, 
  250, 
  80, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'image-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Image Converter', 
  'image-converter', 
  'Convert images between different formats', 
  'Convert images between JPG, PNG, GIF, WebP, and other formats. Fast and free.', 
  (SELECT id FROM categories WHERE slug = 'image-tools'), 
  'external_link', 
  true, 
  220, 
  70, 
  NULL, 
  'https://www.iloveimg.com/convert-image'
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'image-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Background Remover', 
  'background-remover', 
  'Remove image backgrounds automatically', 
  'Remove backgrounds from images with AI-powered technology. Perfect for product photos.', 
  (SELECT id FROM categories WHERE slug = 'image-tools'), 
  'external_link', 
  true, 
  400, 
  150, 
  NULL, 
  'https://www.remove.bg/'
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'image-tools')
ON CONFLICT (slug) DO NOTHING;

-- Text Tools 分类的工具（自动获取category_id）
INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Word Counter', 
  'word-counter', 
  'Count words, characters, and paragraphs', 
  'Count words, characters, paragraphs, and sentences in your text. Perfect for writers and students.', 
  (SELECT id FROM categories WHERE slug = 'text-tools'), 
  'self_developed', 
  true, 
  500, 
  200, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'text-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Text Case Converter', 
  'text-case-converter', 
  'Convert text between different cases', 
  'Convert text to uppercase, lowercase, title case, sentence case, and more.', 
  (SELECT id FROM categories WHERE slug = 'text-tools'), 
  'self_developed', 
  true, 
  180, 
  60, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'text-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Lorem Ipsum Generator', 
  'lorem-ipsum-generator', 
  'Generate placeholder text', 
  'Generate Lorem Ipsum placeholder text for your designs and layouts.', 
  (SELECT id FROM categories WHERE slug = 'text-tools'), 
  'self_developed', 
  true, 
  150, 
  50, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'text-tools')
ON CONFLICT (slug) DO NOTHING;

-- Developer Tools 分类的工具（自动获取category_id）
INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'JSON Formatter', 
  'json-formatter', 
  'Format and validate JSON data', 
  'Format, validate, and beautify JSON data. Perfect for developers and API testing.', 
  (SELECT id FROM categories WHERE slug = 'developer-tools'), 
  'self_developed', 
  true, 
  350, 
  120, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'developer-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'Base64 Encoder', 
  'base64-encoder', 
  'Encode and decode Base64 strings', 
  'Encode text to Base64 or decode Base64 to text. Fast and secure.', 
  (SELECT id FROM categories WHERE slug = 'developer-tools'), 
  'self_developed', 
  true, 
  200, 
  70, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'developer-tools')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO tools (name, slug, short_description, description, category_id, tool_type, is_active, view_count, use_count, icon_url, external_url)
SELECT 
  'URL Encoder', 
  'url-encoder', 
  'Encode and decode URL strings', 
  'Encode special characters in URLs or decode URL-encoded strings.', 
  (SELECT id FROM categories WHERE slug = 'developer-tools'), 
  'self_developed', 
  true, 
  160, 
  55, 
  NULL, 
  NULL
WHERE EXISTS (SELECT 1 FROM categories WHERE slug = 'developer-tools')
ON CONFLICT (slug) DO NOTHING;

-- ============================================
-- 第三步：验证数据已插入
-- ============================================
-- 运行这个查询来查看插入的工具：
SELECT t.id, t.name, t.slug, c.name as category_name 
FROM tools t 
LEFT JOIN categories c ON t.category_id = c.id 
ORDER BY c.name, t.name;

-- 统计每个分类的工具数量：
SELECT c.name, COUNT(t.id) as tool_count 
FROM categories c 
LEFT JOIN tools t ON c.id = t.category_id 
GROUP BY c.id, c.name 
ORDER BY c.name;
