'use client'

interface ShareButtonsProps {
  url: string
  title: string
}

export default function ShareButtons({ url, title }: ShareButtonsProps) {
  const handleCopyLink = () => {
    navigator.clipboard.writeText(url)
    alert('Link copied to clipboard!')
  }

  return (
    <div className="flex flex-wrap gap-3">
      <a
        href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
      >
        Facebook
      </a>
      <a
        href={`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-sky-500 text-white px-4 py-2 rounded-lg hover:bg-sky-600 transition-colors text-sm"
      >
        Twitter
      </a>
      <a
        href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition-colors text-sm"
      >
        LinkedIn
      </a>
      <button
        onClick={handleCopyLink}
        className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm"
      >
        Copy Link
      </button>
    </div>
  )
}

