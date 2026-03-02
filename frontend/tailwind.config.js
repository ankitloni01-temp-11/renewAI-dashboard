/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        suraksha: {
          blue: '#1B4F8A',
          gold: '#D4860B',
          light: '#E8F0F8'
        }
      }
    }
  },
  plugins: []
}
