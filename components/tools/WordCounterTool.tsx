'use client'

import { useState, useEffect } from 'react'

export default function WordCounterTool() {
  const [text, setText] = useState('')
  const [stats, setStats] = useState({
    words: 0,
    characters: 0,
    charactersNoSpaces: 0,
    paragraphs: 0,
    sentences: 0,
    lines: 0,
  })

  useEffect(() => {
    const calculateStats = () => {
      const trimmedText = text.trim()
      
      // Word count (split by whitespace and filter empty strings)
      const words = trimmedText ? trimmedText.split(/\s+/).filter(word => word.length > 0) : []
      
      // Character counts
      const characters = text.length
      const charactersNoSpaces = text.replace(/\s/g, '').length
      
      // Paragraph count (split by double newlines or single newline if text is short)
      const paragraphs = trimmedText ? trimmedText.split(/\n\s*\n/).filter(p => p.trim().length > 0).length || 1 : 0
      
      // Sentence count (split by . ! ? followed by space or end of string)
      const sentences = trimmedText ? trimmedText.split(/[.!?]+(\s|$)/).filter(s => s.trim().length > 0).length : 0
      
      // Line count
      const lines = text ? text.split('\n').length : 0
      
      setStats({
        words: words.length,
        characters,
        charactersNoSpaces,
        paragraphs,
        sentences: sentences || 1, // At least 1 sentence if there's text
        lines,
      })
    }

    calculateStats()
  }, [text])

  const handleClear = () => {
    setText('')
  }

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.words.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Words</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.characters.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Characters</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.charactersNoSpaces.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Characters (no spaces)</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.paragraphs.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Paragraphs</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.sentences.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Sentences</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.lines.toLocaleString()}</div>
          <div className="text-sm text-gray-600 mt-1">Lines</div>
        </div>
      </div>

      {/* 文本输入区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="text-input" className="text-sm font-medium text-gray-700">
            Enter or paste your text below
          </label>
          <button
            onClick={handleClear}
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Clear
          </button>
        </div>
        <textarea
          id="text-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Start typing or paste your text here..."
          className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
        />
        <div className="mt-2 text-sm text-gray-500">
          Tip: The statistics update automatically as you type
        </div>
      </div>
    </div>
  )
}

