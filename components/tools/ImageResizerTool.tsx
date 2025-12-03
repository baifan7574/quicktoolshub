'use client'

import { useState, useRef } from 'react'
import { ArrowDownTrayIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface ResizedImage {
  original: File
  resized: Blob
  originalWidth: number
  originalHeight: number
  newWidth: number
  newHeight: number
  url: string
}

export default function ImageResizerTool() {
  const [images, setImages] = useState<ResizedImage[]>([])
  const [width, setWidth] = useState(800)
  const [height, setHeight] = useState(600)
  const [maintainAspectRatio, setMaintainAspectRatio] = useState(true)
  const [isProcessing, setIsProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const resizeImage = (file: File): Promise<ResizedImage> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (e) => {
        const img = new Image()
        img.onload = () => {
          const originalWidth = img.width
          const originalHeight = img.height

          // 计算新尺寸
          let newWidth = width
          let newHeight = height

          if (maintainAspectRatio) {
            const aspectRatio = originalWidth / originalHeight
            if (width / height > aspectRatio) {
              // 以高度为准
              newWidth = Math.round(height * aspectRatio)
              newHeight = height
            } else {
              // 以宽度为准
              newWidth = width
              newHeight = Math.round(width / aspectRatio)
            }
          }

          // 创建canvas
          const canvas = document.createElement('canvas')
          canvas.width = newWidth
          canvas.height = newHeight
          const ctx = canvas.getContext('2d')
          
          if (!ctx) {
            reject(new Error('Failed to get canvas context'))
            return
          }

          // 绘制图片（使用高质量缩放）
          ctx.imageSmoothingEnabled = true
          ctx.imageSmoothingQuality = 'high'
          ctx.drawImage(img, 0, 0, newWidth, newHeight)

          // 转换为blob
          canvas.toBlob(
            (blob) => {
              if (!blob) {
                reject(new Error('Failed to resize image'))
                return
              }

              resolve({
                original: file,
                resized: blob,
                originalWidth,
                originalHeight,
                newWidth,
                newHeight,
                url: URL.createObjectURL(blob),
              })
            },
            file.type || 'image/jpeg',
            0.95
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
    const newImages: ResizedImage[] = []

    try {
      for (const file of imageFiles) {
        const resized = await resizeImage(file)
        newImages.push(resized)
      }
      setImages(prev => [...prev, ...newImages])
    } catch (error: any) {
      alert(`Error resizing images: ${error.message}`)
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

  const handleDownload = (image: ResizedImage, index: number) => {
    const a = document.createElement('a')
    a.href = image.url
    a.download = `resized-${image.original.name}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  const handleResize = async () => {
    if (images.length === 0) return

    setIsProcessing(true)
    const newImages: ResizedImage[] = []

    try {
      for (const image of images) {
        const resized = await resizeImage(image.original)
        // 释放旧的URL
        URL.revokeObjectURL(image.url)
        newImages.push(resized)
      }
      setImages(newImages)
    } catch (error: any) {
      alert(`Error resizing images: ${error.message}`)
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
      {/* 尺寸设置 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="width" className="block text-sm font-medium text-gray-700 mb-2">
            Width: {width}px
          </label>
          <input
            id="width"
            type="range"
            min="100"
            max="3840"
            step="10"
            value={width}
            onChange={(e) => setWidth(Number(e.target.value))}
            className="w-full h-10 sm:h-8 touch-manipulation"
          />
        </div>
        <div>
          <label htmlFor="height" className="block text-sm font-medium text-gray-700 mb-2">
            Height: {height}px
          </label>
          <input
            id="height"
            type="range"
            min="100"
            max="2160"
            step="10"
            value={height}
            onChange={(e) => setHeight(Number(e.target.value))}
            className="w-full h-10 sm:h-8 touch-manipulation"
          />
        </div>
      </div>

      {/* 保持宽高比选项 */}
      <div>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={maintainAspectRatio}
            onChange={(e) => setMaintainAspectRatio(e.target.checked)}
            className="mr-2"
          />
          <span className="text-sm text-gray-700">
            Maintain aspect ratio
          </span>
        </label>
        <p className="text-xs text-gray-500 mt-1">
          When enabled, images will keep their original proportions
        </p>
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
          className="block w-full text-base sm:text-sm text-gray-500 file:mr-4 file:py-3 sm:file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-base sm:file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50 file:min-h-[44px] touch-manipulation"
        />
        <p className="mt-2 text-sm text-gray-500">
          Select one or multiple images to resize
        </p>
      </div>

      {/* 重新调整大小按钮 */}
      {images.length > 0 && (
        <button
          onClick={handleResize}
          disabled={isProcessing}
          className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
        >
          {isProcessing ? 'Resizing...' : 'Resize with New Settings'}
        </button>
      )}

      {/* 处理状态 */}
      {isProcessing && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          Resizing images... Please wait.
        </div>
      )}

      {/* 图片列表 */}
      {images.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700">
            Resized Images ({images.length})
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
                        Original: {image.originalWidth} × {image.originalHeight}px
                      </p>
                      <p>
                        Resized: {image.newWidth} × {image.newHeight}px
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeImage(index)}
                    className="p-2 text-gray-400 hover:text-red-600 ml-2 min-w-[44px] min-h-[44px] flex items-center justify-center touch-manipulation"
                    title="Remove"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>
                <div className="mb-2">
                  <img
                    src={image.url}
                    alt={`Resized ${image.original.name}`}
                    className="w-full h-32 object-contain bg-gray-50 rounded"
                  />
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
          <li>Set the desired width and height</li>
          <li>Choose whether to maintain aspect ratio</li>
          <li>Upload one or multiple images</li>
          <li>Images will be automatically resized</li>
          <li>Preview and download resized images</li>
          <li>Adjust settings and click "Resize" if needed</li>
        </ol>
      </div>
    </div>
  )
}

