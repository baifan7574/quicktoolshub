import { supabase } from '@/lib/supabase'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import ArticleCard from '@/components/blog/ArticleCard'
import ToolCard from '@/components/tools/ToolCard'
import ReactMarkdown from 'react-markdown'
import { Article, Tool } from '@/types'
import { ClockIcon, ShareIcon } from '@heroicons/react/24/outline'
import ShareButtons from '@/components/blog/ShareButtons'

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { data: article } = await supabase
    .from('articles')
    .select('*')
    .eq('slug', slug)
    .eq('is_published', true)
    .single()

  if (!article) {
    return {
      title: 'Article Not Found - QuickToolsHub',
    }
  }

  return {
    title: `${article.title} - QuickToolsHub`,
    description: article.excerpt || article.title,
  }
}

export default async function ArticleDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params

  // 获取文章详情
  const { data: article } = await supabase
    .from('articles')
    .select('*')
    .eq('slug', slug)
    .eq('is_published', true)
    .single()

  if (!article) {
    notFound()
  }

  // 更新浏览次数
  await supabase
    .from('articles')
    .update({ view_count: (article.view_count || 0) + 1 })
    .eq('id', article.id)

  // 获取相关工具（通过tool_articles关联表）
  const { data: toolArticles } = await supabase
    .from('tool_articles')
    .select('tools(*, categories(name, slug))')
    .eq('article_id', article.id)
    .limit(6)

  // 获取相关文章（同分类的其他文章）
  const { data: relatedArticles } = await supabase
    .from('articles')
    .select('*')
    .eq('category', article.category)
    .eq('is_published', true)
    .neq('id', article.id)
    .order('view_count', { ascending: false })
    .limit(3)

  // 格式化日期
  const publishedDate = article.published_at
    ? new Date(article.published_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null

  return (
    <div className="bg-white min-h-screen">
      {/* 面包屑导航 */}
      <div className="bg-gray-50 border-b">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <nav className="flex items-center space-x-2 text-sm">
            <Link href="/" className="text-gray-500 hover:text-blue-600">
              Home
            </Link>
            <span className="text-gray-400">/</span>
            <Link href="/blog" className="text-gray-500 hover:text-blue-600">
              Blog
            </Link>
            {article.category && (
              <>
                <span className="text-gray-400">/</span>
                <Link
                  href={`/blog?category=${encodeURIComponent(article.category)}`}
                  className="text-gray-500 hover:text-blue-600"
                >
                  {article.category}
                </Link>
              </>
            )}
            <span className="text-gray-400">/</span>
            <span className="text-gray-900 line-clamp-1">{article.title}</span>
          </nav>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* 左侧主要内容（70%） */}
          <main className="flex-1 lg:w-2/3">
            {/* 文章标题和元信息 */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold mb-4">{article.title}</h1>

              {/* 文章元信息 */}
              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-6">
                {publishedDate && (
                  <span>Published on {publishedDate}</span>
                )}
                {article.reading_time && (
                  <div className="flex items-center space-x-1">
                    <ClockIcon className="h-4 w-4" />
                    <span>{article.reading_time} min read</span>
                  </div>
                )}
                {article.category && (
                  <Link
                    href={`/blog?category=${encodeURIComponent(article.category)}`}
                    className="bg-gray-100 px-3 py-1 rounded-full hover:bg-gray-200 transition-colors"
                  >
                    {article.category}
                  </Link>
                )}
                {article.view_count > 0 && (
                  <span>{article.view_count} views</span>
                )}
              </div>

              {/* 文章特色图片 */}
              {article.featured_image && (
                <div className="mb-8 rounded-lg overflow-hidden">
                  <img
                    src={article.featured_image}
                    alt={article.title}
                    className="w-full h-auto"
                  />
                </div>
              )}
            </div>

            {/* 广告位预留（上方） */}
            <div className="mb-8 bg-gray-100 rounded-lg p-8 text-center text-gray-400 border-2 border-dashed">
              <p>Advertisement Space</p>
              <p className="text-sm">(For Google AdSense or Ezoic)</p>
            </div>

            {/* 文章正文 */}
            <div className="prose prose-lg max-w-none mb-8">
              <ReactMarkdown>{article.content}</ReactMarkdown>
            </div>

            {/* 文章标签 */}
            {article.tags && article.tags.length > 0 && (
              <div className="mb-8">
                <div className="flex flex-wrap gap-2">
                  {article.tags.map((tag: string, index: number) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* 分享功能 */}
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="font-semibold mb-4 flex items-center space-x-2">
                <ShareIcon className="h-5 w-5" />
                <span>Share this article</span>
              </h3>
              <ShareButtons
                url={`${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/blog/${article.slug}`}
                title={article.title}
              />
            </div>

            {/* 广告位预留（下方） */}
            <div className="mb-8 bg-gray-100 rounded-lg p-8 text-center text-gray-400 border-2 border-dashed">
              <p>Advertisement Space</p>
              <p className="text-sm">(For Google AdSense or Ezoic)</p>
            </div>

            {/* 相关工具推荐 */}
            {toolArticles && toolArticles.length > 0 && (
              <section className="mb-8">
                <h2 className="text-2xl font-semibold mb-6">Related Tools</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {toolArticles.map((item: any) => (
                    item.tools && <ToolCard key={item.tools.id} tool={item.tools} />
                  ))}
                </div>
              </section>
            )}

            {/* 相关文章推荐 */}
            {relatedArticles && relatedArticles.length > 0 && (
              <section>
                <h2 className="text-2xl font-semibold mb-6">Related Articles</h2>
                <div className="space-y-4">
                  {relatedArticles.map((relatedArticle: Article) => (
                    <ArticleCard key={relatedArticle.id} article={relatedArticle} />
                  ))}
                </div>
              </section>
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

              {/* 相关文章推荐（侧边栏） */}
              {relatedArticles && relatedArticles.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h3 className="text-lg font-semibold mb-4">More Articles</h3>
                  <div className="space-y-4">
                    {relatedArticles.map((relatedArticle: Article) => (
                      <Link
                        key={relatedArticle.id}
                        href={`/blog/${relatedArticle.slug}`}
                        className="block hover:text-blue-600 transition-colors"
                      >
                        <h4 className="font-medium mb-1 line-clamp-2">{relatedArticle.title}</h4>
                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                          {relatedArticle.reading_time && (
                            <span>{relatedArticle.reading_time} min read</span>
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

