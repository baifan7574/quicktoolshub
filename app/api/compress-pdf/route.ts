import { NextRequest, NextResponse } from 'next/server'
import { PDFDocument } from 'pdf-lib'
import { exec } from 'child_process'
import { promisify } from 'util'
import { writeFile, unlink, readFile } from 'fs/promises'
import { join } from 'path'
import { tmpdir } from 'os'

const execAsync = promisify(exec)

export const runtime = 'nodejs'
export const maxDuration = 120 // 120 seconds timeout for Ghostscript

// 检查 Ghostscript 是否可用
async function isGhostscriptAvailable(): Promise<boolean> {
  try {
    // 先尝试直接使用 gs 命令
    await execAsync('gs --version')
    return true
  } catch {
    // 如果失败，尝试使用完整路径（Windows）
    try {
      const { execSync } = require('child_process')
      const fs = require('fs')
      const path = require('path')
      
      // 检查常见的 Ghostscript 安装路径
      const possiblePaths = [
        'C:\\Program Files\\gs\\gs10.03.1\\bin\\gswin64c.exe',
        'C:\\Program Files\\gs\\gs10.00.0\\bin\\gswin64c.exe',
      ]
      
      // 动态查找最新版本
      const gsBasePath = 'C:\\Program Files\\gs'
      if (fs.existsSync(gsBasePath)) {
        const versions = fs.readdirSync(gsBasePath).filter((dir: string) => dir.startsWith('gs'))
        if (versions.length > 0) {
          const latestVersion = versions.sort().reverse()[0]
          const gsPath = path.join(gsBasePath, latestVersion, 'bin', 'gswin64c.exe')
          if (fs.existsSync(gsPath)) {
            return true
          }
        }
      }
      
      return false
    } catch {
      return false
    }
  }
}

// 获取 Ghostscript 可执行文件路径
function getGhostscriptPath(): string {
  const fs = require('fs')
  const path = require('path')
  
  // 先尝试直接使用 gs 命令（如果已在 PATH 中）
  try {
    require('child_process').execSync('gs --version', { stdio: 'ignore' })
    return 'gs'
  } catch {
    // 查找 Windows 安装路径
    const gsBasePath = 'C:\\Program Files\\gs'
    if (fs.existsSync(gsBasePath)) {
      const versions = fs.readdirSync(gsBasePath).filter((dir: string) => dir.startsWith('gs'))
      if (versions.length > 0) {
        const latestVersion = versions.sort().reverse()[0]
        const gsPath = path.join(gsBasePath, latestVersion, 'bin', 'gswin64c.exe')
        if (fs.existsSync(gsPath)) {
          return gsPath
        }
      }
    }
    
    // Linux/Mac 路径
    const linuxPaths = ['/usr/bin/gs', '/usr/local/bin/gs']
    for (const p of linuxPaths) {
      if (fs.existsSync(p)) {
        return p
      }
    }
    
    return 'gs' // 默认尝试
  }
}

// 使用 Ghostscript 压缩 PDF
async function compressWithGhostscript(
  inputPath: string,
  outputPath: string,
  quality: 'screen' | 'ebook' | 'printer' | 'prepress' = 'ebook'
): Promise<void> {
  const gsPath = getGhostscriptPath()
  const command = `"${gsPath}" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/${quality} -dNOPAUSE -dQUIET -dBATCH -dAutoRotatePages=/None -sOutputFile="${outputPath}" "${inputPath}"`
  
  await execAsync(command)
}

