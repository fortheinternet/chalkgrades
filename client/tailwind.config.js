/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'selector',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    fontFamily: {
      display: ['Inter', 'system-ui', 'sans-serif'],
      body: ['Inter', 'system-ui', 'sans-serif'],
    },
    fontSize: {
      '7xl': '2.986rem', // h1
      '6xl': '2.488rem', // h2
      '5xl': '2.074rem', // h3
      '4xl': '1.728rem', // h4
      '3xl': '1.44rem',  // h5
      '2xl': '1.2rem',   // h6
      'base': '1rem',    // p
      'small': '0.833rem', // small
      'smaller': '0.694rem', // smaller
    },
    colors: {
      "white": "#ffffff",
      "black": "#000000",
      "dark-grey": '#131315',
      "darker-grey": '#111112',
      "light-grey": "#EFEFEF",
      "lighter-grey": "#E6E6E6"
    }
  },
  plugins: [],
}