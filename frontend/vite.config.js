import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react' // Fixed the path here
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
    strictPort: true,
    // Add CORS settings so Django can talk to Vite during dev
    cors: true, 
  }
})