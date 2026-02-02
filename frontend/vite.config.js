import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            const auth = req.headers?.authorization || req.headers?.Authorization;
            if (auth) proxyReq.setHeader('Authorization', auth);
          });
        },
      },
    },
  },
})
