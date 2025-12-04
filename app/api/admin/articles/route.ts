import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

// GET: 获取所有文章
export async function GET() {
  try {
    const { data, error } = await supabase
      .from('articles')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

// POST: 创建新文章
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const {
      title,
      slug,
      excerpt,
      content,
      category,
      tags,
      featured_image,
      reading_time,
      is_published,
      published_at,
    } = body

    // 验证必填字段
    if (!title || !slug || !content) {
      return NextResponse.json(
        { error: '标题、Slug 和内容为必填项' },
        { status: 400 }
      )
    }

    // 检查 slug 是否已存在
    const { data: existing } = await supabase
      .from('articles')
      .select('id')
      .eq('slug', slug)
      .single()

    if (existing) {
      return NextResponse.json(
        { error: '该 Slug 已存在，请使用其他 Slug' },
        { status: 400 }
      )
    }

    // 创建文章
    const { data, error } = await supabase
      .from('articles')
      .insert({
        title,
        slug,
        excerpt: excerpt || null,
        content,
        category: category || null,
        tags: tags || [],
        featured_image: featured_image || null,
        reading_time: reading_time || null,
        is_published: is_published || false,
        published_at: published_at || null,
      })
      .select()
      .single()

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json(data, { status: 201 })
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

