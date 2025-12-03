-- 更新所有分类的工具数量
-- 在 Supabase SQL Editor 中运行此脚本

-- ============================================
-- 方法1：使用 UPDATE 语句更新 tool_count
-- ============================================

UPDATE categories
SET tool_count = (
  SELECT COUNT(*)
  FROM tools
  WHERE tools.category_id = categories.id
    AND tools.is_active = true
);

-- ============================================
-- 验证更新结果
-- ============================================

-- 查看所有分类及其工具数量
SELECT 
  c.id,
  c.name,
  c.slug,
  c.tool_count as stored_count,
  COUNT(t.id) as actual_count
FROM categories c
LEFT JOIN tools t ON t.category_id = c.id AND t.is_active = true
GROUP BY c.id, c.name, c.slug, c.tool_count
ORDER BY c.name;

-- ============================================
-- 方法2：创建触发器自动更新（可选）
-- ============================================

-- 创建函数：更新分类的工具数量
CREATE OR REPLACE FUNCTION update_category_tool_count()
RETURNS TRIGGER AS $$
BEGIN
  -- 更新旧分类的工具数量
  IF OLD.category_id IS NOT NULL THEN
    UPDATE categories
    SET tool_count = (
      SELECT COUNT(*)
      FROM tools
      WHERE tools.category_id = OLD.category_id
        AND tools.is_active = true
    )
    WHERE id = OLD.category_id;
  END IF;

  -- 更新新分类的工具数量
  IF NEW.category_id IS NOT NULL THEN
    UPDATE categories
    SET tool_count = (
      SELECT COUNT(*)
      FROM tools
      WHERE tools.category_id = NEW.category_id
        AND tools.is_active = true
    )
    WHERE id = NEW.category_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器：当工具被插入、更新或删除时，自动更新分类的工具数量
DROP TRIGGER IF EXISTS trigger_update_category_tool_count ON tools;
CREATE TRIGGER trigger_update_category_tool_count
  AFTER INSERT OR UPDATE OR DELETE ON tools
  FOR EACH ROW
  EXECUTE FUNCTION update_category_tool_count();

-- ============================================
-- 说明
-- ============================================
-- 方法1：手动更新（立即执行）
-- - 运行 UPDATE 语句即可更新所有分类的工具数量
-- - 适合一次性更新

-- 方法2：自动更新（推荐）
-- - 创建触发器后，每次工具被添加、更新或删除时，会自动更新分类的工具数量
-- - 适合长期维护

-- 建议：先运行方法1更新现有数据，然后运行方法2创建触发器，以后就自动更新了

