'use client'

import { useState } from 'react'

const loremWords = [
  'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
  'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
  'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
  'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
  'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate', 'velit',
  'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat',
  'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia', 'deserunt',
  'mollit', 'anim', 'id', 'est', 'laborum'
]

export default function LoremIpsumGeneratorTool() {
  const [count, setCount] = useState(5)
  const [type, setType] = useState<'words' | 'sentences' | 'paragraphs'>('paragraphs')
  const [output, setOutput] = useState('')

  const generateWords = (num: number): string => {
    const words: string[] = []
    for (let i = 0; i < num; i++) {
      words.push(loremWords[i % loremWords.length])
    }
    return words.join(' ')
  }

  const generateSentence = (): string => {
    const wordCount = Math.floor(Math.random() * 10) + 5 // 5-15 words
    const words = generateWords(wordCount)
    return words.charAt(0).toUpperCase() + words.slice(1) + '.'
  }

  const generateParagraph = (): string => {
    const sentenceCount = Math.floor(Math.random() * 3) + 3 // 3-5 sentences
    const sentences: string[] = []
    for (let i = 0; i < sentenceCount; i++) {
      sentences.push(generateSentence())
    }
    return sentences.join(' ')
  }

  const generate = () => {
    let result = ''

    if (type === 'words') {
      result = generateWords(count)
    } else if (type === 'sentences') {
      const sentences: string[] = []
      for (let i = 0; i < count; i++) {
        sentences.push(generateSentence())
      }
      result = sentences.join(' ')
    } else if (type === 'paragraphs') {
      const paragraphs: string[] = []
      for (let i = 0; i < count; i++) {
        paragraphs.push(generateParagraph())
      }
      result = paragraphs.join('\n\n')
    }

    setOutput(result)
  }

  const handleCopy = () => {
    if (output) {
      navigator.clipboard.writeText(output)
      alert('Text copied to clipboard!')
    }
  }

  const handleClear = () => {
    setOutput('')
  }

  return (
    <div className="space-y-6">
      {/* 生成选项 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-2">
            Generate:
          </label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value as 'words' | 'sentences' | 'paragraphs')}
            className="w-full px-4 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-base sm:text-sm min-h-[44px] touch-manipulation"
          >
            <option value="words">Words</option>
            <option value="sentences">Sentences</option>
            <option value="paragraphs">Paragraphs</option>
          </select>
        </div>
        <div>
          <label htmlFor="count" className="block text-sm font-medium text-gray-700 mb-2">
            Count:
          </label>
          <input
            id="count"
            type="number"
            min="1"
            max={type === 'words' ? 1000 : type === 'sentences' ? 100 : 50}
            value={count}
            onChange={(e) => setCount(Number(e.target.value))}
            className="w-full px-4 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-base sm:text-sm min-h-[44px] touch-manipulation"
          />
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="flex gap-3">
        <button
          onClick={generate}
          className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
        >
          Generate Lorem Ipsum
        </button>
        <button
          onClick={handleClear}
          className="px-4 py-3 sm:py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
        >
          Clear
        </button>
      </div>

      {/* 输出区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="lorem-output" className="text-sm font-medium text-gray-700">
            Generated Text
          </label>
          <button
            onClick={handleCopy}
            disabled={!output}
            className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
          >
            Copy
          </button>
        </div>
        <textarea
          id="lorem-output"
          value={output}
          readOnly
          className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 resize-none text-base sm:text-sm min-h-[200px] touch-manipulation"
        />
      </div>
    </div>
  )
}

