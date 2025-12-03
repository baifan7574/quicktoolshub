'use client'

import {
  DocumentTextIcon,
  PhotoIcon,
  PencilSquareIcon,
  CodeBracketIcon,
  ArrowPathIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline'

interface CategoryIconProps {
  slug: string
  name: string
  className?: string
  size?: 'sm' | 'md' | 'lg'
}

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  'pdf-tools': DocumentTextIcon,
  'image-tools': PhotoIcon,
  'text-tools': PencilSquareIcon,
  'developer-tools': CodeBracketIcon,
  'converter-tools': ArrowPathIcon,
  'generator-tools': SparklesIcon,
}

const sizeMap = {
  sm: 'w-8 h-8',
  md: 'w-12 h-12',
  lg: 'w-16 h-16',
}

export default function CategoryIcon({ slug, name, className = '', size = 'md' }: CategoryIconProps) {
  const IconComponent = iconMap[slug] || DocumentTextIcon
  const sizeClass = sizeMap[size]

  return (
    <div className={`${sizeClass} ${className} flex items-center justify-center`}>
      <IconComponent className={`${sizeClass} text-blue-600`} aria-label={name} />
    </div>
  )
}

