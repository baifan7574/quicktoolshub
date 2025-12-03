'use client'

import { useState } from 'react'

export default function URLEncoderTool() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [mode, setMode] = useState<'encode' | 'decode'>('encode')

  const handleEncode = () => {
    try {
      const encoded = encodeURIComponent(input)
      setOutput(encoded)
    } catch (e) {
      setOutput('Error encoding URL')
    }
  }

  const handleDecode = () => {
    try {
      const decoded = decodeURIComponent(input)
      setOutput(decoded)
    } catch (e) {
      setOutput('Error decoding URL. Please check if the input is valid URL-encoded text.')
    }
  }

  const handleConvert = () => {
    if (mode === 'encode') {
      handleEncode()
    } else {
      handleDecode()
    }
  }

  const handleCopy = () => {
    if (output) {
      navigator.clipboard.writeText(output)
      alert('Text copied to clipboard!')
    }
  }

  const handleClear = () => {
    setInput('')
    setOutput('')
  }

  return (
    <div className="space-y-6">
      {/* 模式选择 */}
      <div>
        <label htmlFor="mode" className="block text-sm font-medium text-gray-700 mb-2">
          Mode:
        </label>
        <div className="flex space-x-4">
          <label className="flex items-center">
            <input
              type="radio"
              name="mode"
              value="encode"
              checked={mode === 'encode'}
              onChange={(e) => setMode(e.target.value as 'encode' | 'decode')}
              className="mr-2"
            />
            <span>Encode (Text → URL)</span>
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              name="mode"
              value="decode"
              checked={mode === 'decode'}
              onChange={(e) => setMode(e.target.value as 'encode' | 'decode')}
              className="mr-2"
            />
            <span>Decode (URL → Text)</span>
          </label>
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="flex gap-3">
        <button
          onClick={handleConvert}
          className="px-4 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-base sm:text-sm font-semibold min-h-[44px] touch-manipulation"
        >
          {mode === 'encode' ? 'Encode' : 'Decode'}
        </button>
        <button
          onClick={handleClear}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
        >
          Clear
        </button>
      </div>

      {/* 输入区域 */}
      <div>
        <label htmlFor="url-input" className="block text-sm font-medium text-gray-700 mb-2">
          {mode === 'encode' ? 'Input Text' : 'Input URL-encoded Text'}
        </label>
        <textarea
          id="url-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={mode === 'encode' ? 'Enter text to encode...' : 'Enter URL-encoded text to decode...'}
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-base sm:text-sm min-h-[120px] touch-manipulation"
        />
      </div>

      {/* 输出区域 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label htmlFor="url-output" className="text-sm font-medium text-gray-700">
            {mode === 'encode' ? 'URL-encoded Output' : 'Decoded Text'}
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
          id="url-output"
          value={output}
          readOnly
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 resize-none font-mono text-sm"
        />
      </div>
    </div>
  )
}

