'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, TrashIcon } from '@heroicons/react/24/outline'

export default function PDFToWordTool() {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Please select a PDF file.')
      return
    }

    setPdfFile(file)
    setError('')
    setSuccess(false)
    
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const convertPDFToWord = async () => {
    if (!pdfFile) {
      setError('Please upload a PDF file first.')
      return
    }

    setIsProcessing(true)
    setError('')
    setSuccess(false)

    try {
      const formData = new FormData()
      formData.append('file', pdfFile)

      const response = await fetch('/api/pdf-to-word', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `Server error: ${response.status}`)
      }

      // 获取 Word 文档
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)

      // 自动下载
      const a = document.createElement('a')
      a.href = url
      a.download = pdfFile.name.replace('.pdf', '.docx')
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)

      // 清理
      URL.revokeObjectURL(url)

      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Failed to convert PDF to Word. Please make sure it is a valid PDF file.')
      console.error('PDF to Word conversion error:', err)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleClear = () => {
    setPdfFile(null)
    setError('')
    setSuccess(false)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
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
          className="block w-full text-base sm:text-sm text-gray-500 file:mr-4 file:py-3 sm:file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-base sm:file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 file:min-h-[44px] touch-manipulation"
        />
        {pdfFile && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="text-sm font-medium text-gray-900">{pdfFile.name}</p>
                <p className="text-xs text-gray-500 mt-1">
                  File size: {formatFileSize(pdfFile.size)}
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
            <button
              onClick={convertPDFToWord}
              disabled={isProcessing}
              className="w-full mt-3 px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
            >
              {isProcessing ? 'Converting PDF to Word...' : 'Convert to Word'}
            </button>
          </div>
        )}
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700">
          <p className="text-sm font-medium">Error</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}

      {/* 成功提示 */}
      {success && (
        <div className="p-4 rounded-lg bg-green-50 border border-green-200 text-green-700">
          <p className="text-sm font-medium">✅ Conversion successful!</p>
          <p className="text-sm mt-1">Your Word document has been downloaded.</p>
        </div>
      )}

      {/* 使用说明 */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">How to use:</h4>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Upload a PDF file</li>
          <li>Click "Convert to Word" to convert</li>
          <li>Download the converted Word document</li>
        </ol>
        <div className="mt-3 p-3 bg-blue-100 rounded text-xs text-blue-700">
          <p className="font-semibold mb-1">⚠️ Important Notes:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>This tool works best with text-based PDFs</li>
            <li>PDFs with only images may not convert properly</li>
            <li>Complex formatting may not be preserved perfectly</li>
            <li>Maximum file size: 100MB</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

