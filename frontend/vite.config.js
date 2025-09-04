import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  root: './src',
  base: '/static/frontend/',
  build: {
    outDir: '../../workshop/static/frontend',
    assetsDir: '',
    rollupOptions: {
      input: {
        'customer-home': './src/customer-home.jsx',
        'customer-dashboard': './src/customer-dashboard.jsx',
        'customer-add-bike': './src/customer-add-bike.jsx',
        'customer-bikes-list': './src/customer-bikes-list.jsx',
        'customer-approval': './src/customer-approval.jsx'
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].[hash].js',
        assetFileNames: '[name].[hash].[ext]'
      }
    },
    emptyOutDir: true
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
    hmr: {
      port: 3001
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})