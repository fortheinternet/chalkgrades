/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
    fontFamily: {
      display: ['Inter', 'system-ui', 'sans-serif'],
      body: ['Inter', 'system-ui', 'sans-serif'],
      navigation: ['monospace'],
    },
    colors: {
      'transparent-100': '#ffffff10',
      'transparent-250': '#ffffff25',
      'transparent-500': '#ffffff50',
      'transparent-750': '#ffffff75',
      'accent': '#d7e4dc',
      'enabled': '#7189ff',
      'disabled': '#5567c0',
      'border': '#0C0A09',
      'background': '#09090b'
    }
  },
  plugins: [],
}