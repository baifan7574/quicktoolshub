import { supabase } from '@/lib/supabase'
import ArticleCard from '@/components/blog/ArticleCard'
import ArticleSortSelect from '@/components/blog/ArticleSortSelect'
import Link from 'next/link'
import { Article } from '@/types'

export const metadata = {
  title: 'Blog - QuickToolsHub',
  description: 'Read articles about tools, tutorials, and best practices',
}

interface SearchParams {
  category?: string
  sort?: string
  page?: string
}

// 文章分类列表
const articleCategories = [
  { value: 'all', label: 'All Articles' },
  { value: 'PDF Tools Guides', label: 'PDF Tools Guides' },
  { value: 'Image Tools Guides', label: 'Image Tools Guides' },
  { value: 'Text Tools Guides', label: 'Text Tools Guides' },
  { value: 'Developer Tools Guides', label: 'Developer Tools Guides' },
  { value: 'Tool Comparisons', label: 'Tool Comparisons' },
  { value: 'Best Practices', label: 'Best Practices' },
]

export default async function BlogPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>
}) {
  const params = await searchParams
  const category = params.category || 'all'
  const sort = params.sort || 'latest'
  const page = parseInt(params.page || '1')
  const limit = 10
  const offset = (page - 1) * limit

  // 构建查询
  let query = supabase
    .from('articles')
    .select('*', { count: 'exact' })
    .eq('is_published', true)

  // 分类筛选
  if (category && category !== 'all') {
    query = query.eq('category', category)
  }

  // 排序
  switch (sort) {
    case 'popular':
      query = query.order('view_count', { ascending: false })
      break
    case 'viewed':
      query = query.order('view_count', { ascending: false })
      break
    default: // latest
      query = query.order('published_at', { ascending: false })
  }

  // 分页
  query = query.range(offset, offset + limit - 1)

  const { data: articles, count } = await query

  const totalPages = count ? Math.ceil(count / limit) : 1

  // 获取热门文章（用于右侧栏）
  const { data: popularArticles } = await supabase
    .from('articles')
    .select('*')
    .eq('is_published', true)
    .order('view_count', { ascending: false })
    .limit(5)

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* 页面标题 */}
        <div className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-2">Blog</h1>
          <p className="text-sm sm:text-base text-gray-600">Articles, tutorials, and guides about our tools</p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* 左侧主要内容（70%） */}
          <main className="flex-1 lg:w-2/3">
            {/* 分类筛选和排序 */}
            <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6 mb-4 sm:mb-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
                {/* 分类筛选 */}
                <div className="flex flex-wrap gap-2">
                  {articleCategories.map((cat: any) => (
                    <Link
                      key={cat.value}
                      href={`/blog${cat.value === 'all' ? '' : `?category=${encodeURIComponent(cat.value)}`}`}
                      className={`px-3 sm:px-4 py-2.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors min-h-[36px] sm:min-h-[44px] flex items-center justify-center touch-manipulation ${
                        category === cat.value
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {cat.label}
                    </Link>
                  ))}
                </div>

                {/* 排序 */}
                <ArticleSortSelect currentSort={sort} category={category} />
              </div>
            </div>

            {/* 文章列表 */}
            {articles && articles.length > 0 ? (
              <>
                <div className="space-y-6 mb-8">
                  {articles.map((article: Article) => (
                    <ArticleCard key={article.id} article={article} />
                  ))}
                </div>

                {/* 分页 */}
                {totalPages > 1 && (
                  <div className="flex flex-col sm:flex-row justify-center items-center gap-3 sm:gap-2">
                    {page > 1 && (
                      <Link
                        href={`/blog?${new URLSearchParams({
                          ...(category !== 'all' && { category }),
                          ...(sort && { sort }),
                          page: (page - 1).toString(),
                        }).toString()}`}
                        className="px-4 py-2.5 sm:py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors text-sm sm:text-base min-h-[44px] flex items-center justify-center touch-manipulation"
                      >
                        Previous
                      </Link>
                    )}
                    <span className="px-4 py-2 text-gray-600 text-sm sm:text-base">
                      Page {page} of {totalPages}
                    </span>
                    {page < totalPages && (
                      <Link
                        href={`/blog?${new URLSearchParams({
                          ...(category !== 'all' && { category }),
                          ...(sort && { sort }),
                          page: (page + 1).toString(),
                        }).toString()}`}
                        className="px-4 py-2.5 sm:py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors text-sm sm:text-base min-h-[44px] flex items-center justify-center touch-manipulation"
                      >
                        Next
                      </Link>
                    )}
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-sm p-12 text-center">
                <p className="text-gray-500 text-lg mb-4">No articles found</p>
                <p className="text-gray-400">
                  {category !== 'all'
                    ? 'This category does not have any articles yet.'
                    : 'No articles available yet. Check back soon!'}
                </p>
              </div>
            )}
          </main>

          {/* 右侧栏（30%） */}
          <aside className="lg:w-1/3">
            <div className="space-y-6">
              {/* 广告位预留 */}
              <div className="bg-gray-100 rounded-lg p-8 text-center text-gray-400 border-2 border-dashed">
                <p>Advertisement Space</p>
                <p className="text-sm">(Sidebar Ad)</p>
              </div>

              {/* 热门文章 */}
              {popularArticles && popularArticles.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6">
                  <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Popular Articles</h3>
                  <div className="space-y-3 sm:space-y-4">
                    {popularArticles.map((article: Article) => (
                      <Link
                        key={article.id}
                        href={`/blog/${article.slug}`}
                        className="block hover:text-blue-600 transition-colors min-h-[44px] touch-manipulation"
                      >
                        <h4 className="font-medium mb-1 line-clamp-2 text-sm sm:text-base">{article.title}</h4>
                        <div className="flex items-center space-x-2 text-xs sm:text-sm text-gray-500">
                          {article.reading_time && (
                            <span>{article.reading_time} min read</span>
                          )}
                          {article.view_count > 0 && (
                            <span>• {article.view_count} views</span>
                          )}
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}

