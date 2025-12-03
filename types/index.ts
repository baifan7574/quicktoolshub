// 分类类型
export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
  icon_url: string | null
  tool_count: number
  created_at: string
  updated_at: string
}

// 工具类型
export interface Tool {
  id: number
  name: string
  slug: string
  description: string | null
  short_description: string | null
  category_id: number | null
  tool_type: 'self_developed' | 'external_link'
  external_url: string | null
  icon_url: string | null
  screenshot_url: string | null
  tags: string[]
  is_featured: boolean
  is_active: boolean
  view_count: number
  use_count: number
  created_at: string
  updated_at: string
  category?: Category
}

// 文章类型
export interface Article {
  id: number
  title: string
  slug: string
  excerpt: string | null
  content: string
  category: string | null
  tags: string[]
  featured_image: string | null
  reading_time: number | null
  view_count: number
  is_published: boolean
  published_at: string | null
  created_at: string
  updated_at: string
}

// 工具-文章关联类型
export interface ToolArticle {
  id: number
  tool_id: number
  article_id: number
  relation_type: 'tutorial' | 'comparison' | 'guide'
  created_at: string
  tool?: Tool
  article?: Article
}

