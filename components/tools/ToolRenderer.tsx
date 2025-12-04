'use client'

import dynamic from 'next/dynamic'
import { Tool } from '@/types'

// 加载中组件
const LoadingComponent = () => (
  <div className="flex items-center justify-center py-12">
    <div className="text-center">
      <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
      <p className="text-gray-600">Loading tool...</p>
    </div>
  </div>
)

// 动态导入工具组件（按需加载）
const toolComponents: Record<string, React.ComponentType> = {
  'word-counter': dynamic(() => import('./WordCounterTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'text-case-converter': dynamic(() => import('./TextCaseConverterTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'lorem-ipsum-generator': dynamic(() => import('./LoremIpsumGeneratorTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'json-formatter': dynamic(() => import('./JSONFormatterTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'base64-encoder': dynamic(() => import('./Base64EncoderTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'url-encoder': dynamic(() => import('./URLEncoderTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'pdf-merger': dynamic(() => import('./PDFMergerTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'pdf-splitter': dynamic(() => import('./PDFSplitterTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'pdf-compressor': dynamic(() => import('./PDFCompressorTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'image-compressor': dynamic(() => import('./ImageCompressorTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'image-resizer': dynamic(() => import('./ImageResizerTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'image-converter': dynamic(() => import('./ImageConverterTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'background-remover': dynamic(() => import('./BackgroundRemoverTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
  'pdf-to-word': dynamic(() => import('./PDFToWordTool'), { 
    ssr: false,
    loading: () => <LoadingComponent />
  }),
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

