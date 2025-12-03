'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, TrashIcon } from '@heroicons/react/24/outline'

interface SplitPage {
  start: number
  end: number
}

export default function PDFSplitterTool() {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [totalPages, setTotalPages] = useState(0)
  const [splitPages, setSplitPages] = useState<SplitPage[]>([])
  const [splitPdfs, setSplitPdfs] = useState<{ name: string; url: string }[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const loadPdfInfo = async (file: File) => {
    try {
      const { PDFDocument } = await import('pdf-lib')
      const arrayBuffer = await file.arrayBuffer()
      const pdf = await PDFDocument.load(arrayBuffer)
      const pages = pdf.getPageCount()
      setTotalPages(pages)
      setSplitPages([{ start: 1, end: pages }])
    } catch (err: any) {
      setError('Failed to load PDF. Please make sure it is a valid PDF file.')
      console.error('PDF load error:', err)
    }
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Please select a PDF file.')
      return
    }

    setPdfFile(file)
    setError('')
    setSplitPdfs([])
    await loadPdfInfo(file)
    
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const addSplitRange = () => {
    setSplitPages(prev => [...prev, { start: 1, end: totalPages }])
  }

  const updateSplitRange = (index: number, field: 'start' | 'end', value: number) => {
    setSplitPages(prev => {
      const newPages = [...prev]
      newPages[index] = { ...newPages[index], [field]: value }
      return newPages
    })
    setSplitPdfs([])
  }

  const removeSplitRange = (index: number) => {
    setSplitPages(prev => prev.filter((_, i) => i !== index))
    setSplitPdfs([])
  }

  const handleSplit = async () => {
    if (!pdfFile) {
      setError('Please upload a PDF file first.')
      return
    }

    if (splitPages.length === 0) {
      setError('Please add at least one page range.')
      return
    }

    setIsProcessing(true)
    setError('')
    setSplitPdfs([])

    try {
      const { PDFDocument } = await import('pdf-lib')
      const arrayBuffer = await pdfFile.arrayBuffer()
      const sourcePdf = await PDFDocument.load(arrayBuffer)

      const newPdfs: { name: string; url: string }[] = []

      for (let i = 0; i < splitPages.length; i++) {
        const range = splitPages[i]
        const newPdf = await PDFDocument.create()

        // 验证页面范围
        const start = Math.max(1, Math.min(range.start, totalPages))
        const end = Math.max(start, Math.min(range.end, totalPages))

        // 复制页面（PDF页面索引从0开始）
        const pageIndices = Array.from({ length: end - start + 1 }, (_, i) => start - 1 + i)
        const pages = await newPdf.copyPages(sourcePdf, pageIndices)
        pages.forEach(page => newPdf.addPage(page))

        // 生成PDF
        const pdfBytes = await newPdf.save()
        const blob = new Blob([pdfBytes as any], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)

        newPdfs.push({
          name: `split-${i + 1}-pages-${start}-${end}.pdf`,
          url,
        })
      }

      setSplitPdfs(newPdfs)
    } catch (err: any) {
      setError(err.message || 'Failed to split PDF. Please try again.')
      console.error('PDF split error:', err)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDownload = (url: string, name: string) => {
    const a = document.createElement('a')
    a.href = url
    a.download = name
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  const handleClear = () => {
    setPdfFile(null)
    setTotalPages(0)
    setSplitPages([])
    setSplitPdfs([])
    setError('')
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
          <div className="mt-2 p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">{pdfFile.name}</p>
                <p className="text-xs text-gray-500 mt-1">
                  Total pages: {totalPages}
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
          </div>
        )}
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {/* 页面范围设置 */}
      {totalPages > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-700">
              Page Ranges
            </h3>
            <button
              onClick={addSplitRange}
              className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              Add Range
            </button>
          </div>
          <div className="space-y-3">
            {splitPages.map((range: any, index: number) => (
              <div
                key={index}
                className="flex items-center space-x-4 p-3 bg-white border border-gray-200 rounded-lg"
              >
                <span className="text-sm font-medium text-gray-500">
                  {index + 1}.
                </span>
                <div className="flex items-center space-x-2 flex-1">
                  <label className="text-sm text-gray-700">From:</label>
                  <input
                    type="number"
                    min="1"
                    max={totalPages}
                    value={range.start}
                    onChange={(e) => updateSplitRange(index, 'start', Number(e.target.value))}
                    className="w-20 px-2 py-1 border border-gray-300 rounded text-sm"
                  />
                  <label className="text-sm text-gray-700">To:</label>
                  <input
                    type="number"
                    min="1"
                    max={totalPages}
                    value={range.end}
                    onChange={(e) => updateSplitRange(index, 'end', Number(e.target.value))}
                    className="w-20 px-2 py-1 border border-gray-300 rounded text-sm"
                  />
                  <span className="text-xs text-gray-500">
                    ({range.end - range.start + 1} pages)
                  </span>
                </div>
                <button
                  onClick={() => removeSplitRange(index)}
                  className="p-1 text-red-400 hover:text-red-600"
                  title="Remove range"
                >
                  <TrashIcon className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
          <button
            onClick={handleSplit}
            disabled={isProcessing || splitPages.length === 0}
            className="mt-4 w-full px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
          >
            {isProcessing ? 'Splitting PDF...' : 'Split PDF'}
          </button>
        </div>
      )}

      {/* 分割结果 */}
      {splitPdfs.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Split PDFs ({splitPdfs.length})
          </h3>
          <div className="space-y-2">
            {splitPdfs.map((pdf: any, index: number) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg"
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-green-900 truncate">
                    {pdf.name}
                  </p>
                </div>
                <button
                  onClick={() => handleDownload(pdf.url, pdf.name)}
                  className="flex items-center space-x-2 px-4 py-3 sm:py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation ml-2 sm:ml-4"
                >
                  <ArrowDownTrayIcon className="h-5 w-5" />
                  <span>Download</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 使用说明 */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">How to use:</h4>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Upload a PDF file</li>
          <li>Add page ranges (e.g., pages 1-5, 6-10)</li>
          <li>Click "Split PDF" to create separate PDF files</li>
          <li>Download each split PDF file</li>
        </ol>
      </div>
    </div>
  )
}