export async function POST(request: NextRequest) {
  let inputPath: string | null = null
  let outputPath: string | null = null

  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const quality = (formData.get('quality') as string) || 'ebook' // screen, ebook, printer, prepress

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

    // 检查文件大小（限制 500MB）
    const maxSize = 500 * 1024 * 1024 // 500MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size exceeds 500MB limit' },
        { status: 400 }
      )
    }

    const arrayBuffer = await file.arrayBuffer()
    const originalSize = arrayBuffer.byteLength

    // 优先尝试使用 Ghostscript（如果可用）
    const gsAvailable = await isGhostscriptAvailable()

    if (gsAvailable) {
      // 使用 Ghostscript 压缩（效果更好）
      try {
        // 创建临时文件
        const tempDir = tmpdir()
        const timestamp = Date.now()
        inputPath = join(tempDir, `input-${timestamp}.pdf`)
        outputPath = join(tempDir, `output-${timestamp}.pdf`)

        // 写入输入文件
        await writeFile(inputPath, Buffer.from(arrayBuffer))

        // 使用 Ghostscript 压缩
        await compressWithGhostscript(inputPath, outputPath, quality as any)

        // 读取压缩后的文件
        const compressedBuffer = await readFile(outputPath)
        const compressedSize = compressedBuffer.byteLength
        const compressionRatio = ((1 - compressedSize / originalSize) * 100).toFixed(2)

        // 清理临时文件
        try {
          await unlink(inputPath)
          await unlink(outputPath)
        } catch (cleanupErr) {
          console.warn('Failed to cleanup temp files:', cleanupErr)
        }

        // 如果压缩后文件更大，返回原始文件
        if (compressedSize >= originalSize) {
          return NextResponse.json({
            success: false,
            message: 'Unable to compress this PDF further. The file may already be optimized.',
            originalSize,
            compressedSize: originalSize,
            compressionRatio: '0.00',
            method: 'ghostscript',
          })
        }

        // 返回压缩后的 PDF
        return new NextResponse(compressedBuffer as any, {
          status: 200,
          headers: {
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="compressed-${file.name}"`,
            'X-Original-Size': originalSize.toString(),
            'X-Compressed-Size': compressedSize.toString(),
            'X-Compression-Ratio': compressionRatio,
            'X-Compression-Method': 'ghostscript',
          },
        })
      } catch (gsError: any) {
        console.error('Ghostscript compression error:', gsError)
        // 如果 Ghostscript 失败，回退到 pdf-lib
        console.log('Falling back to pdf-lib compression')
      }
    }

    // 回退方案：使用 pdf-lib（如果 Ghostscript 不可用或失败）
    const pdf = await PDFDocument.load(arrayBuffer, {
      ignoreEncryption: true,
    })

    // 保存 PDF，使用压缩选项
    const pdfBytes = await pdf.save({
      useObjectStreams: false,
      addDefaultPage: false,
    })

    const compressedSize = pdfBytes.byteLength
    const compressionRatio = ((1 - compressedSize / originalSize) * 100).toFixed(2)

    // 如果压缩后文件更大，返回原始文件
    if (compressedSize >= originalSize) {
      return NextResponse.json({
        success: false,
        message: 'Unable to compress this PDF further. The file may already be optimized.',
        originalSize,
        compressedSize: originalSize,
        compressionRatio: '0.00',
        method: 'pdf-lib',
      })
    }

    // 如果压缩效果不明显（小于1%），也返回提示（但使用更友好的消息）
    if (parseFloat(compressionRatio) < 1) {
      return NextResponse.json({
        success: true, // 改为 true，这样前端会显示为成功而不是错误
        message: `Your PDF has been processed. The file size was reduced by ${compressionRatio}%. This PDF appears to be already well-optimized.`,
        originalSize,
        compressedSize,
        compressionRatio,
        method: 'pdf-lib',
      })
    }

    // 返回压缩后的 PDF
    return new NextResponse(Buffer.from(pdfBytes) as any, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="compressed-${file.name}"`,
        'X-Original-Size': originalSize.toString(),
        'X-Compressed-Size': compressedSize.toString(),
        'X-Compression-Ratio': compressionRatio,
        'X-Compression-Method': 'pdf-lib',
      },
    })
  } catch (error: any) {
    // 清理临时文件
    if (inputPath) {
      try {
        await unlink(inputPath)
      } catch {}
    }
    if (outputPath) {
      try {
        await unlink(outputPath)
      } catch {}
    }

    console.error('PDF compression error:', error)
    return NextResponse.json(
      {
        error: error.message || 'Failed to compress PDF',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined,
      },
      { status: 500 }
    )
  }
}
