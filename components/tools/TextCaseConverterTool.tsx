'use client'

import { useState } from 'react'

type CaseType = 'lowercase' | 'uppercase' | 'title' | 'sentence' | 'camel' | 'pascal' | 'snake' | 'kebab'

export default function TextCaseConverterTool() {
  const [text, setText] = useState('')
  const [caseType, setCaseType] = useState<CaseType>('lowercase')

  const convertText = (input: string, type: CaseType): string => {
    if (!input) return ''

    switch (type) {
      case 'lowercase':
        return input.toLowerCase()
      case 'uppercase':
        return input.toUpperCase()
      case 'title':
        return input
          .toLowerCase()
          .split(' ')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ')
      case 'sentence':
        return input
          .toLowerCase()
          .split(/[.!?]+\s*/)
          .map(sentence => sentence.trim().charAt(0).toUpperCase() + sentence.trim().slice(1))
          .join('. ')
      case 'camel':
        return input
          .toLowerCase()
          .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase())
      case 'pascal':
        const camel = convertText(input, 'camel')
        return camel.charAt(0).toUpperCase() + camel.slice(1)
      case 'snake':
        return input
          .toLowerCase()
          .replace(/[^a-zA-Z0-9]+/g, '_')
          .replace(/^_|_$/g, '')
      case 'kebab':
        return input
          .toLowerCase()
          .replace(/[^a-zA-Z0-9]+/g, '-')
          .replace(/^-|-$/g, '')
      default:
        return input
    }
  }

  const convertedText = convertText(text, caseType)

  const handleCopy = () => {
    navigator.clipboard.writeText(convertedText)
    alert('Text copied to clipboard!')
  }

  const handleClear = () => {
    setText('')
  }

  return (
    <div className="space-y-6">
      {/* 转换选项 */}
      <div>
        <label htmlFor="case-type" className="block text-sm font-medium text-gray-700 mb-2">
          Convert to:
        </label>
        <select
          id="case-type"
          value={caseType}
          onChange={(e) => setCaseType(e.target.value as CaseType)}
          className="w-full px-4 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-base sm:text-sm min-h-[44px] touch-manipulation"
        >
          <option value="lowercase">lowercase</option>
          <option value="uppercase">UPPERCASE</option>
          <option value="title">Title Case</option>
          <option value="sentence">Sentence case</option>
          <option value="camel">camelCase</option>
          <option value="pascal">PascalCase</option>
          <option value="snake">snake_case</option>
          <option value="kebab">kebab-case</option>
        </select>
      </div>

      {/* 输入区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="input-text" className="text-sm font-medium text-gray-700">
            Input Text
          </label>
          <button
            onClick={handleClear}
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors min-h-[36px] px-2 touch-manipulation"
          >
            Clear
          </button>
        </div>
        <textarea
          id="input-text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter or paste your text here..."
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-base sm:text-sm min-h-[120px] touch-manipulation"
        />
      </div>

      {/* 输出区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="output-text" className="text-sm font-medium text-gray-700">
            Converted Text
          </label>
          <button
            onClick={handleCopy}
            disabled={!convertedText}
            className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
          >
            Copy
          </button>
        </div>
        <textarea
          id="output-text"
          value={convertedText}
          readOnly
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 resize-none"
        />
      </div>
    </div>
  )
}

