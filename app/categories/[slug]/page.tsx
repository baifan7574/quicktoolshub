import { supabase } from '@/lib/supabase'
import { notFound } from 'next/navigation'
import ToolCard from '@/components/tools/ToolCard'
import ArticleCard from '@/components/blog/ArticleCard'
import Link from 'next/link'
import CategoryIcon from '@/components/categories/CategoryIcon'

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { data: category } = await supabase
    .from('categories')
    .select('*')
    .eq('slug', slug)
    .single()

  if (!category) {
    return {
      title: 'Category Not Found - QuickToolsHub',
    }
  }

  return {
    title: `${category.name} - QuickToolsHub`,
    description: category.description || `Browse ${category.name} on QuickToolsHub`,
  }
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // 获取分类信息
  const { data: category } = await supabase
    .from('categories')
    .select('*')
    .eq('slug', slug)
    .single()

  if (!category) {
    notFound()
  }

  // 获取该分类下的工具
  const { data: tools } = await supabase
    .from('tools')
    .select('*, categories(name, slug)')
    .eq('category_id', category.id)
    .eq('is_active', true)
    .order('view_count', { ascending: false })
    .limit(20)

  // 获取该分类下的相关文章
  const { data: articles } = await supabase
    .from('articles')
    .select('*')
    .eq('category', category.name)
    .eq('is_published', true)
    .order('published_at', { ascending: false })
    .limit(5)

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* 分类标题和描述 */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center shadow-sm">
              <CategoryIcon slug={category.slug} name={category.name} size="lg" />
            </div>
            <div>
              <h1 className="text-4xl font-bold mb-2">{category.name}</h1>
              {category.description && (
                <p className="text-lg text-gray-600">{category.description}</p>
              )}
            </div>
          </div>
          <div className="mt-4 text-gray-500">
            {category.tool_count} tools available
          </div>
        </div>

        {/* 工具列表 */}
        {tools && tools.length > 0 ? (
          <section className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold">Tools in this Category</h2>
              <Link
                href="/tools"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                View All Tools →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {tools.map((tool: any) => (
                <ToolCard key={tool.id} tool={tool} />
              ))}
            </div>
          </section>
        ) : (
          <section className="mb-12">
            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
              <p className="text-gray-500 text-lg mb-2">No tools in this category yet</p>
              <p className="text-gray-400">Check back soon for new tools!</p>
            </div>
          </section>
        )}

        {/* 相关文章 */}
        {articles && articles.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold">Related Articles</h2>
              <Link
                href="/blog"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                View All Articles →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article: any) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

