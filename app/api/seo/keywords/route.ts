import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

// GET: 获取关键词分析数据
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const keyword = searchParams.get('keyword')
    const type = searchParams.get('type') || 'all' // all, tools, articles, categories

    if (!keyword) {
      return NextResponse.json(
        { error: 'Keyword parameter is required' },
        { status: 400 }
      )
    }

    const results: any = {
      keyword,
      type,
      matches: [],
      suggestions: [],
    }

    // 搜索工具
    if (type === 'all' || type === 'tools') {
      const { data: tools } = await supabase
        .from('tools')
        .select('id, name, slug, description, view_count, use_count')
        .or(`name.ilike.%${keyword}%,description.ilike.%${keyword}%,short_description.ilike.%${keyword}%`)
        .eq('is_active', true)
        .limit(10)

      if (tools) {
        results.matches.push(
          ...tools.map((tool) => ({
            type: 'tool',
            title: tool.name,
            url: `/tools/${tool.slug}`,
            description: tool.description,
            metrics: {
              views: tool.view_count || 0,
              uses: tool.use_count || 0,
            },
          }))
        )
      }
    }

    // 搜索文章
    if (type === 'all' || type === 'articles') {
      const { data: articles } = await supabase
        .from('articles')
        .select('id, title, slug, excerpt, view_count')
        .or(`title.ilike.%${keyword}%,content.ilike.%${keyword}%,excerpt.ilike.%${keyword}%`)
        .eq('is_published', true)
        .limit(10)

      if (articles) {
        results.matches.push(
          ...articles.map((article) => ({
            type: 'article',
            title: article.title,
            url: `/blog/${article.slug}`,
            description: article.excerpt,
            metrics: {
              views: article.view_count || 0,
            },
          }))
        )
      }
    }

    // 生成关键词建议
    const keywordVariations = [
      `free ${keyword}`,
      `${keyword} online`,
      `online ${keyword}`,
      `best ${keyword}`,
      `how to ${keyword}`,
      `${keyword} tool`,
      `${keyword} free`,
    ]

    results.suggestions = keywordVariations

    return NextResponse.json(results)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

