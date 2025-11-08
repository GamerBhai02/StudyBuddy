import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  // Output standalone for optimal Vercel deployment
  output: 'standalone',
  // Allow cross-origin requests from Replit domains
  allowedDevOrigins: [
    "*.replit.dev",
    "*.repl.co",
  ],
};

export default nextConfig;
