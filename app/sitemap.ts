import { MetadataRoute } from 'next'
import { supabase } from '@/lib/supabase'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://soeasyhub.com'

  // 静态页面
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/tools`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/categories`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms-of-service`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/cookie-policy`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/disclaimer`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ]

  // 动态页面：工具
  const { data: tools } = await supabase
    .from('tools')
    .select('slug, updated_at')
    .eq('is_active', true)

  const toolPages: MetadataRoute.Sitemap =
    tools?.map((tool: any) => ({
      url: `${baseUrl}/tools/${tool.slug}`,
      lastModified: tool.updated_at ? new Date(tool.updated_at) : new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    })) || []

  // 动态页面：分类
  const { data: categories } = await supabase
    .from('categories')
    .select('slug, updated_at')

  const categoryPages: MetadataRoute.Sitemap =
    categories?.map((category: any) => ({
      url: `${baseUrl}/categories/${category.slug}`,
      lastModified: category.updated_at ? new Date(category.updated_at) : new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.6,
    })) || []

  // 动态页面：文章
  const { data: articles } = await supabase
    .from('articles')
    .select('slug, published_at')
    .eq('is_published', true)

  const articlePages: MetadataRoute.Sitemap =
    articles?.map((article: any) => ({
      url: `${baseUrl}/blog/${article.slug}`,
      lastModified: article.published_at ? new Date(article.published_at) : new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    })) || []

  return [...staticPages, ...toolPages, ...categoryPages, ...articlePages]
}

