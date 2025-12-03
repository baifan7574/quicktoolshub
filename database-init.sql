-- QuickToolsHub 数据库初始化脚本
-- 在Supabase SQL Editor中执行此脚本

-- ============================================
-- 1. 创建分类表（categories）
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  icon_url VARCHAR(500),
  tool_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

-- ============================================
-- 2. 创建工具表（tools）
-- ============================================
CREATE TABLE IF NOT EXISTS tools (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  short_description VARCHAR(500),
  category_id INTEGER REFERENCES categories(id),
  tool_type VARCHAR(50) DEFAULT 'external_link', -- 'self_developed' or 'external_link'
  external_url VARCHAR(500), -- 如果是外部链接
  icon_url VARCHAR(500),
  screenshot_url VARCHAR(500),
  tags TEXT[], -- 标签数组
  is_featured BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  view_count INTEGER DEFAULT 0,
  use_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_tools_slug ON tools(slug);
CREATE INDEX IF NOT EXISTS idx_tools_category_id ON tools(category_id);
CREATE INDEX IF NOT EXISTS idx_tools_is_featured ON tools(is_featured);
CREATE INDEX IF NOT EXISTS idx_tools_is_active ON tools(is_active);
CREATE INDEX IF NOT EXISTS idx_tools_view_count ON tools(view_count DESC);

-- ============================================
-- 3. 创建文章表（articles）
-- ============================================
CREATE TABLE IF NOT EXISTS articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  excerpt TEXT,
  content TEXT NOT NULL, -- Markdown格式
  category VARCHAR(100),
  tags TEXT[],
  featured_image VARCHAR(500),
  reading_time INTEGER, -- 阅读时长（分钟）
  view_count INTEGER DEFAULT 0,
  is_published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_articles_slug ON articles(slug);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_is_published ON articles(is_published);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_view_count ON articles(view_count DESC);

-- ============================================
-- 4. 创建工具-文章关联表（tool_articles）
-- ============================================
CREATE TABLE IF NOT EXISTS tool_articles (
  id SERIAL PRIMARY KEY,
  tool_id INTEGER REFERENCES tools(id) ON DELETE CASCADE,
  article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
  relation_type VARCHAR(50) DEFAULT 'tutorial', -- 'tutorial', 'comparison', 'guide'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(tool_id, article_id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_tool_articles_tool_id ON tool_articles(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_articles_article_id ON tool_articles(article_id);

-- ============================================
-- 5. 创建搜索记录表（search_logs，可选）
-- ============================================
CREATE TABLE IF NOT EXISTS search_logs (
  id SERIAL PRIMARY KEY,
  query VARCHAR(255) NOT NULL,
  result_count INTEGER,
  user_ip VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_search_logs_created_at ON search_logs(created_at DESC);

-- ============================================
-- 6. 创建更新时间触发器函数
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为categories表添加触发器
DROP TRIGGER IF EXISTS update_categories_updated_at ON categories;
CREATE TRIGGER update_categories_updated_at 
  BEFORE UPDATE ON categories
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 为tools表添加触发器
DROP TRIGGER IF EXISTS update_tools_updated_at ON tools;
CREATE TRIGGER update_tools_updated_at 
  BEFORE UPDATE ON tools
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 为articles表添加触发器
DROP TRIGGER IF EXISTS update_articles_updated_at ON articles;
CREATE TRIGGER update_articles_updated_at 
  BEFORE UPDATE ON articles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 7. 插入初始分类数据
-- ============================================
INSERT INTO categories (name, slug, description, icon_url) VALUES
('PDF Tools', 'pdf-tools', 'Free online PDF tools for merging, splitting, converting and more', '/icons/pdf.svg'),
('Image Tools', 'image-tools', 'Free online image tools for compression, conversion, editing and more', '/icons/image.svg'),
('Text Tools', 'text-tools', 'Free online text tools for counting, formatting, converting and more', '/icons/text.svg'),
('Developer Tools', 'developer-tools', 'Free online developer tools for coding, formatting, testing and more', '/icons/developer.svg'),
('Converter Tools', 'converter-tools', 'Free online converter tools for various file formats', '/icons/converter.svg'),
('Generator Tools', 'generator-tools', 'Free online generator tools for passwords, QR codes, and more', '/icons/generator.svg')
ON CONFLICT (slug) DO NOTHING;

-- ============================================
-- 完成！
-- ============================================
-- 所有表已创建完成
-- 初始分类数据已插入
-- 可以开始使用数据库了

