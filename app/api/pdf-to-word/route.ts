import { NextRequest, NextResponse } from 'next/server'
import { Document, Packer, Paragraph, TextRun, HeadingLevel } from 'docx'
import { writeFile, unlink } from 'fs/promises'
import { join } from 'path'
import { tmpdir } from 'os'

export const runtime = 'nodejs'
export const maxDuration = 120 // 120 seconds timeout

export async function POST(request: NextRequest) {
  let tempPdfPath: string | null = null
  
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      )
    }

    if (file.type !== 'application/pdf') {
      return NextResponse.json(
        { error: 'File must be a PDF' },
        { status: 400 }
      )
    }

    // 检查文件大小（限制 100MB）
    const maxSize = 100 * 1024 * 1024 // 100MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size exceeds 100MB limit' },
        { status: 400 }
      )
    }

    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // 使用 pdf2json（专门为 Node.js 设计，无需浏览器 API）
    const PDFParser = require('pdf2json')
    
    // 创建临时文件
    const tempDir = tmpdir()
    const timestamp = Date.now()
    tempPdfPath = join(tempDir, `pdf-${timestamp}.pdf`)
    await writeFile(tempPdfPath, buffer)
    
    // 解析 PDF
    const pdfParser = new PDFParser(null, 1)
    
    // 使用 Promise 包装回调
    const pdfData = await new Promise<any>((resolve, reject) => {
      pdfParser.on('pdfParser_dataError', (err: any) => {
        reject(new Error(`PDF parsing error: ${err.parserError}`))
      })
      
      pdfParser.on('pdfParser_dataReady', (pdfData: any) => {
        resolve(pdfData)
      })
      
      pdfParser.loadPDF(tempPdfPath)
    })
    
    // 提取文本内容
    let fullText = ''
    
    if (pdfData.Pages && pdfData.Pages.length > 0) {
      for (const page of pdfData.Pages) {
        if (page.Texts && page.Texts.length > 0) {
          // 提取页面文本
          const pageText = page.Texts
            .map((textItem: any) => {
              // pdf2json 的文本是编码的，需要解码
              if (textItem.R && textItem.R.length > 0) {
                return textItem.R.map((r: any) => {
                  // 解码 URI 编码的文本
                  try {
                    return decodeURIComponent(r.T || '')
                  } catch {
                    return r.T || ''
                  }
                }).join('')
              }
              return ''
            })
            .join(' ')
          
          fullText += pageText + '\n\n'
        }
      }
    }
    
    const text = fullText.trim()
    
    // 清理临时文件
    if (tempPdfPath) {
      try {
        await unlink(tempPdfPath)
      } catch (err) {
        console.warn('Failed to delete temp file:', err)
      }
    }
    
    if (!text || text.trim().length === 0) {
      return NextResponse.json(
        { error: 'PDF appears to be empty or contains only images. Text-based PDFs are required for conversion.' },
        { status: 400 }
      )
    }

    // 将文本按段落分割
    const paragraphs = text
      .split(/\n\s*\n/) // 按双换行分割段落
      .map((para: string) => para.trim())
      .filter((para: string) => para.length > 0)

    // 创建 Word 文档
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: paragraphs.map((para: string, index: number) => {
            // 检查是否是标题（短文本且可能是标题）
            const isHeading = para.length < 100 && (
              para.match(/^[A-Z][^.!?]*$/) || // 全大写或首字母大写
              para.match(/^Chapter|Section|Part|Introduction|Conclusion/i) // 常见标题词
            )

            if (isHeading && index < 5) {
              // 前几个可能是标题
              return new Paragraph({
                text: para,
                heading: HeadingLevel.HEADING_1,
                spacing: { after: 200 },
              })
            }

            // 普通段落
            return new Paragraph({
              children: [
                new TextRun({
                  text: para,
                  size: 24, // 12pt
                }),
              ],
              spacing: { after: 200 },
            })
          }),
        },
      ],
    })

    // 生成 Word 文档
    const docxBuffer = await Packer.toBuffer(doc)

    // 返回 Word 文档
    return new NextResponse(docxBuffer as any, {
      status: 200,
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'Content-Disposition': `attachment; filename="${file.name.replace('.pdf', '.docx')}"`,
        'X-Original-Size': file.size.toString(),
        'X-Converted-Size': docxBuffer.length.toString(),
      },
    })
  } catch (error: any) {
    // 清理临时文件
    if (tempPdfPath) {
      try {
        await unlink(tempPdfPath)
      } catch (err) {
        console.warn('Failed to delete temp file:', err)
      }
    }
    
    console.error('PDF to Word conversion error:', error)
    
    // 处理特定错误
    if (error.message?.includes('Invalid PDF') || error.message?.includes('parsing error')) {
      return NextResponse.json(
        {
          error: 'Invalid PDF file. Please ensure the file is a valid PDF document.',
        },
        { status: 400 }
      )
    }

    return NextResponse.json(
      {
        error: error.message || 'Failed to convert PDF to Word',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined,
      },
      { status: 500 }
    )
  }
}

