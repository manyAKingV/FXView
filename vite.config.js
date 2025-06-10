import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import yaml from '@vitejs/plugin-yaml';
export default defineConfig({
  plugins: [vue(),yaml()],
   build: {
    outDir: 'dist'
  },
});