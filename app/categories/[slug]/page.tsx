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
        <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6 lg:p-8 mb-6 sm:mb-8">
          <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-3 sm:space-y-0 sm:space-x-4 mb-3 sm:mb-4">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center shadow-sm">
              <CategoryIcon slug={category.slug} name={category.name} size="md" className="sm:hidden" />
              <CategoryIcon slug={category.slug} name={category.name} size="lg" className="hidden sm:flex" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-2">{category.name}</h1>
              {category.description && (
                <p className="text-sm sm:text-base lg:text-lg text-gray-600">{category.description}</p>
              )}
            </div>
          </div>
          <div className="mt-3 sm:mt-4 text-sm sm:text-base text-gray-500">
            {category.tool_count} tools available
          </div>
        </div>

        {/* 工具列表 */}
        {tools && tools.length > 0 ? (
          <section className="mb-12">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 sm:mb-6 gap-3 sm:gap-0">
              <h2 className="text-xl sm:text-2xl font-semibold">Tools in this Category</h2>
              <Link
                href="/tools"
                className="text-blue-600 hover:text-blue-700 font-semibold text-sm sm:text-base min-h-[36px] flex items-center"
              >
                View All Tools →
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
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
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 sm:mb-6 gap-3 sm:gap-0">
              <h2 className="text-xl sm:text-2xl font-semibold">Related Articles</h2>
              <Link
                href="/blog"
                className="text-blue-600 hover:text-blue-700 font-semibold text-sm sm:text-base min-h-[36px] flex items-center"
              >
                View All Articles →
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
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

