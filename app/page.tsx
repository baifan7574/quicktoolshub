import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import ToolCard from '@/components/tools/ToolCard'
import ArticleCard from '@/components/blog/ArticleCard'
import CategoryIcon from '@/components/categories/CategoryIcon'

export default async function Home() {
  // 获取热门工具（浏览次数最多的）
  const { data: featuredTools } = await supabase
    .from('tools')
    .select('*, categories(name, slug)')
    .eq('is_active', true)
    .eq('is_featured', true)
    .order('view_count', { ascending: false })
    .limit(12)

  // 获取最新文章
  const { data: latestArticles } = await supabase
    .from('articles')
    .select('*')
    .eq('is_published', true)
    .order('published_at', { ascending: false })
    .limit(5)

  // 获取分类数据（用于显示工具数量）
  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('tool_count', { ascending: false })
    .limit(6)
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Free Online Tools
            </h1>
            <p className="text-2xl text-gray-600 mb-2">
              Quick & Easy Solutions
            </p>
            <p className="text-lg text-gray-500 mb-8">
              50+ Free Tools for PDF, Image, Text, and More
            </p>
            <div className="flex justify-center gap-4">
              <Link
                href="/tools"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Explore Tools
              </Link>
              <Link
                href="/categories"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition-colors"
              >
                View All Categories
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">50+</div>
              <div className="text-gray-600">Free Tools</div>
              <div className="text-sm text-gray-500 mt-1">Hand-picked and regularly updated</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">10,000+</div>
              <div className="text-gray-600">Monthly Users</div>
              <div className="text-sm text-gray-500 mt-1">Trusted by users worldwide</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">12</div>
              <div className="text-gray-600">Categories</div>
              <div className="text-sm text-gray-500 mt-1">Organized by use case</div>
            </div>
          </div>
        </div>
      </section>

      {/* Search Section */}
      <section className="py-12 bg-gray-50">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <form action="/search" method="get" className="relative">
            <input
              type="text"
              name="q"
              placeholder="Search tools, articles..."
              className="w-full px-6 py-4 pl-12 pr-24 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg
              className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Search
            </button>
          </form>
          <div className="mt-4 flex flex-wrap gap-2 justify-center">
            <Link
              href="/search?q=PDF Tools"
              className="px-4 py-2 bg-white rounded-full text-sm text-gray-600 border border-gray-200 hover:bg-blue-50 transition-colors"
            >
              PDF Tools
            </Link>
            <Link
              href="/search?q=Image Tools"
              className="px-4 py-2 bg-white rounded-full text-sm text-gray-600 border border-gray-200 hover:bg-blue-50 transition-colors"
            >
              Image Tools
            </Link>
            <Link
              href="/search?q=Text Tools"
              className="px-4 py-2 bg-white rounded-full text-sm text-gray-600 border border-gray-200 hover:bg-blue-50 transition-colors"
            >
              Text Tools
            </Link>
            <Link
              href="/search?q=Developer Tools"
              className="px-4 py-2 bg-white rounded-full text-sm text-gray-600 border border-gray-200 hover:bg-blue-50 transition-colors"
            >
              Developer Tools
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Tools Section */}
      {featuredTools && featuredTools.length > 0 && (
        <section className="py-16 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold">Featured Tools</h2>
              <Link
                href="/tools"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                View All Tools →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {featuredTools.map((tool: any) => (
                <ToolCard key={tool.id} tool={tool} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Categories Preview */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Browse by Category</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories && categories.map((category: any) => (
              <Link
                key={category.id}
                href={`/categories/${category.slug}`}
                className="bg-white p-6 rounded-lg text-center hover:bg-blue-50 transition-all border border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md"
              >
                <div className="flex justify-center mb-3">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center shadow-sm">
                    <CategoryIcon slug={category.slug} name={category.name} size="md" />
                  </div>
                </div>
                <div className="font-semibold text-gray-900 mb-1">{category.name}</div>
                <div className="text-sm text-gray-500">{category.tool_count} tools</div>
                <div className="text-xs text-blue-600 mt-2 font-medium">View All →</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Latest Articles Section */}
      {latestArticles && latestArticles.length > 0 && (
        <section className="py-16 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold">Latest Articles</h2>
              <Link
                href="/blog"
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                View All Articles →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {latestArticles.map((article: any) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  )
}
