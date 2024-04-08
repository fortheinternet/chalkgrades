/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
    fontFamily: {
      display: ['Inter', 'system-ui', 'sans-serif'],
      body: ['Inter', 'system-ui', 'sans-serif'],
    },
    colors: {
      'transparent-100': '#ffffff10',
      'transparent-250': '#ffffff25',
      'transparent-500': '#ffffff50',
      'transparent-750': '#ffffff75',
      'white': '#ffffff',
      'accent': '#d7e4dc',
      'enabled': '#7189ff',
      'disabled': '#5567c0',
      'border': '#1e1e1e',
      'background': '#232323',
      'background-2': '#2b2a2b'
    }
  },
  plugins: [],
}