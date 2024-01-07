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
      'cwhite': '#ffffff',
      'twhite': '#ffffff25',
      'twhite2': '#ffffff50',
      'twhite3': '#ffffff75',
      'cblack': '#000000',
      'dark-1': '#141312',
      'dark-1a': '#1c1710',
      'dark-1c': '#1f1d1b',
      'dark-2': '#101010',
      'accent-1': '#d7e4dc',
      'accent-2': '#c20002',
      'primary': '#155831',
      'enabled': '#7189ff',
      'disabled': '#5567c0',
      'success': '#25f87c',
      'warning': '#ff3d40',
    }
  },
  plugins: [],
}

