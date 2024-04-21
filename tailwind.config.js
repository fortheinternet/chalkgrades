/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  darkMode: 'selector',
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
      'transparent-black-100': '#00000010',
      'transparent-black-250': '#00000025',
      'transparent-black-500': '#00000050',
      'transparent-black-750': '#00000075',
      'white': '#ffffff',
      'black': '#000000',
      'accent': '#d7e4dc',
      'enabled': '#7189ff',
      'disabled': '#5567c0',
      'error': '#FF3D40',
      'border': '#1e1e1e',
      'background': '#1a1818',
      'background-2': '#1E1C1C',
      'background-light': '#F4F4F4',
      'background-light-2': '#E9E9E9'
    }
  },
  plugins: [],
}