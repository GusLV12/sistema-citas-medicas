import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'

const apiProxyTarget = process.env.API_PROXY_TARGET ?? 'http://localhost:8000'
const allowedHosts = process.env.VITE_ALLOWED_HOSTS?.split(',').map((host) => host.trim()).filter(Boolean) ?? []

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(import.meta.dirname, 'src') } },
  server: { allowedHosts, proxy: { '/api': { target: apiProxyTarget, changeOrigin: true } } },
  test: {
    environment: 'jsdom',
    env: { VITE_USE_MOCKS: 'true' },
    setupFiles: ['./src/test/setup.ts'],
    css: true,
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
  },
})
