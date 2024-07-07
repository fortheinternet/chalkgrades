/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'selector',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
    fontFamily: {
      display: ['Inter', 'system-ui', 'sans-serif'],
      body: ['Inter', 'system-ui', 'sans-serif']
    },
    fontSize: {
      '7xl': '2.986rem', // h1
      '6xl': '2.488rem', // h2
      '5xl': '2.074rem', // h3
      '4xl': '1.728rem', // h4
      '3xl': '1.44rem', // h5
      '2xl': '1.2rem', // h6
      base: '0.890rem', // p
      small: '0.833rem', // small
      smaller: '0.694rem' // smaller
    },
    colors: {
      white: '#ffffff',
      black: '#000000',
      'dark-grey': '#191919',
      'light-grey': '#EFEFEF',
      red: '#ef4444',
      green: '#84cc16',
      yellow: '#fbbf24'
    }
  },
  plugins: []
}
