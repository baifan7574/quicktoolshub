'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, TrashIcon } from '@heroicons/react/24/outline'

export default function PDFCompressorTool() {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [compressedPdfUrl, setCompressedPdfUrl] = useState<string | null>(null)
  const [originalSize, setOriginalSize] = useState(0)
  const [compressedSize, setCompressedSize] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const [compressionQuality, setCompressionQuality] = useState<'ebook' | 'screen' | 'printer' | 'prepress'>('ebook')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Please select a PDF file.')
      return
    }

    setPdfFile(file)
    setOriginalSize(file.size)
    setError('')
    setCompressedPdfUrl(null)
    
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const compressPDF = async () => {
    if (!pdfFile) {
      setError('Please upload a PDF file first.')
      return
    }

    setIsProcessing(true)
    setError('')
    setCompressedPdfUrl(null)

    try {
      // 使用后端 API 进行压缩
      const formData = new FormData()
      formData.append('file', pdfFile)
      formData.append('quality', compressionQuality)

      const response = await fetch('/api/compress-pdf', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `Server error: ${response.status}`)
      }

      // 检查响应类型
      const contentType = response.headers.get('content-type')
      
      if (contentType === 'application/json') {
        // 如果返回 JSON，说明压缩失败或效果不明显
        const data = await response.json()
        setError(data.message || 'Unable to compress this PDF further.')
        setCompressedSize(data.compressedSize || originalSize)
        
        // 仍然提供下载选项（原始文件）
        const arrayBuffer = await pdfFile.arrayBuffer()
        const blob = new Blob([arrayBuffer as any], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        setCompressedPdfUrl(url)
      } else {
        // 返回的是压缩后的 PDF 文件
        const pdfBytes = await response.arrayBuffer()
        const compressedSizeValue = parseInt(response.headers.get('X-Compressed-Size') || '0')
        
        const blob = new Blob([pdfBytes as any], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        setCompressedPdfUrl(url)
        setCompressedSize(compressedSizeValue || pdfBytes.byteLength)
      }
    } catch (err: any) {
      setError(err.message || 'Failed to compress PDF. Please make sure it is a valid PDF file.')
      console.error('PDF compression error:', err)
      
      // 如果 API 调用失败，提供原始文件下载
      try {
        const arrayBuffer = await pdfFile.arrayBuffer()
        const blob = new Blob([arrayBuffer as any], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        setCompressedPdfUrl(url)
        setCompressedSize(originalSize)
      } catch (fallbackErr) {
        console.error('Failed to create fallback download:', fallbackErr)
      }
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDownload = () => {
    if (compressedPdfUrl) {
      const a = document.createElement('a')
      a.href = compressedPdfUrl
      a.download = `compressed-${pdfFile?.name || 'file.pdf'}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  }

  const handleClear = () => {
    if (compressedPdfUrl) {
      URL.revokeObjectURL(compressedPdfUrl)
    }
    setPdfFile(null)
    setCompressedPdfUrl(null)
    setOriginalSize(0)
    setCompressedSize(0)
    setError('')
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getCompressionRatio = () => {
    if (originalSize === 0 || compressedSize === 0) return 0
    return Math.round((1 - compressedSize / originalSize) * 100)
  }

  return (
    <div className="space-y-6">
      {/* 文件上传 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload PDF File
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileSelect}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        {pdfFile && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="text-sm font-medium text-gray-900">{pdfFile.name}</p>
                <p className="text-xs text-gray-500 mt-1">
                  Original size: {formatFileSize(originalSize)}
                </p>
              </div>
              <button
                onClick={handleClear}
                className="p-1 text-red-400 hover:text-red-600"
                title="Remove file"
              >
                <TrashIcon className="h-5 w-5" />
              </button>
            </div>
            {/* 压缩质量选择 */}
            <div className="mt-3">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Compression Quality
              </label>
              <select
                value={compressionQuality}
                onChange={(e) => setCompressionQuality(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isProcessing}
              >
                <option value="screen">Screen (Lowest quality, smallest size)</option>
                <option value="ebook">Ebook (Balanced quality and size) - Recommended</option>
                <option value="printer">Printer (High quality, larger size)</option>
                <option value="prepress">Prepress (Highest quality, largest size)</option>
              </select>
            </div>
            <button
              onClick={compressPDF}
              disabled={isProcessing}
              className="w-full mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isProcessing ? 'Compressing PDF...' : 'Compress PDF'}
            </button>
          </div>
        )}
      </div>

      {/* 错误提示 */}
      {error && (
        <div className={`p-4 rounded-lg ${
          error.includes('Unable to compress') 
            ? 'bg-yellow-50 border border-yellow-200 text-yellow-700'
            : 'bg-red-50 border border-red-200 text-red-700'
        }`}>
          {error}
        </div>
      )}

      {/* 压缩结果 */}
      {compressedPdfUrl && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="mb-4">
            <p className="text-sm font-medium text-green-800 mb-2">
              ✅ PDF compressed successfully!
            </p>
            <div className="space-y-1 text-sm text-green-700">
              <p>Original size: {formatFileSize(originalSize)}</p>
              <p>Compressed size: {formatFileSize(compressedSize)}</p>
              {compressedSize < originalSize && (
                <p className="font-semibold">
                  Saved: {formatFileSize(originalSize - compressedSize)} ({getCompressionRatio()}% reduction)
                </p>
              )}
            </div>
          </div>
          <button
            onClick={handleDownload}
            className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <ArrowDownTrayIcon className="h-5 w-5" />
            <span>Download Compressed PDF</span>
          </button>
        </div>
      )}

      {/* 使用说明 */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">How to use:</h4>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Upload a PDF file</li>
          <li>Click "Compress PDF" to reduce file size</li>
          <li>Download the compressed PDF file</li>
        </ol>
        <p className="text-xs text-blue-700 mt-2">
          <strong>Note:</strong> This tool uses browser-based compression which has limitations. 
          PDFs with already compressed images, encrypted content, or complex structures may not compress significantly. 
          For best results, try PDFs with uncompressed images or large file sizes. 
          For professional-grade compression, consider using server-side tools.
        </p>
      </div>
    </div>
  )
}
