import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Search - QuickToolsHub',
  description: 'Search for free online tools, articles, and categories on QuickToolsHub',
  robots: {
    index: true,
    follow: true,
  },
}

interface SearchParams {
  q?: string
}

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>
}) {
  const params = await searchParams
  const query = params.q || ''

  let tools: any[] = []
  let articles: any[] = []
  let categories: any[] = []

  if (query) {
    // 搜索工具
    const { data: toolsData } = await supabase
      .from('tools')
      .select('*, categories(name, slug)')
      .or(`name.ilike.%${query}%,description.ilike.%${query}%,short_description.ilike.%${query}%`)
      .eq('is_active', true)
      .limit(20)

    tools = toolsData || []

    // 搜索文章
    const { data: articlesData } = await supabase
      .from('articles')
      .select('*')
      .or(`title.ilike.%${query}%,content.ilike.%${query}%,excerpt.ilike.%${query}%`)
      .eq('is_published', true)
      .limit(10)

    articles = articlesData || []

    // 搜索分类
    const { data: categoriesData } = await supabase
      .from('categories')
      .select('*')
      .or(`name.ilike.%${query}%,description.ilike.%${query}%`)
      .limit(10)

    categories = categoriesData || []
  }

  const totalResults = tools.length + articles.length + categories.length

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold mb-3 sm:mb-4">Search Results</h1>
        {query && (
          <p className="text-sm sm:text-base text-gray-600">
            Found {totalResults} results for "{query}"
          </p>
        )}
      </div>

      {/* Search Box */}
      <div className="mb-6 sm:mb-8">
        <form action="/search" method="get" className="relative">
          <input
            type="text"
            name="q"
            defaultValue={query}
            placeholder="Search tools, articles..."
            className="w-full px-4 sm:px-6 py-3 sm:py-4 pl-10 sm:pl-12 pr-20 sm:pr-24 border border-gray-300 rounded-lg text-base sm:text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px]"
          />
          <MagnifyingGlassIcon className="absolute left-3 sm:left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 sm:h-6 sm:w-6 text-gray-400" />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-4 sm:px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base min-h-[36px] min-w-[60px] touch-manipulation"
          >
            Search
          </button>
        </form>
      </div>

      {!query && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Enter a search term to find tools and articles</p>
          <div className="mt-6 flex flex-wrap gap-2 justify-center">
            <span className="px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
              PDF Tools
            </span>
            <span className="px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
              Image Tools
            </span>
            <span className="px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
              Text Tools
            </span>
            <span className="px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
              Developer Tools
            </span>
          </div>
        </div>
      )}

      {query && totalResults === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No results found for "{query}"</p>
          <p className="text-gray-400 mt-2">Try different keywords or browse our categories</p>
        </div>
      )}

      {/* Tools Results */}
      {tools.length > 0 && (
        <section className="mb-8 sm:mb-12">
          <h2 className="text-xl sm:text-2xl font-semibold mb-4 sm:mb-6">Tools ({tools.length})</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {tools.map((tool: any) => (
              <Link
                key={tool.id}
                href={`/tools/${tool.slug}`}
                className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🔧</span>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-1">{tool.name}</h3>
                    <p className="text-gray-600 text-sm line-clamp-2">
                      {tool.short_description || tool.description}
                    </p>
                    <div className="mt-2 flex items-center space-x-2">
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                        Free
                      </span>
                      {tool.tool_type === 'self_developed' && (
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          Online
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Articles Results */}
      {articles.length > 0 && (
        <section className="mb-8 sm:mb-12">
          <h2 className="text-xl sm:text-2xl font-semibold mb-4 sm:mb-6">Articles ({articles.length})</h2>
          <div className="space-y-4">
            {articles.map((article: any) => (
              <Link
                key={article.id}
                href={`/blog/${article.slug}`}
                className="block bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
              >
                <h3 className="font-semibold text-xl mb-2">{article.title}</h3>
                {article.excerpt && (
                  <p className="text-gray-600 mb-3 line-clamp-2">{article.excerpt}</p>
                )}
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  {article.reading_time && (
                    <span>{article.reading_time} min read</span>
                  )}
                  {article.published_at && (
                    <span>{new Date(article.published_at).toLocaleDateString()}</span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Categories Results */}
      {categories.length > 0 && (
        <section className="mb-8 sm:mb-12">
          <h2 className="text-xl sm:text-2xl font-semibold mb-4 sm:mb-6">Categories ({categories.length})</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {categories.map((category: any) => (
              <Link
                key={category.id}
                href={`/categories/${category.slug}`}
                className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow text-center"
              >
                <div className="text-3xl mb-2">📁</div>
                <h3 className="font-semibold text-lg mb-1">{category.name}</h3>
                {category.description && (
                  <p className="text-gray-600 text-sm">{category.description}</p>
                )}
                <div className="mt-2 text-sm text-gray-500">
                  {category.tool_count} tools
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

