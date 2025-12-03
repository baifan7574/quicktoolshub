'use client'

import { useRouter, useSearchParams } from 'next/navigation'

interface ArticleSortSelectProps {
  currentSort: string
  category?: string
}

export default function ArticleSortSelect({ currentSort, category }: ArticleSortSelectProps) {
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
    if (category && category !== 'all') {
      params.set('category', category)
    }
    
    // 重置到第一页
    params.delete('page')
    
    router.push(`/blog?${params.toString()}`)
  }

  return (
    <div className="flex items-center space-x-2">
      <label className="text-sm text-gray-600">Sort by:</label>
      <select
        value={currentSort}
        onChange={handleSortChange}
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="latest">Latest</option>
        <option value="popular">Most Popular</option>
        <option value="viewed">Most Viewed</option>
      </select>
    </div>
  )
}

