import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 禁用可能导致卡住的优化
  swcMinify: false,
  // 减少并发构建
  experimental: {
    workerThreads: false,
    cpus: 1,
  },
  // 禁用图片优化（减少构建时间）
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
