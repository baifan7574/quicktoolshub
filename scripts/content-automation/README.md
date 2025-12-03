# 自动化内容营销脚本

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `config/env.example` 为 `.env` 并填写：

```bash
cp config/env.example .env
# 编辑 .env 文件
```

**必需配置**：
- `SUPABASE_URL` - Supabase项目URL
- `SUPABASE_SERVICE_KEY` - Supabase服务密钥
- `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY` - AI API密钥

### 3. 准备关键词数据

你的关键词脚本应该输出CSV或JSON格式：

**CSV格式**：
```csv
keyword,search_volume,competition,cpc,trend
"how to merge PDF files",3000,medium,0.5,up
"best PDF merger",2000,low,0.3,stable
```

**JSON格式**：
```json
[
  {
    "keyword": "how to merge PDF files",
    "search_volume": 3000,
    "competition": "medium",
    "cpc": 0.5,
    "trend": "up"
  }
]
```

### 4. 运行脚本

#### 方式1：完整流程（推荐）

```bash
# 从关键词到发布，一步完成
python batch-processor.py ../data/keywords-raw.csv --max 50 --publish
```

#### 方式2：分步执行

```bash
# 步骤1: 处理关键词
python keyword-processor.py ../data/keywords-raw.csv ../data/keywords-processed.json

# 步骤2: 生成文章（测试5篇）
python article-generator.py ../data/keywords-processed.json ../data/articles-generated/

# 步骤3: 发布文章
python content-publisher.py ../data/articles-generated/ --schedule
```

---

## 📋 脚本说明

### `keyword-processor.py` - 关键词处理器

**功能**：
- 筛选有效关键词（搜索量、竞争度）
- 分类关键词（文章类型、目标工具）
- 计算优先级

**用法**：
```bash
python keyword-processor.py <输入文件> [输出文件]
```

**示例**：
```bash
python keyword-processor.py ../data/keywords-raw.csv ../data/keywords-processed.json
```

---

### `article-generator.py` - 文章生成器

**功能**：
- 使用AI生成文章大纲
- 生成完整文章内容
- 自动SEO优化

**用法**：
```bash
python article-generator.py <关键词JSON> [输出目录]
```

**示例**：
```bash
python article-generator.py ../data/keywords-processed.json ../data/articles-generated/
```

---

### `content-publisher.py` - 内容发布器

**功能**：
- 发布文章到Supabase
- 自动关联工具
- 定时发布

**用法**：
```bash
python content-publisher.py <文章目录> [选项]
```

**选项**：
- `--publish-now` - 立即发布（前2篇）
- `--schedule` - 定时发布（每天2篇）

**示例**：
```bash
# 立即发布
python content-publisher.py ../data/articles-generated/ --publish-now

# 定时发布（推荐）
python content-publisher.py ../data/articles-generated/ --schedule
```

---

### `batch-processor.py` - 批量处理器

**功能**：
- 完整自动化流程
- 从关键词到发布
- 批量处理

**用法**：
```bash
python batch-processor.py <关键词文件> [选项]
```

**选项**：
- `--max <数量>` - 最大生成文章数
- `--publish` - 自动发布
- `--output <目录>` - 输出目录

**示例**：
```bash
# 生成50篇文章并自动发布
python batch-processor.py ../data/keywords-raw.csv --max 50 --publish
```

---

## ⚡ 快速变现策略

### 第一周：快速填充

```bash
# 1. 用你的脚本拉取100个关键词
# 2. 生成50篇文章
python batch-processor.py keywords.csv --max 50 --publish

# 结果：50篇文章，每天发布2篇，25天完成
```

### 持续自动化

```bash
# 每天运行一次
python batch-processor.py new-keywords.csv --max 5 --publish

# 结果：每天新增2-3篇文章
```

---

## 📊 工作流程

```
你的关键词脚本
  ↓
keywords-raw.csv
  ↓
keyword-processor.py (筛选、分类)
  ↓
keywords-processed.json
  ↓
article-generator.py (AI生成)
  ↓
articles-generated/*.json
  ↓
content-publisher.py (发布到数据库)
  ↓
Supabase数据库
  ↓
网站自动显示
```

---

## 🔧 自定义配置

### 修改文章长度

编辑 `.env`：
```env
DEFAULT_ARTICLE_LENGTH=2000  # 改为2000字
```

### 修改每天发布数量

编辑 `.env`：
```env
DEFAULT_ARTICLES_PER_DAY=3  # 改为每天3篇
```

### 修改关键词筛选规则

编辑 `.env`：
```env
MIN_SEARCH_VOLUME=200      # 最小搜索量
MAX_SEARCH_VOLUME=10000     # 最大搜索量
MAX_COMPETITION=medium      # 最大竞争度
```

---

## 🐛 常见问题

### 1. API限流

**解决**：脚本已内置延迟，如仍有限流，增加 `time.sleep()` 时间

### 2. 文章质量

**解决**：调整AI模型（使用 `gpt-4` 或 `claude-3-opus`），或手动审核后发布

### 3. 数据库连接失败

**解决**：检查 `.env` 中的 Supabase 配置

---

## 📈 效率对比

**手动方式**：3-4小时/篇
**自动化方式**：8分钟/篇

**效率提升：20-30倍**

---

## 🎯 下一步

1. ✅ 配置环境变量
2. ✅ 测试生成5-10篇文章
3. ✅ 批量生成50-100篇
4. ✅ 监控流量和排名
5. ✅ 优化和调整

---

## 💡 提示

- 先小批量测试（5-10篇）
- 检查生成的文章质量
- 调整参数后再批量运行
- 定期检查关键词排名
- 优化表现好的文章

