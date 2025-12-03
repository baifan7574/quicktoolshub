import Link from 'next/link'
import Image from 'next/image'
import { Tool } from '@/types'

interface ToolCardProps {
  tool: Tool
}

export default function ToolCard({ tool }: ToolCardProps) {
  return (
    <Link
      href={`/tools/${tool.slug}`}
      className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 hover:shadow-lg transition-shadow block min-h-[120px] touch-manipulation"
    >
      <div className="flex items-start space-x-3 sm:space-x-4">
        <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-lg flex items-center justify-center">
          {tool.icon_url ? (
            <Image 
              src={tool.icon_url} 
              alt={tool.name} 
              width={32} 
              height={32} 
              className="object-contain"
              loading="lazy"
            />
          ) : (
            <span className="text-xl sm:text-2xl">🔧</span>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-base sm:text-lg mb-1 truncate">{tool.name}</h3>
          <p className="text-gray-600 text-sm line-clamp-2 mb-3">
            {tool.short_description || tool.description}
          </p>
          <div className="flex items-center space-x-2 flex-wrap gap-1">
            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
              Free
            </span>
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
              Online
            </span>
            {tool.tool_type === 'self_developed' && (
              <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                Built-in
              </span>
            )}
            {tool.tool_type === 'external_link' && (
              <span className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">
                External
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  )
}

