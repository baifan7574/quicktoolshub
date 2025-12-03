import { supabase } from '@/lib/supabase'
import ToolCard from '@/components/tools/ToolCard'
import SortSelect from '@/components/tools/SortSelect'
import Link from 'next/link'
import { Category } from '@/types'

interface SearchParams {
  category?: string
  sort?: string
  page?: string
}

export default async function ToolsPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>
}) {
  const params = await searchParams
  const categorySlug = params.category
  const sort = params.sort || 'popular'
  const page = parseInt(params.page || '1')
  const limit = 20
  const offset = (page - 1) * limit

  // 获取所有分类
  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('name')

  // 构建查询
  let query = supabase
    .from('tools')
    .select('*, categories(name, slug)', { count: 'exact' })
    .eq('is_active', true)

  // 分类筛选
  if (categorySlug && categorySlug !== 'all') {
    const { data: category, error } = await supabase
      .from('categories')
      .select('id')
      .eq('slug', categorySlug)
      .single()

    if (category && !error) {
      query = query.eq('category_id', category.id)
    }
  }

  // 排序
  switch (sort) {
    case 'recent':
      query = query.order('created_at', { ascending: false })
      break
    case 'alphabetical':
      query = query.order('name', { ascending: true })
      break
    case 'most-used':
      query = query.order('use_count', { ascending: false })
      break
    default: // popular
      query = query.order('view_count', { ascending: false })
  }

  // 分页
  query = query.range(offset, offset + limit - 1)

  const { data: tools, count } = await query

  const totalPages = count ? Math.ceil(count / limit) : 1

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* 左侧分类筛选 */}
          <aside className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-24">
              <h2 className="text-lg font-semibold mb-4">Categories</h2>
              <nav className="space-y-2">
                <Link
                  href="/tools"
                  className={`block px-4 py-2 rounded-lg transition-colors ${
                    !categorySlug || categorySlug === 'all'
                      ? 'bg-blue-100 text-blue-700 font-semibold'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  All Tools
                </Link>
                {categories?.map((category: Category) => (
                  <Link
                    key={category.id}
                    href={`/tools?category=${category.slug}`}
                    className={`block px-4 py-2 rounded-lg transition-colors ${
                      categorySlug === category.slug
                        ? 'bg-blue-100 text-blue-700 font-semibold'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {category.name} ({category.tool_count})
                  </Link>
                ))}
              </nav>
            </div>
          </aside>

          {/* 中间工具列表 */}
          <main className="flex-1">
            {/* 排序和标题 */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <h1 className="text-2xl font-bold">
                  {categorySlug && categorySlug !== 'all'
                    ? categories?.find((c: Category) => c.slug === categorySlug)?.name || 'Tools'
                    : 'All Tools'}
                </h1>
                <SortSelect currentSort={sort} categorySlug={categorySlug} />
              </div>
            </div>

            {/* 工具列表 */}
            {tools && tools.length > 0 ? (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {tools.map((tool: any) => (
                    <ToolCard key={tool.id} tool={tool} />
                  ))}
                </div>

                {/* 分页 */}
                {totalPages > 1 && (
                  <div className="flex justify-center items-center space-x-2">
                    {page > 1 && (
                      <Link
                        href={`/tools?${new URLSearchParams({
                          ...(categorySlug && { category: categorySlug }),
                          ...(sort && { sort }),
                          page: (page - 1).toString(),
                        }).toString()}`}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
                      >
                        Previous
                      </Link>
                    )}
                    <span className="px-4 py-2 text-gray-600">
                      Page {page} of {totalPages}
                    </span>
                    {page < totalPages && (
                      <Link
                        href={`/tools?${new URLSearchParams({
                          ...(categorySlug && { category: categorySlug }),
                          ...(sort && { sort }),
                          page: (page + 1).toString(),
                        }).toString()}`}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
                      >
                        Next
                      </Link>
                    )}
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-sm p-12 text-center">
                <p className="text-gray-500 text-lg mb-4">No tools found</p>
                <p className="text-gray-400">
                  {categorySlug && categorySlug !== 'all'
                    ? 'This category does not have any tools yet.'
                    : 'No tools available yet. Check back soon!'}
                </p>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}

