'use client'

import dynamic from 'next/dynamic'
import { Tool } from '@/types'

// 动态导入工具组件（按需加载）
const toolComponents: Record<string, React.ComponentType> = {
  'word-counter': dynamic(() => import('./WordCounterTool'), { ssr: false }),
  'text-case-converter': dynamic(() => import('./TextCaseConverterTool'), { ssr: false }),
  'lorem-ipsum-generator': dynamic(() => import('./LoremIpsumGeneratorTool'), { ssr: false }),
  'json-formatter': dynamic(() => import('./JSONFormatterTool'), { ssr: false }),
  'base64-encoder': dynamic(() => import('./Base64EncoderTool'), { ssr: false }),
  'url-encoder': dynamic(() => import('./URLEncoderTool'), { ssr: false }),
  'pdf-merger': dynamic(() => import('./PDFMergerTool'), { ssr: false }),
  'pdf-splitter': dynamic(() => import('./PDFSplitterTool'), { ssr: false }),
  'pdf-compressor': dynamic(() => import('./PDFCompressorTool'), { ssr: false }),
  'image-compressor': dynamic(() => import('./ImageCompressorTool'), { ssr: false }),
  'image-resizer': dynamic(() => import('./ImageResizerTool'), { ssr: false }),
  'image-converter': dynamic(() => import('./ImageConverterTool'), { ssr: false }),
  'background-remover': dynamic(() => import('./BackgroundRemoverTool'), { ssr: false }),
  'pdf-to-word': dynamic(() => import('./PDFToWordTool'), { ssr: false }),
}

interface ToolRendererProps {
  tool: Tool
}

export default function ToolRenderer({ tool }: ToolRendererProps) {
  if (tool.tool_type === 'external_link') {
    return (
      <div>
        <h2 className="text-2xl font-semibold mb-4">About This Tool</h2>
        {tool.description && (
          <div className="prose max-w-none mb-6">
            <p className="text-gray-700">{tool.description}</p>
          </div>
        )}
        {tool.external_url && (
          <a
            href={tool.external_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Visit Tool →
          </a>
        )}
      </div>
    )
  }

  // 自开发工具：根据slug加载对应的工具组件
  const ToolComponent = toolComponents[tool.slug]

  if (ToolComponent) {
    return (
      <div>
        <h2 className="text-2xl font-semibold mb-4">Use This Tool</h2>
        <ToolComponent />
      </div>
    )
  }

  // 如果工具组件不存在，显示占位符
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Use This Tool</h2>
      <p className="text-gray-600 mb-4">
        This tool is under development. Please check back soon!
      </p>
      <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-12 text-center text-gray-400">
        <p>Tool Interface Coming Soon</p>
        <p className="text-sm mt-2">(Tool functionality will be implemented here)</p>
      </div>
    </div>
  )
}

