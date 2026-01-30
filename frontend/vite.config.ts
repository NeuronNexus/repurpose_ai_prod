import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],server: {
    // Add this line to allow all hosts (including ngrok)
    allowedHosts: ['60a0b9519e79.ngrok-free.app'],
  },
})
