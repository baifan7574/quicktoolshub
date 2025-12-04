'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import ReactMarkdown from 'react-markdown'

// 文章分类列表
const articleCategories = [
  'PDF Tools Guides',
  'Image Tools Guides',
  'Text Tools Guides',
  'Developer Tools Guides',
  'Tool Comparisons',
  'Best Practices',
]

// 长尾关键词建议（根据分类）
const keywordSuggestions: Record<string, string[]> = {
  'PDF Tools Guides': [
    'how to merge PDF files online free',
    'best free PDF merger tool',
    'merge PDF files without watermark',
    'how to compress PDF file size',
    'free PDF to Word converter online',
  ],
  'Image Tools Guides': [
    'how to compress image for email',
    'resize image online free',
    'convert image to different format',
    'remove background from image free',
    'optimize image for web',
  ],
  'Text Tools Guides': [
    'count words in text online',
    'convert text to uppercase',
    'format JSON online',
    'encode decode text online',
  ],
  'Developer Tools Guides': [
    'format JSON online free',
    'base64 encode decode online',
    'URL encoder decoder tool',
  ],
  'Tool Comparisons': [
    'best free PDF tools compared',
    'free vs paid image tools',
    'top 10 online tools 2024',
  ],
  'Best Practices': [
    'how to optimize PDF files',
    'image optimization best practices',
    'PDF tools for students',
  ],
}

export default function NewArticlePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    category: '',
    tags: '',
    featured_image: '',
    is_published: false,
  })

  // 自动生成 slug
  const generateSlug = (title: string) => {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '')
  }

  // 计算阅读时长
  const calculateReadingTime = (content: string) => {
    const words = content.split(/\s+/).length
    return Math.ceil(words / 200) // 假设每分钟阅读 200 字
  }

  // 处理标题变化
  const handleTitleChange = (title: string) => {
    setFormData({
      ...formData,
      title,
      slug: generateSlug(title),
    })
  }

  // 处理分类变化（显示关键词建议）
  const handleCategoryChange = (category: string) => {
    setFormData({ ...formData, category })
  }

  // 提交文章
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const readingTime = calculateReadingTime(formData.content)
      const tags = formData.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0)

      const articleData = {
        ...formData,
        tags,
        reading_time: readingTime,
        published_at: formData.is_published ? new Date().toISOString() : null,
      }

      const response = await fetch('/api/admin/articles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(articleData),
      })

      if (response.ok) {
        router.push('/admin/blog')
      } else {
        const error = await response.json()
        alert(error.error || '创建文章失败')
      }
    } catch (error) {
      console.error('Failed to create article:', error)
      alert('创建文章失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">新建文章</h1>
          <p className="mt-2 text-gray-600">创建包含长尾关键词的 SEO 优化文章</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 标题 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标题 <span className="text-red-500">*</span>
              <span className="text-gray-500 text-xs ml-2">
                (包含长尾关键词，例如："How to Merge PDF Files Online Free")
              </span>
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => handleTitleChange(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              placeholder="例如：How to Merge PDF Files Online Free - Complete Guide"
            />
            <p className="mt-1 text-xs text-gray-500">
              💡 SEO 提示：标题应该包含用户搜索的长尾关键词
            </p>
          </div>

          {/* Slug */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              URL Slug <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              required
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              placeholder="how-to-merge-pdf-files-online-free"
            />
            <p className="mt-1 text-xs text-gray-500">
              URL 友好格式，自动从标题生成
            </p>
          </div>

          {/* 分类 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分类 <span className="text-red-500">*</span>
            </label>
            <select
              required
              value={formData.category}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
            >
              <option value="">选择分类</option>
              {articleCategories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
            
            {/* 关键词建议 */}
            {formData.category && keywordSuggestions[formData.category] && (
              <div className="mt-2 p-3 bg-blue-50 rounded-lg">
                <p className="text-xs font-medium text-blue-900 mb-2">
                  💡 长尾关键词建议（用于标题和内容）：
                </p>
                <ul className="text-xs text-blue-700 space-y-1">
                  {keywordSuggestions[formData.category].map((keyword, index) => (
                    <li key={index}>• {keyword}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* 摘要 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              摘要 <span className="text-red-500">*</span>
              <span className="text-gray-500 text-xs ml-2">
                (150-200 字，包含关键词，用于 SEO 和文章预览)
              </span>
            </label>
            <textarea
              required
              value={formData.excerpt}
              onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
              rows={3}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px] touch-manipulation"
              placeholder="文章摘要，包含主要关键词，用于 SEO 和文章列表预览..."
            />
            <p className="mt-1 text-xs text-gray-500">
              当前字数: {formData.excerpt.length} / 200（建议 150-200 字）
            </p>
          </div>

          {/* 标签 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标签
              <span className="text-gray-500 text-xs ml-2">
                (用逗号分隔，例如：pdf, merge, tutorial, free)
              </span>
            </label>
            <input
              type="text"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              placeholder="pdf, merge, tutorial, free, online"
            />
          </div>

          {/* 特色图片 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              特色图片 URL
            </label>
            <input
              type="url"
              value={formData.featured_image}
              onChange={(e) => setFormData({ ...formData, featured_image: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              placeholder="https://example.com/image.jpg"
            />
          </div>

          {/* 内容编辑 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              内容 <span className="text-red-500">*</span>
              <span className="text-gray-500 text-xs ml-2">
                (Markdown 格式，1000-2000 字，自然使用长尾关键词)
              </span>
            </label>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* 编辑区域 */}
              <div>
                <textarea
                  required
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  rows={20}
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 touch-manipulation"
                  placeholder={`使用 Markdown 格式编写文章内容...

💡 SEO 提示：
- 在标题中使用长尾关键词（例如：## How to Merge PDF Files Online Free）
- 在内容中自然使用关键词（不要堆砌）
- 添加内部链接到相关工具页面（例如：[PDF合并工具](/tools/pdf-merger)）
- 使用 H2、H3 标题组织内容
- 添加相关图片（使用 ![alt text](image-url)）

Markdown 语法：
# 一级标题
## 二级标题
**粗体** *斜体*
[链接文本](URL)
![图片alt](图片URL)
- 列表项
1. 有序列表`}
                />
                <p className="mt-2 text-xs text-gray-500">
                  当前字数: {formData.content.split(/\s+/).length} 字（建议 1000-2000 字）
                </p>
              </div>
              {/* 预览区域 */}
              <div>
                <div className="border border-gray-300 rounded-lg px-4 py-3 bg-white min-h-[500px] max-h-[600px] overflow-y-auto">
                  <div className="prose prose-sm max-w-none">
                    {formData.content ? (
                      <ReactMarkdown>{formData.content}</ReactMarkdown>
                    ) : (
                      <p className="text-gray-400">预览将显示在这里...</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 发布选项 */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_published"
              checked={formData.is_published}
              onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="is_published" className="ml-2 text-sm text-gray-700">
              立即发布（发布后文章会出现在博客页面，可以被搜索引擎索引）
            </label>
          </div>

          {/* 提交按钮 */}
          <div className="flex items-center gap-4">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 min-h-[44px] touch-manipulation"
            >
              {loading ? '保存中...' : formData.is_published ? '发布文章' : '保存草稿'}
            </button>
            <Link
              href="/admin/blog"
              className="bg-gray-200 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors min-h-[44px] touch-manipulation"
            >
              取消
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}

