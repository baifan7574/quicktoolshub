import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // 禁用 Turbopack（使用传统 Webpack）
  experimental: {
    turbo: false,
  },
};

export default nextConfig;
