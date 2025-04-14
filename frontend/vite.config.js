import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // Add these critical production settings:
  base: '/',  // Ensures assets are loaded from root
  build: {
    outDir: '../backend/static',  // Build directly into Flask's static folder
    emptyOutDir: true,  // Cleans the directory before build
    assetsDir: 'assets'  // Organized asset directory
  }
})