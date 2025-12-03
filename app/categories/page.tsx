import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { Category } from '@/types'
import CategoryIcon from '@/components/categories/CategoryIcon'

export const metadata = {
  title: 'All Categories - QuickToolsHub',
  description: 'Browse all tool categories on QuickToolsHub',
}

export default async function CategoriesPage() {
  // 获取所有分类
  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('tool_count', { ascending: false })

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* 页面标题 */}
        <div className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-2">All Categories</h1>
          <p className="text-sm sm:text-base text-gray-600">
            Browse tools by category. Find the perfect tool for your needs.
          </p>
        </div>

        {/* 分类列表 */}
        {categories && categories.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {categories.map((category: Category) => (
              <Link
                key={category.id}
                href={`/categories/${category.slug}`}
                className="bg-white p-4 sm:p-6 rounded-lg hover:bg-blue-50 transition-colors border border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md touch-manipulation"
              >
                <div className="flex items-start space-x-3 sm:space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center shadow-sm">
                    <CategoryIcon slug={category.slug} name={category.name} size="sm" className="sm:hidden" />
                    <CategoryIcon slug={category.slug} name={category.name} size="md" className="hidden sm:flex" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-gray-900 mb-1 sm:mb-2">
                      {category.name}
                    </h3>
                    {category.description && (
                      <p className="text-xs sm:text-sm text-gray-600 mb-2 sm:mb-3 line-clamp-2">
                        {category.description}
                      </p>
                    )}
                    <div className="flex items-center space-x-3 sm:space-x-4 text-xs sm:text-sm text-gray-500">
                      <span className="font-medium text-blue-600">
                        {category.tool_count || 0} tools
                      </span>
                      <span className="text-blue-600 hover:text-blue-700">
                        View All →
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <p className="text-gray-500 text-lg mb-4">No categories found</p>
            <p className="text-gray-400">Categories will appear here once they are added.</p>
          </div>
        )}

        {/* 快速链接 */}
        <div className="mt-8 sm:mt-12 bg-white rounded-lg shadow-sm p-4 sm:p-6">
          <h2 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Quick Links</h2>
          <div className="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4">
            <Link
              href="/tools"
              className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base font-medium min-h-[44px] flex items-center justify-center touch-manipulation"
            >
              View All Tools
            </Link>
            <Link
              href="/blog"
              className="px-4 py-3 sm:py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm sm:text-base font-medium min-h-[44px] flex items-center justify-center touch-manipulation"
            >
              Browse Articles
            </Link>
            <Link
              href="/search"
              className="px-4 py-3 sm:py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm sm:text-base font-medium min-h-[44px] flex items-center justify-center touch-manipulation"
            >
              Search Tools
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

