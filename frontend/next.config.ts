import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  // Allow cross-origin requests from Replit domains
  allowedDevOrigins: [
    "*.replit.dev",
    "*.repl.co",
  ],
};

export default nextConfig;
