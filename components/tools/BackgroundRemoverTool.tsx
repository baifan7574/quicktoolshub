'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface ProcessedImage {
  original: File
  processed: Blob
  url: string
  originalSize: number
  processedSize: number
}

export default function BackgroundRemoverTool() {
  const [images, setImages] = useState<ProcessedImage[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  // 使用后端 API 移除背景
  const removeBackground = async (file: File): Promise<ProcessedImage> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/remove-background', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.error || 
        `Server error: ${response.status} ${response.statusText}`
      )
    }

    const blob = await response.blob()
    const url = URL.createObjectURL(blob)

    return {
      original: file,
      processed: blob,
      url,
      originalSize: file.size,
      processedSize: blob.size,
    }
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const imageFiles = files.filter(file => 
      file.type.startsWith('image/') && 
      ['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)
    )

    if (imageFiles.length === 0) {
      setError('Please select JPEG or PNG image files.')
      return
    }

    setIsProcessing(true)
    setError('')
    const newImages: ProcessedImage[] = []

    try {
      for (const file of imageFiles) {
        try {
          const processed = await removeBackground(file)
          newImages.push(processed)
        } catch (err: any) {
          console.error(`Error processing ${file.name}:`, err)
          setError(prev => prev + (prev ? '\n' : '') + `${file.name}: ${err.message}`)
        }
      }

      if (newImages.length > 0) {
        setImages(prev => [...prev, ...newImages])
      }
    } catch (error: any) {
      setError(error.message || 'Failed to remove background. Please try again.')
    } finally {
      setIsProcessing(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const removeImage = (index: number) => {
    const image = images[index]
    URL.revokeObjectURL(image.url)
    setImages(prev => prev.filter((_, i) => i !== index))
  }

  const handleDownload = (image: ProcessedImage, index: number) => {
    const a = document.createElement('a')
    a.href = image.url
    
    // 生成安全的下载文件名（避免中文字符问题）
    const originalName = image.original.name.replace(/\.[^/.]+$/, '')
    // 检查是否包含中文字符
    const hasChinese = /[\u4e00-\u9fa5]/.test(originalName)
    const downloadName = hasChinese
      ? `no-background-${Date.now()}.png`
      : `no-background-${originalName}.png`
    
    a.download = downloadName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
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
          Upload Images (JPEG or PNG)
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png"
          multiple
          onChange={handleFileSelect}
          disabled={isProcessing}
          className="block w-full text-base sm:text-sm text-gray-500 file:mr-4 file:py-3 sm:file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-base sm:file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50 file:min-h-[44px] touch-manipulation"
        />
        <p className="mt-2 text-sm text-gray-500">
          Select one or multiple images (JPEG/PNG only)
        </p>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700 whitespace-pre-line">{error}</p>
        </div>
      )}

      {/* 处理状态 */}
      {isProcessing && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span>Removing backgrounds... This may take a few seconds per image.</span>
          </div>
        </div>
      )}

      {/* 处理结果 */}
      {images.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700">
            Processed Images ({images.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {images.map((image: any, index: number) => (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {image.original.name}
                    </p>
                    <div className="mt-1 text-xs text-gray-500 space-y-1">
                      <p>Original: {formatFileSize(image.originalSize)}</p>
                      <p>Processed: {formatFileSize(image.processedSize)}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeImage(index)}
                    className="p-1 text-gray-400 hover:text-red-600 ml-2"
                    title="Remove"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>
                <div className="mb-2 grid grid-cols-2 gap-2">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Original</p>
                    <img
                      src={URL.createObjectURL(image.original)}
                      alt={`Original ${image.original.name}`}
                      className="w-full h-24 object-contain bg-gray-50 rounded border"
                    />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Background Removed</p>
                    <img
                      src={image.url}
                      alt={`Processed ${image.original.name}`}
                      className="w-full h-24 object-contain bg-gray-50 rounded border"
                    />
                  </div>
                </div>
                <button
                  onClick={() => handleDownload(image, index)}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
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
          <li>Upload JPEG or PNG images</li>
          <li>Wait for background removal (a few seconds per image)</li>
          <li>Preview and download images with backgrounds removed</li>
        </ol>
        <p className="text-xs text-blue-700 mt-2">
          Powered by AI technology. Fast and accurate background removal.
        </p>
      </div>
    </div>
  )
}

