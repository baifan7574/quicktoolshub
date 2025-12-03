'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface CompressedImage {
  original: File
  compressed: Blob
  originalSize: number
  compressedSize: number
  url: string
}

export default function ImageCompressorTool() {
  const [images, setImages] = useState<CompressedImage[]>([])
  const [quality, setQuality] = useState(0.8)
  const [maxWidth, setMaxWidth] = useState(1920)
  const [isProcessing, setIsProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const compressImage = (file: File): Promise<CompressedImage> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (e) => {
        const img = new Image()
        img.onload = () => {
          // 计算新尺寸
          let width = img.width
          let height = img.height
          
          if (width > maxWidth) {
            height = (height * maxWidth) / width
            width = maxWidth
          }

          // 创建canvas
          const canvas = document.createElement('canvas')
          canvas.width = width
          canvas.height = height
          const ctx = canvas.getContext('2d')
          
          if (!ctx) {
            reject(new Error('Failed to get canvas context'))
            return
          }

          // 绘制图片
          ctx.drawImage(img, 0, 0, width, height)

          // 转换为blob
          canvas.toBlob(
            (blob) => {
              if (!blob) {
                reject(new Error('Failed to compress image'))
                return
              }

              resolve({
                original: file,
                compressed: blob,
                originalSize: file.size,
                compressedSize: blob.size,
                url: URL.createObjectURL(blob),
              })
            },
            file.type || 'image/jpeg',
            quality
          )
        }
        
        img.onerror = () => reject(new Error('Failed to load image'))
        img.src = e.target?.result as string
      }
      
      reader.onerror = () => reject(new Error('Failed to read file'))
      reader.readAsDataURL(file)
    })
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const imageFiles = files.filter(file => file.type.startsWith('image/'))

    if (imageFiles.length === 0) {
      alert('Please select image files.')
      return
    }

    setIsProcessing(true)
    const newImages: CompressedImage[] = []

    try {
      for (const file of imageFiles) {
        const compressed = await compressImage(file)
        newImages.push(compressed)
      }
      setImages(prev => [...prev, ...newImages])
    } catch (error: any) {
      alert(`Error compressing images: ${error.message}`)
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

  const handleDownload = (image: CompressedImage, index: number) => {
    const a = document.createElement('a')
    a.href = image.url
    a.download = `compressed-${image.original.name}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  const handleRecompress = async () => {
    if (images.length === 0) return

    setIsProcessing(true)
    const newImages: CompressedImage[] = []

    try {
      for (const image of images) {
        const compressed = await compressImage(image.original)
        // 释放旧的URL
        URL.revokeObjectURL(image.url)
        newImages.push(compressed)
      }
      setImages(newImages)
    } catch (error: any) {
      alert(`Error recompressing images: ${error.message}`)
    } finally {
      setIsProcessing(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getCompressionRatio = (original: number, compressed: number) => {
    return Math.round((1 - compressed / original) * 100)
  }

  return (
    <div className="space-y-6">
      {/* 压缩设置 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="quality" className="block text-sm font-medium text-gray-700 mb-2">
            Quality: {Math.round(quality * 100)}%
          </label>
          <input
            id="quality"
            type="range"
            min="0.1"
            max="1"
            step="0.1"
            value={quality}
            onChange={(e) => setQuality(Number(e.target.value))}
            className="w-full"
          />
          <p className="text-xs text-gray-500 mt-1">
            Lower quality = smaller file size
          </p>
        </div>
        <div>
          <label htmlFor="max-width" className="block text-sm font-medium text-gray-700 mb-2">
            Max Width: {maxWidth}px
          </label>
          <input
            id="max-width"
            type="range"
            min="400"
            max="3840"
            step="40"
            value={maxWidth}
            onChange={(e) => setMaxWidth(Number(e.target.value))}
            className="w-full"
          />
          <p className="text-xs text-gray-500 mt-1">
            Images wider than this will be resized
          </p>
        </div>
      </div>

      {/* 文件上传 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload Images
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileSelect}
          disabled={isProcessing}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
        />
        <p className="mt-2 text-sm text-gray-500">
          Select one or multiple images to compress
        </p>
      </div>

      {/* 重新压缩按钮 */}
      {images.length > 0 && (
        <button
          onClick={handleRecompress}
          disabled={isProcessing}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
        >
          {isProcessing ? 'Compressing...' : 'Recompress with New Settings'}
        </button>
      )}

      {/* 处理状态 */}
      {isProcessing && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          Compressing images... Please wait.
        </div>
      )}

      {/* 图片列表 */}
      {images.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700">
            Compressed Images ({images.length})
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
                      <p>
                        Original: {formatFileSize(image.originalSize)}
                      </p>
                      <p>
                        Compressed: {formatFileSize(image.compressedSize)} (
                        {getCompressionRatio(image.originalSize, image.compressedSize)}% smaller)
                      </p>
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
                <div className="mb-2">
                  <img
                    src={image.url}
                    alt={`Compressed ${image.original.name}`}
                    className="w-full h-32 object-contain bg-gray-50 rounded"
                  />
                </div>
                <button
                  onClick={() => handleDownload(image, index)}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
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
          <li>Adjust quality and max width settings</li>
          <li>Upload one or multiple images</li>
          <li>Images will be automatically compressed</li>
          <li>Preview and download compressed images</li>
          <li>Adjust settings and click "Recompress" if needed</li>
        </ol>
      </div>
    </div>
  )
}

