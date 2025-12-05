import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'
export const maxDuration = 60 // 60 seconds timeout

// 支持多个背景移除 API
const BACKGROUND_REMOVAL_APIS = {
  removebg: {
    url: 'https://api.remove.bg/v1.0/removebg',
    headerKey: 'X-Api-Key',
    getApiKey: () => process.env.REMOVE_BG_API_KEY || process.env.NEXT_PUBLIC_REMOVE_BG_API_KEY,
  },
  erasebg: {
    url: 'https://api.erase.bg/api/v1/remove-background',
    headerKey: 'X-Api-Key',
    getApiKey: () => process.env.ERASE_BG_API_KEY || process.env.NEXT_PUBLIC_ERASE_BG_API_KEY,
  },
  // 可以添加更多 API
}

// 将文件名转换为安全的 ASCII 文件名
function sanitizeFileName(fileName: string): string {
  // 获取文件扩展名
  const ext = fileName.substring(fileName.lastIndexOf('.'))
  // 生成安全的文件名（只包含字母、数字、连字符和下划线）
  const safeName = `image_${Date.now()}_${Math.random().toString(36).substring(2, 9)}${ext}`
  return safeName
}

// 尝试使用可用的 API
async function removeBackgroundWithAPI(
  buffer: Buffer,
  fileName: string,
  fileType: string
): Promise<{ success: boolean; data?: Buffer; error?: string }> {
  // 优先级：1. Remove.bg 2. Erase.bg
  const apis = ['removebg', 'erasebg'] as const

  // 将文件名转换为安全的 ASCII 文件名，避免编码问题
  const safeFileName = sanitizeFileName(fileName)

  for (const apiName of apis) {
    const api = BACKGROUND_REMOVAL_APIS[apiName]
    const apiKey = api.getApiKey()

    if (!apiKey || apiKey === 'your_api_key' || apiKey === 'your_remove_bg_api_key') {
      continue // 跳过未配置的 API
    }

    try {
      const formDataToSend = new FormData()
      const blob = new Blob([buffer as any], { type: fileType })
      // 使用安全的文件名，避免中文字符编码问题
      formDataToSend.append('image_file', blob, safeFileName)
      formDataToSend.append('size', 'auto')

      const response = await fetch(api.url, {
        method: 'POST',
        headers: {
          [api.headerKey]: apiKey,
        },
        body: formDataToSend,
      })

      if (response.ok) {
        const processedBlob = await response.blob()
        const processedBuffer = Buffer.from(await processedBlob.arrayBuffer())
        return { success: true, data: processedBuffer }
      } else if (response.status === 402 || response.status === 403) {
        // API Key 无效或配额用完，尝试下一个
        continue
      } else {
        // 其他错误，尝试下一个
        continue
      }
    } catch (error) {
      // 网络错误，尝试下一个
      continue
    }
  }

  return { success: false, error: 'No available background removal API configured' }
}

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

    // 准备文件数据
    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // 尝试使用可用的 API
    const result = await removeBackgroundWithAPI(buffer, file.name, file.type)

    if (!result.success) {
      return NextResponse.json(
        { 
          error: result.error || 'Background removal service is not available. Please configure an API key (Remove.bg or Erase.bg).',
          details: 'You can get a free API key from: https://www.erase.bg/api (if Remove.bg is unavailable)'
        },
        { status: 500 }
      )
    }

    // 生成安全的下载文件名（避免中文字符问题）
    const originalName = file.name.replace(/\.[^/.]+$/, '')
    // 将中文文件名转换为安全的 ASCII 文件名
    const safeDownloadName = originalName.match(/[\u4e00-\u9fa5]/) 
      ? `no-background-${Date.now()}.png`
      : `no-background-${originalName}.png`

    // 返回处理后的图片
    return new NextResponse(result.data as any, {
      status: 200,
      headers: {
        'Content-Type': 'image/png',
        'Content-Disposition': `attachment; filename="${safeDownloadName}"`,
        'X-Original-Size': file.size.toString(),
        'X-Processed-Size': result.data!.length.toString(),
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
