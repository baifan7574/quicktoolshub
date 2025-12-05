'use client'

import { useState } from 'react'
import { MagnifyingGlassIcon, ChartBarIcon } from '@heroicons/react/24/outline'

export default function SEOAdminPage() {
  const [keyword, setKeyword] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [searchType, setSearchType] = useState('all')

  const handleSearch = async () => {
    if (!keyword.trim()) return

    setLoading(true)
    try {
      const response = await fetch(
        `/api/seo/keywords?keyword=${encodeURIComponent(keyword)}&type=${searchType}`
      )
      if (response.ok) {
        const data = await response.json()
        setResults(data)
      }
    } catch (error) {
      console.error('Failed to search keywords:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">SEO 关键词分析</h1>
          <p className="mt-2 text-gray-600">
            分析关键词在网站中的使用情况和流量潜力
          </p>
        </div>

        {/* 搜索框 */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="输入关键词，例如：PDF merger, image compressor..."
                className="w-full border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              />
            </div>
            <div>
              <select
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
                className="border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] touch-manipulation"
              >
                <option value="all">全部</option>
                <option value="tools">工具</option>
                <option value="articles">文章</option>
              </select>
            </div>
            <button
              onClick={handleSearch}
              disabled={loading || !keyword.trim()}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 min-h-[44px] touch-manipulation flex items-center justify-center gap-2"
            >
              <MagnifyingGlassIcon className="h-5 w-5" />
              {loading ? '分析中...' : '分析关键词'}
            </button>
          </div>
        </div>

        {/* 结果展示 */}
        {results && (
          <div className="space-y-6">
            {/* 匹配结果 */}
            {results.matches && results.matches.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  网站中的匹配内容 ({results.matches.length})
                </h2>
                <div className="space-y-4">
                  {results.matches.map((match: any, index: number) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span
                              className={`px-2 py-1 text-xs font-semibold rounded ${
                                match.type === 'tool'
                                  ? 'bg-blue-100 text-blue-800'
                                  : 'bg-green-100 text-green-800'
                              }`}
                            >
                              {match.type === 'tool' ? '工具' : '文章'}
                            </span>
                            <a
                              href={match.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:text-blue-800 font-medium"
                            >
                              {match.title}
                            </a>
                          </div>
                          {match.description && (
                            <p className="text-sm text-gray-600 mb-2">
                              {match.description}
                            </p>
                          )}
                          {match.metrics && (
                            <div className="flex items-center gap-4 text-xs text-gray-500">
                              {match.metrics.views !== undefined && (
                                <span>浏览量: {match.metrics.views}</span>
                              )}
                              {match.metrics.uses !== undefined && (
                                <span>使用次数: {match.metrics.uses}</span>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 关键词建议 */}
            {results.suggestions && results.suggestions.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  长尾关键词建议
                </h2>
                <div className="flex flex-wrap gap-2">
                  {results.suggestions.map((suggestion: string, index: number) => (
                    <button
                      key={index}
                      onClick={() => {
                        setKeyword(suggestion)
                        setTimeout(() => handleSearch(), 100)
                      }}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm min-h-[44px] touch-manipulation"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
                <p className="mt-4 text-sm text-gray-600">
                  💡 提示：点击关键词建议可以快速分析该关键词
                </p>
              </div>
            )}

            {/* 无结果提示 */}
            {results.matches && results.matches.length === 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                <p className="text-yellow-800">
                  ⚠️ 未找到匹配的内容。建议：
                </p>
                <ul className="mt-2 text-sm text-yellow-700 list-disc list-inside space-y-1">
                  <li>创建包含此关键词的新文章</li>
                  <li>在现有工具页面中添加此关键词</li>
                  <li>使用长尾关键词建议创建内容</li>
                </ul>
              </div>
            )}
          </div>
        )}

        {/* 使用说明 */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">
            📊 如何使用关键词分析
          </h3>
          <ul className="text-sm text-blue-800 space-y-2">
            <li>
              <strong>1. 输入关键词：</strong>
              输入您想分析的关键词（例如："PDF merger"）
            </li>
            <li>
              <strong>2. 查看匹配结果：</strong>
              查看网站中哪些页面使用了这个关键词
            </li>
            <li>
              <strong>3. 查看流量数据：</strong>
              查看这些页面的浏览量和使用次数（需要集成 Google Analytics）
            </li>
            <li>
              <strong>4. 使用关键词建议：</strong>
              使用长尾关键词建议创建新内容
            </li>
          </ul>
        </div>

        {/* Google Search Console 集成提示 */}
        <div className="mt-6 bg-gray-100 border border-gray-300 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            🔍 获取真实搜索流量数据
          </h3>
          <p className="text-sm text-gray-700 mb-3">
            要查看关键词的真实搜索流量，需要集成 Google Search Console API：
          </p>
          <ul className="text-sm text-gray-700 space-y-2 list-disc list-inside">
            <li>在 Google Search Console 中验证网站</li>
            <li>获取 API 凭证</li>
            <li>查看每个关键词的搜索次数、点击率、排名</li>
            <li>识别高流量、低竞争的关键词</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

