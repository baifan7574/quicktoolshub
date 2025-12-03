'use client'

import { useState, useRef } from 'react'
import { TrashIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline'

interface PDFFile {
  file: File
  id: string
  name: string
  size: number
}

export default function PDFMergerTool() {
  const [pdfFiles, setPdfFiles] = useState<PDFFile[]>([])
  const [mergedPdfUrl, setMergedPdfUrl] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const pdfFiles = files
      .filter(file => file.type === 'application/pdf')
      .map(file => ({
        file,
        id: Math.random().toString(36).substring(7),
        name: file.name,
        size: file.size,
      }))
    
    if (pdfFiles.length !== files.length) {
      setError('Some files are not PDF files and were skipped.')
    } else {
      setError('')
    }
    
    setPdfFiles(prev => [...prev, ...pdfFiles])
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const removeFile = (id: string) => {
    setPdfFiles(prev => prev.filter(f => f.id !== id))
    setMergedPdfUrl(null)
  }

  const moveFile = (index: number, direction: 'up' | 'down') => {
    if (
      (direction === 'up' && index === 0) ||
      (direction === 'down' && index === pdfFiles.length - 1)
    ) {
      return
    }
    
    const newFiles = [...pdfFiles]
    const targetIndex = direction === 'up' ? index - 1 : index + 1
    ;[newFiles[index], newFiles[targetIndex]] = [newFiles[targetIndex], newFiles[index]]
    setPdfFiles(newFiles)
    setMergedPdfUrl(null)
  }

  const handleMerge = async () => {
    if (pdfFiles.length < 2) {
      setError('Please upload at least 2 PDF files to merge.')
      return
    }

    setIsProcessing(true)
    setError('')
    setMergedPdfUrl(null)

    try {
      // 动态导入 pdf-lib（如果未安装，会提示用户）
      const { PDFDocument } = await import('pdf-lib')
      
      const mergedPdf = await PDFDocument.create()

      // 合并所有PDF
      for (const pdfFile of pdfFiles) {
        const arrayBuffer = await pdfFile.file.arrayBuffer()
        const pdf = await PDFDocument.load(arrayBuffer)
        const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices())
        pages.forEach(page => mergedPdf.addPage(page))
      }

      // 生成合并后的PDF
      const pdfBytes = await mergedPdf.save()
      const blob = new Blob([pdfBytes as any], { type: 'application/pdf' })
      const url = URL.createObjectURL(blob)
      setMergedPdfUrl(url)
    } catch (err: any) {
      setError(err.message || 'Failed to merge PDFs. Please make sure all files are valid PDFs.')
      console.error('PDF merge error:', err)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDownload = () => {
    if (mergedPdfUrl) {
      const a = document.createElement('a')
      a.href = mergedPdfUrl
      a.download = 'merged.pdf'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
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
      {/* 文件上传区域 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload PDF Files (Select multiple files)
        </label>
        <div className="flex items-center space-x-4">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            multiple
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>
        <p className="mt-2 text-sm text-gray-500">
          You can select multiple PDF files at once or add them one by one.
        </p>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {/* 文件列表 */}
      {pdfFiles.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-700">
              PDF Files ({pdfFiles.length})
            </h3>
            <button
              onClick={handleMerge}
              disabled={isProcessing || pdfFiles.length < 2}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
            >
              {isProcessing ? 'Merging...' : 'Merge PDFs'}
            </button>
          </div>
          <div className="space-y-2">
            {pdfFiles.map((pdfFile: File, index: number) => (
              <div
                key={pdfFile.id}
                className="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg"
              >
                <div className="flex items-center space-x-3 flex-1 min-w-0">
                  <span className="text-sm font-medium text-gray-500">
                    {index + 1}.
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {pdfFile.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(pdfFile.size)}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => moveFile(index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
                    title="Move up"
                  >
                    ↑
                  </button>
                  <button
                    onClick={() => moveFile(index, 'down')}
                    disabled={index === pdfFiles.length - 1}
                    className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
                    title="Move down"
                  >
                    ↓
                  </button>
                  <button
                    onClick={() => removeFile(pdfFile.id)}
                    className="p-1 text-red-400 hover:text-red-600"
                    title="Remove"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 合并结果 */}
      {mergedPdfUrl && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-800">
                ✅ PDFs merged successfully!
              </p>
              <p className="text-xs text-green-600 mt-1">
                Click download to save the merged PDF file.
              </p>
            </div>
            <button
              onClick={handleDownload}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
            >
              <ArrowDownTrayIcon className="h-5 w-5" />
              <span>Download</span>
            </button>
          </div>
        </div>
      )}

      {/* 使用说明 */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">How to use:</h4>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Click "Choose Files" and select multiple PDF files</li>
          <li>Arrange the order using ↑ and ↓ buttons if needed</li>
          <li>Click "Merge PDFs" to combine all files</li>
          <li>Download the merged PDF file</li>
        </ol>
      </div>
    </div>
  )
}

