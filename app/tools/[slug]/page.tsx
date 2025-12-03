import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import ArticleCard from '@/components/blog/ArticleCard'
import ToolCard from '@/components/tools/ToolCard'
import ToolRenderer from '@/components/tools/ToolRenderer'

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { data: tool } = await supabase
    .from('tools')
    .select('*, categories(name, slug)')
    .eq('slug', slug)
    .eq('is_active', true)
    .single()

  if (!tool) {
    return {
      title: 'Tool Not Found - QuickToolsHub',
    }
  }

  return {
    title: `${tool.name} - QuickToolsHub`,
    description: tool.short_description || tool.description || `Use ${tool.name} for free online`,
  }
}

export default async function ToolDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // 获取工具详情
  const { data: tool } = await supabase
    .from('tools')
    .select('*, categories(name, slug)')
    .eq('slug', slug)
    .eq('is_active', true)
    .single()

  if (!tool) {
    notFound()
  }

  // 更新浏览次数
  await supabase
    .from('tools')
    .update({ view_count: (tool.view_count || 0) + 1 })
    .eq('id', tool.id)

  // 获取相关文章
  const { data: relatedArticles } = await supabase
    .from('tool_articles')
    .select('articles(*)')
    .eq('tool_id', tool.id)
    .limit(3)

  // 获取同分类的其他工具
  const { data: relatedTools } = await supabase
    .from('tools')
    .select('*, categories(name, slug)')
    .eq('category_id', tool.category_id)
    .eq('is_active', true)
    .neq('id', tool.id)
    .limit(6)

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
            <Link href="/tools" className="text-gray-500 hover:text-blue-600">
              Tools
            </Link>
            {tool.categories && (
              <>
                <span className="text-gray-400">/</span>
                <Link
                  href={`/categories/${tool.categories.slug}`}
                  className="text-gray-500 hover:text-blue-600"
                >
                  {tool.categories.name}
                </Link>
              </>
            )}
            <span className="text-gray-400">/</span>
            <span className="text-gray-900">{tool.name}</span>
          </nav>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* 左侧主要内容（70%） */}
          <main className="flex-1 lg:w-2/3">
            {/* 工具标题和信息 */}
            <div className="mb-8">
              <div className="flex items-start space-x-4 mb-4">
                <div className="flex-shrink-0 w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                  {tool.icon_url ? (
                    <img src={tool.icon_url} alt={tool.name} className="w-12 h-12" />
                  ) : (
                    <span className="text-3xl">🔧</span>
                  )}
                </div>
                <div className="flex-1">
                  <h1 className="text-4xl font-bold mb-2">{tool.name}</h1>
                  <div className="flex items-center space-x-2 flex-wrap mb-4">
                    <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                      Free
                    </span>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                      Online
                    </span>
                    {tool.tool_type === 'self_developed' && (
                      <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
                        Built-in
                      </span>
                    )}
                    {tool.tool_type === 'external_link' && (
                      <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-semibold">
                        External Link
                      </span>
                    )}
                    {tool.categories && (
                      <Link
                        href={`/categories/${tool.categories.slug}`}
                        className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-semibold hover:bg-gray-200"
                      >
                        {tool.categories.name}
                      </Link>
                    )}
                  </div>
                </div>
              </div>

              {tool.description && (
                <p className="text-lg text-gray-700 mb-4">{tool.description}</p>
              )}
            </div>

            {/* 广告位预留（上方） */}
            <div className="mb-8 bg-gray-100 rounded-lg p-8 text-center text-gray-400 border-2 border-dashed">
              <p>Advertisement Space</p>
              <p className="text-sm">(For Google AdSense or Ezoic)</p>
            </div>

            {/* 工具功能区域 */}
            <div className="bg-gray-50 rounded-lg p-8 mb-8">
              <ToolRenderer tool={tool} />
            </div>

            {/* 广告位预留（下方） */}
            <div className="mb-8 bg-gray-100 rounded-lg p-8 text-center text-gray-400 border-2 border-dashed">
              <p>Advertisement Space</p>
              <p className="text-sm">(For Google AdSense or Ezoic)</p>
            </div>

            {/* 相关文章 */}
            {relatedArticles && relatedArticles.length > 0 && (
              <section className="mb-8">
                <h2 className="text-2xl font-semibold mb-6">Related Articles</h2>
                <div className="space-y-4">
                  {relatedArticles.map((item: any) => (
                    item.articles && (
                      <ArticleCard key={item.articles.id} article={item.articles} />
                    )
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

              {/* 相关工具推荐 */}
              {relatedTools && relatedTools.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h3 className="text-lg font-semibold mb-4">Related Tools</h3>
                  <div className="space-y-4">
                    {relatedTools.map((relatedTool: any) => (
                      <ToolCard key={relatedTool.id} tool={relatedTool} />
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

