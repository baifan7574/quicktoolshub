// 自动部署测试 - 2024-12-XX (测试自动部署流程是否正常工作)
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";
import "./globals.css";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "QuickToolsHub - Free Online Tools",
    template: "%s | QuickToolsHub",
  },
  description: "Free online tools for PDF, Image, Text, and more. Quick & Easy Solutions.",
  keywords: ["free online tools", "PDF tools", "image tools", "text tools", "developer tools", "online utilities"],
  authors: [{ name: "QuickToolsHub" }],
  creator: "QuickToolsHub",
  publisher: "QuickToolsHub",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://soeasyhub.com'),
  openGraph: {
    type: "website",
    locale: "en_US",
    url: 'https://soeasyhub.com',
    siteName: "QuickToolsHub",
    title: "QuickToolsHub - Free Online Tools",
    description: "Free online tools for PDF, Image, Text, and more. Quick & Easy Solutions.",
  },
  twitter: {
    card: "summary_large_image",
    title: "QuickToolsHub - Free Online Tools",
    description: "Free online tools for PDF, Image, Text, and more. Quick & Easy Solutions.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'ywGUpboShDk141_-Lf1r2V6zyzAYVBwRnch6oTHO5yM',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        {/* Google Analytics */}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-N7EED2NH6J"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-N7EED2NH6J');
          `}
        </Script>
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}
      >
        <Header />
        <main className="flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
