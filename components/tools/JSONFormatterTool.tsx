'use client'

import { useState } from 'react'

export default function JSONFormatterTool() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [indent, setIndent] = useState(2)

  const formatJSON = () => {
    setError('')
    if (!input.trim()) {
      setOutput('')
      return
    }

    try {
      const parsed = JSON.parse(input)
      const formatted = JSON.stringify(parsed, null, indent)
      setOutput(formatted)
    } catch (e: any) {
      setError(e.message || 'Invalid JSON')
      setOutput('')
    }
  }

  const validateJSON = () => {
    setError('')
    if (!input.trim()) {
      setError('Please enter JSON to validate')
      return
    }

    try {
      JSON.parse(input)
      setError('')
      alert('✅ Valid JSON!')
    } catch (e: any) {
      setError(`❌ Invalid JSON: ${e.message}`)
    }
  }

  const minifyJSON = () => {
    setError('')
    if (!input.trim()) {
      setOutput('')
      return
    }

    try {
      const parsed = JSON.parse(input)
      const minified = JSON.stringify(parsed)
      setOutput(minified)
    } catch (e: any) {
      setError(e.message || 'Invalid JSON')
      setOutput('')
    }
  }

  const handleCopy = () => {
    if (output) {
      navigator.clipboard.writeText(output)
      alert('JSON copied to clipboard!')
    }
  }

  const handleClear = () => {
    setInput('')
    setOutput('')
    setError('')
  }

  return (
    <div className="space-y-6">
      {/* 操作按钮 */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={formatJSON}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
        >
          Format JSON
        </button>
        <button
          onClick={minifyJSON}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
        >
          Minify JSON
        </button>
        <button
          onClick={validateJSON}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm"
        >
          Validate JSON
        </button>
        <button
          onClick={handleClear}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
        >
          Clear
        </button>
      </div>

      {/* 缩进设置 */}
      <div className="flex items-center space-x-4">
        <label htmlFor="indent" className="text-sm font-medium text-gray-700">
          Indentation:
        </label>
        <select
          id="indent"
          value={indent}
          onChange={(e) => setIndent(Number(e.target.value))}
          className="px-3 py-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value={2}>2 spaces</option>
          <option value={4}>4 spaces</option>
          <option value={0}>No indent</option>
        </select>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {/* 输入区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="json-input" className="text-sm font-medium text-gray-700">
            Input JSON
          </label>
          <span className="text-xs text-gray-500">
            {input.length} characters
          </span>
        </div>
        <textarea
          id="json-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Paste your JSON here, e.g., {"name": "John", "age": 30}'
          className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
        />
      </div>

      {/* 输出区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="json-output" className="text-sm font-medium text-gray-700">
            Formatted JSON
          </label>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">
              {output.length} characters
            </span>
            <button
              onClick={handleCopy}
              disabled={!output}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
            >
              Copy
            </button>
          </div>
        </div>
        <textarea
          id="json-output"
          value={output}
          readOnly
          className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 resize-none font-mono text-sm"
        />
      </div>
    </div>
  )
}

