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
    // Enable source maps for debugging
    sourcemap: true,
    // Optimize build (using esbuild for now, faster than terser)
    minify: 'esbuild',
    rollupOptions: {
      input: {
        // Customer pages (existing)
        'customer-home': './src/customer-home.jsx',
        'customer-dashboard': './src/customer-dashboard.jsx',
        'customer-add-bike': './src/customer-add-bike.jsx',
        'customer-bikes-list': './src/customer-bikes-list.jsx',
        'customer-approval': './src/customer-approval.jsx',
        'customer-report': './src/pages/customer/ReportForm.jsx',
        // Manager pages (Phase 1)
        'manager-dashboard': './src/pages/manager/Dashboard.jsx',
        'repair-form': './src/pages/manager/RepairForm.jsx',
        // Mechanic pages (Phase 1)
        'mechanic-dashboard': './src/pages/mechanic/Dashboard.jsx',
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].[hash].js',
        assetFileNames: '[name].[hash].[ext]',
        // Manual chunks for better code splitting
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          // Add more vendor chunks as we install dependencies
          // 'react-query-vendor': ['react-query'],
          // 'router-vendor': ['react-router-dom'],
        }
      }
    },
    emptyOutDir: true,
    // Increase chunk size warning limit
    chunkSizeWarningLimit: 1000,
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
    hmr: {
      port: 3001
    },
    // Proxy API requests to Django backend
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@api': path.resolve(__dirname, './src/api'),
      '@utils': path.resolve(__dirname, './src/utils'),
    }
  },
  // Optimize dependencies
  optimizeDeps: {
    include: ['react', 'react-dom'],
  }
})