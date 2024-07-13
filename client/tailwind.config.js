/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'selector',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
    fontFamily: {
      body: ['Poppins', 'system-ui', 'sans-serif']
    },
    fontSize: {
      '7xl': '2.986rem', // h1
      '6xl': '2.488rem', // h2
      '5xl': '2.074rem', // h3
      '4xl': '1.728rem', // h4
      '3xl': '1.44rem', // h5
      '2xl': '1.2rem', // h6
      base: '0.890rem', // p
      small: '0.850rem', // small
      smaller: '0.700rem' // smaller
    },
    colors: {
      white: '#ffffff',
      black: '#000000',
      'dark-grey': '#111111',
      'light-grey': '#FGFGFG',
      red: '#ef4444',
      green: '#84cc16',
      yellow: '#fbbf24'
    }
  },
  plugins: []
}
