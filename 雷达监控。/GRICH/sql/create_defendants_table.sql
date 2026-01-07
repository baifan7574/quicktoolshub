-- ============================================
-- GRICH 引擎2: 被告人数据库表
-- ============================================
-- 用途: 存储从GBC律所抓取的被告人信息
-- 执行: 在 Supabase SQL Editor 中运行此脚本

-- 创建被告人表
CREATE TABLE IF NOT EXISTS defendants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    brand_name TEXT NOT NULL,
    case_number TEXT NOT NULL,
    defendant_name TEXT NOT NULL,
    defendant_email TEXT,
    platform TEXT,
    store_url TEXT,
    address TEXT,
    source TEXT DEFAULT 'GBC_Official',
    found_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(case_number, defendant_name)
);

-- 启用行级安全 (RLS)
ALTER TABLE defendants ENABLE ROW LEVEL SECURITY;

-- 创建策略: 允许公开读取 (用于SEO页面)
CREATE POLICY "Allow public read access" ON defendants
FOR SELECT USING (true);

-- 创建策略: 允许service role写入 (用于自动化脚本)
CREATE POLICY "Allow service role insert" ON defendants
FOR INSERT WITH CHECK (true);

-- 创建索引 (加速查询)
CREATE INDEX IF NOT EXISTS idx_defendants_name ON defendants(defendant_name);
CREATE INDEX IF NOT EXISTS idx_defendants_case ON defendants(case_number);
CREATE INDEX IF NOT EXISTS idx_defendants_brand ON defendants(brand_name);

-- 验证表创建
SELECT 
    'defendants' as table_name,
    COUNT(*) as row_count,
    pg_size_pretty(pg_total_relation_size('defendants')) as table_size
FROM defendants;
