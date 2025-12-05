import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import ArticleCard from '@/components/blog/ArticleCard'
import ToolCard from '@/components/tools/ToolCard'
import ToolRenderer from '@/components/tools/ToolRenderer'

// 生成长尾关键词（基于工具信息）
function generateLongTailKeywords(tool: any) {
  const keywords = []
  const toolName = tool.name.toLowerCase()
  const category = tool.categories?.name?.toLowerCase() || ''
  
  // 基础长尾关键词
  keywords.push(`free online ${toolName}`)
  keywords.push(`${toolName} online free`)
  keywords.push(`use ${toolName} free`)
  
  // 场景关键词
  if (category.includes('pdf')) {
    keywords.push(`free PDF ${toolName.replace('pdf ', '')}`)
    keywords.push(`${toolName} without watermark`)
    keywords.push(`${toolName} no sign up`)
  }
  
  if (category.includes('image')) {
    keywords.push(`free image ${toolName.replace('image ', '')}`)
    keywords.push(`${toolName} online`)
    keywords.push(`online ${toolName} tool`)
  }
  
  // 问题关键词
  keywords.push(`how to use ${toolName}`)
  keywords.push(`best free ${toolName}`)
  
  return keywords.join(', ')
}

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

  // 生成优化的标题和描述
  const title = `${tool.name} - Free Online Tool | QuickToolsHub`
  const description = tool.short_description || tool.description || 
    `Use ${tool.name} for free online. No registration required. Fast, secure, and easy to use.`
  
  // 生成长尾关键词
  const keywords = generateLongTailKeywords(tool)
  
  // 生成结构化数据
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: tool.name,
    description: description,
    url: `https://soeasyhub.com/tools/${tool.slug}`,
    applicationCategory: 'UtilityApplication',
    operatingSystem: 'Web',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    aggregateRating: tool.view_count > 0 ? {
      '@type': 'AggregateRating',
      ratingValue: '4.5',
      ratingCount: Math.floor(tool.view_count / 10),
    } : undefined,
  }

  return {
    title,
    description,
    keywords: keywords,
    openGraph: {
      title,
      description,
      url: `https://soeasyhub.com/tools/${tool.slug}`,
      siteName: 'QuickToolsHub',
      type: 'website',
      images: tool.screenshot_url ? [tool.screenshot_url] : [],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: tool.screenshot_url ? [tool.screenshot_url] : [],
    },
    alternates: {
      canonical: `https://soeasyhub.com/tools/${tool.slug}`,
    },
    other: {
      'structured-data': JSON.stringify(structuredData),
    },
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

  // 生成结构化数据
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: tool.name,
    description: tool.description || tool.short_description,
    url: `https://soeasyhub.com/tools/${tool.slug}`,
    applicationCategory: 'UtilityApplication',
    operatingSystem: 'Web',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
  }

  return (
    <>
      {/* 结构化数据 */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      
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
            {/* 主内容区 */}
            <div className="flex-1">
              {/* 工具标题和描述 */}
              <div className="mb-8">
                <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
                  {tool.name}
                </h1>
                {tool.description && (
                  <p className="text-lg text-gray-700 mb-4">{tool.description}</p>
                )}
                {tool.short_description && (
                  <p className="text-base text-gray-600">{tool.short_description}</p>
                )}
              </div>

              {/* 工具组件 */}
              <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8">
                <ToolRenderer tool={tool} />
              </div>

              {/* 使用说明（SEO内容） */}
              <div className="prose prose-lg max-w-none mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  How to Use {tool.name}
                </h2>
                <p className="text-gray-700 mb-4">
                  {tool.name} is a free online tool that allows you to {tool.description?.toLowerCase() || 'perform this task'} quickly and easily. 
                  No registration or sign-up is required. Simply upload your files or enter your data, and our tool will process it instantly.
                </p>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Key Features
                </h3>
                <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
                  <li>100% free to use - no hidden costs</li>
                  <li>No registration required - use instantly</li>
                  <li>Secure and private - your data is safe</li>
                  <li>Fast processing - results in seconds</li>
                  <li>Works in your browser - no software download needed</li>
                </ul>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Common Use Cases
                </h3>
                <p className="text-gray-700 mb-4">
                  {tool.name} is perfect for a variety of tasks. Whether you're working on a personal project, 
                  preparing documents for work, or handling files for school, our tool makes it easy to get the job done.
                </p>
              </div>

              {/* 相关文章 */}
              {relatedArticles && relatedArticles.length > 0 && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Related Articles
                  </h2>
                  <div className="space-y-4">
                    {relatedArticles.map((item: any) => (
                      <ArticleCard key={item.articles.id} article={item.articles} />
                    ))}
                  </div>
                </div>
              )}

              {/* 相关工具 */}
              {relatedTools && relatedTools.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Related Tools
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {relatedTools.map((relatedTool: any) => (
                      <ToolCard key={relatedTool.id} tool={relatedTool} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
