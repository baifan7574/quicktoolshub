import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Website Info */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-white text-xl font-bold mb-4">QuickToolsHub</h3>
            <p className="text-sm mb-4">
              Free online tools for PDF, Image, Text, and more. Quick & Easy Solutions.
            </p>
            <p className="text-xs text-gray-500">
              © 2024 QuickToolsHub. All rights reserved.
            </p>
          </div>

          {/* Important Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Important Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/about" className="hover:text-white transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-white transition-colors">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link href="/privacy-policy" className="hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms-of-service" className="hover:text-white transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/cookie-policy" className="hover:text-white transition-colors">
                  Cookie Policy
                </Link>
              </li>
              <li>
                <Link href="/disclaimer" className="hover:text-white transition-colors">
                  Disclaimer
                </Link>
              </li>
            </ul>
          </div>

          {/* Tool Categories */}
          <div>
            <h4 className="text-white font-semibold mb-4">Tool Categories</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/categories/pdf-tools" className="hover:text-white transition-colors">
                  PDF Tools
                </Link>
              </li>
              <li>
                <Link href="/categories/image-tools" className="hover:text-white transition-colors">
                  Image Tools
                </Link>
              </li>
              <li>
                <Link href="/categories/text-tools" className="hover:text-white transition-colors">
                  Text Tools
                </Link>
              </li>
              <li>
                <Link href="/categories/developer-tools" className="hover:text-white transition-colors">
                  Developer Tools
                </Link>
              </li>
              <li>
                <Link href="/tools" className="hover:text-white transition-colors">
                  All Tools
                </Link>
              </li>
              <li>
                <Link href="/blog" className="hover:text-white transition-colors">
                  Blog
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  )
}

