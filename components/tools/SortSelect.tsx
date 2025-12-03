'use client'

import { useRouter, useSearchParams } from 'next/navigation'

interface SortSelectProps {
  currentSort: string
  categorySlug?: string
}

export default function SortSelect({ currentSort, categorySlug }: SortSelectProps) {
  const router = useRouter()
  const searchParams = useSearchParams()

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = e.target.value
    const params = new URLSearchParams(searchParams.toString())
    
    if (newSort) {
      params.set('sort', newSort)
    } else {
      params.delete('sort')
    }
    
    // 保持分类筛选
    if (categorySlug && categorySlug !== 'all') {
      params.set('category', categorySlug)
    }
    
    // 重置到第一页
    params.delete('page')
    
    router.push(`/tools?${params.toString()}`)
  }

  return (
    <div className="flex items-center space-x-2">
      <label className="text-sm text-gray-600">Sort by:</label>
      <select
        value={currentSort}
        onChange={handleSortChange}
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="popular">Most Popular</option>
        <option value="recent">Recently Added</option>
        <option value="alphabetical">Alphabetical</option>
        <option value="most-used">Most Used</option>
      </select>
    </div>
  )
}

