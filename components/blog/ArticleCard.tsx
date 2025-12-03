import Link from 'next/link'
import Image from 'next/image'
import { Article } from '@/types'
import { ClockIcon } from '@heroicons/react/24/outline'

interface ArticleCardProps {
  article: Article
}

export default function ArticleCard({ article }: ArticleCardProps) {
  return (
    <Link
      href={`/blog/${article.slug}`}
      className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow block"
    >
      <div className="flex flex-col sm:flex-row">
        {/* 文章缩略图 */}
        {article.featured_image ? (
          <div className="sm:w-48 sm:flex-shrink-0 h-48 sm:h-auto bg-gray-200 relative">
            <Image
              src={article.featured_image}
              alt={article.title}
              fill
              className="object-cover"
              loading="lazy"
            />
          </div>
        ) : (
          <div className="sm:w-48 sm:flex-shrink-0 h-48 sm:h-auto bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
            <span className="text-4xl">📄</span>
          </div>
        )}

        {/* 文章内容 */}
        <div className="flex-1 p-6">
          <h3 className="font-semibold text-xl mb-2 hover:text-blue-600 transition-colors">
            {article.title}
          </h3>
          {article.excerpt && (
            <p className="text-gray-600 mb-3 line-clamp-2">{article.excerpt}</p>
          )}
          <div className="flex items-center flex-wrap gap-3 text-sm text-gray-500">
            {article.reading_time && (
              <div className="flex items-center space-x-1">
                <ClockIcon className="h-4 w-4" />
                <span>{article.reading_time} min read</span>
              </div>
            )}
            {article.published_at && (
              <span>{new Date(article.published_at).toLocaleDateString()}</span>
            )}
            {article.category && (
              <span className="bg-gray-100 px-2 py-1 rounded text-gray-700">
                {article.category}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  )
}

