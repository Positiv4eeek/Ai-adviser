import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/auth': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/me': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/upload-transcript': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/upload-curriculum': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    }
  }
})
