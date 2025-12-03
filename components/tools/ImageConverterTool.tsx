'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface ConvertedImage {
  original: File
  converted: Blob
  format: string
  url: string
}

const supportedFormats = [
  { value: 'image/jpeg', label: 'JPEG', extension: 'jpg' },
  { value: 'image/png', label: 'PNG', extension: 'png' },
  { value: 'image/webp', label: 'WebP', extension: 'webp' },
  { value: 'image/gif', label: 'GIF', extension: 'gif' },
]

export default function ImageConverterTool() {
  const [images, setImages] = useState<ConvertedImage[]>([])
  const [targetFormat, setTargetFormat] = useState('image/jpeg')
  const [quality, setQuality] = useState(0.9)
  const [isProcessing, setIsProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const convertImage = (file: File, format: string): Promise<ConvertedImage> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (e) => {
        const img = new Image()
        img.onload = () => {
          // 创建canvas
          const canvas = document.createElement('canvas')
          canvas.width = img.width
          canvas.height = img.height
          const ctx = canvas.getContext('2d')
          
          if (!ctx) {
            reject(new Error('Failed to get canvas context'))
            return
          }

          // 绘制图片
          ctx.drawImage(img, 0, 0)

          // 转换为目标格式
          canvas.toBlob(
            (blob) => {
              if (!blob) {
                reject(new Error('Failed to convert image'))
                return
              }

              resolve({
                original: file,
                converted: blob,
                format,
                url: URL.createObjectURL(blob),
              })
            },
            format,
            format === 'image/jpeg' || format === 'image/webp' ? quality : undefined
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
    const newImages: ConvertedImage[] = []

    try {
      for (const file of imageFiles) {
        const converted = await convertImage(file, targetFormat)
        newImages.push(converted)
      }
      setImages(prev => [...prev, ...newImages])
    } catch (error: any) {
      alert(`Error converting images: ${error.message}`)
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

  const handleDownload = (image: ConvertedImage, index: number) => {
    const format = supportedFormats.find(f => f.value === image.format)
    const extension = format?.extension || 'jpg'
    const originalName = image.original.name.replace(/\.[^/.]+$/, '')
    
    const a = document.createElement('a')
    a.href = image.url
    a.download = `${originalName}.${extension}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  const handleReconvert = async () => {
    if (images.length === 0) return

    setIsProcessing(true)
    const newImages: ConvertedImage[] = []

    try {
      for (const image of images) {
        const converted = await convertImage(image.original, targetFormat)
        // 释放旧的URL
        URL.revokeObjectURL(image.url)
        newImages.push(converted)
      }
      setImages(newImages)
    } catch (error: any) {
      alert(`Error reconverting images: ${error.message}`)
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

  return (
    <div className="space-y-6">
      {/* 转换设置 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="target-format" className="block text-sm font-medium text-gray-700 mb-2">
            Convert to:
          </label>
          <select
            id="target-format"
            value={targetFormat}
            onChange={(e) => setTargetFormat(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {supportedFormats.map(format => (
              <option key={format.value} value={format.value}>
                {format.label}
              </option>
            ))}
          </select>
        </div>
        {(targetFormat === 'image/jpeg' || targetFormat === 'image/webp') && (
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
          </div>
        )}
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
          Select one or multiple images to convert
        </p>
      </div>

      {/* 重新转换按钮 */}
      {images.length > 0 && (
        <button
          onClick={handleReconvert}
          disabled={isProcessing}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
        >
          {isProcessing ? 'Converting...' : 'Reconvert with New Settings'}
        </button>
      )}

      {/* 处理状态 */}
      {isProcessing && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          Converting images... Please wait.
        </div>
      )}

      {/* 图片列表 */}
      {images.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700">
            Converted Images ({images.length})
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
                        Original: {image.original.type} ({formatFileSize(image.original.size)})
                      </p>
                      <p>
                        Converted: {image.format} ({formatFileSize(image.converted.size)})
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
                    alt={`Converted ${image.original.name}`}
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
          <li>Select the target format (JPEG, PNG, WebP, or GIF)</li>
          <li>Adjust quality if converting to JPEG or WebP</li>
          <li>Upload one or multiple images</li>
          <li>Images will be automatically converted</li>
          <li>Preview and download converted images</li>
        </ol>
        <p className="text-xs text-blue-700 mt-2">
          Supported formats: JPEG, PNG, WebP, GIF
        </p>
      </div>
    </div>
  )
}
