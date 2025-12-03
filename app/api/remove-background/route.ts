import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'
export const maxDuration = 60 // 60 seconds timeout

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      )
    }

    // 检查文件类型
    if (!file.type.startsWith('image/') || 
        !['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
      return NextResponse.json(
        { error: 'File must be a JPEG or PNG image' },
        { status: 400 }
      )
    }

    // 检查文件大小（限制 10MB）
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size exceeds 10MB limit' },
        { status: 400 }
      )
    }

    // 获取 API Key（从服务器端环境变量）
    const apiKey = process.env.REMOVE_BG_API_KEY || process.env.NEXT_PUBLIC_REMOVE_BG_API_KEY

    if (!apiKey) {
      return NextResponse.json(
        { error: 'Remove.bg API key is not configured. Please contact the administrator.' },
        { status: 500 }
      )
    }

    // 准备文件数据
    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // 调用 Remove.bg API
    const formDataToSend = new FormData()
    const blob = new Blob([buffer as any], { type: file.type })
    formDataToSend.append('image_file', blob, file.name)
    formDataToSend.append('size', 'auto')

    const response = await fetch('https://api.remove.bg/v1.0/removebg', {
      method: 'POST',
      headers: {
        'X-Api-Key': apiKey,
      },
      body: formDataToSend,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      const errorMessage = errorData.error?.message || 
        `API Error: ${response.status} ${response.statusText}`
      
      // 处理特定错误
      if (response.status === 402) {
        return NextResponse.json(
          { error: 'API quota exceeded. Please try again later or contact support.' },
          { status: 402 }
        )
      }
      
      if (response.status === 403) {
        return NextResponse.json(
          { error: 'Invalid API key. Please contact the administrator.' },
          { status: 403 }
        )
      }

      return NextResponse.json(
        { error: errorMessage },
        { status: response.status }
      )
    }

    // 返回处理后的图片
    const processedBlob = await response.blob()
    const processedBuffer = Buffer.from(await processedBlob.arrayBuffer())

    return new NextResponse(processedBuffer as any, {
      status: 200,
      headers: {
        'Content-Type': 'image/png',
        'Content-Disposition': `attachment; filename="no-background-${file.name.replace(/\.[^/.]+$/, '')}.png"`,
        'X-Original-Size': file.size.toString(),
        'X-Processed-Size': processedBuffer.length.toString(),
      },
    })
  } catch (error: any) {
    console.error('Background removal error:', error)
    return NextResponse.json(
      {
        error: error.message || 'Failed to remove background',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined,
      },
      { status: 500 }
    )
  }
}

