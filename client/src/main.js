import './assets/main.css'

import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'

import messages_en from './locales/en_us.json'
import messages_hu from './locales/hu.json'

const savedLocale = localStorage.getItem('locale') || 'en_us'

const i18n = createI18n({
  locale: savedLocale,
  fallbackLocale: 'en_us',
  messages: {
    en_us: messages_en,
    hu: messages_hu
  }
})

// tailwind darkmode stuff
if (
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  document.documentElement.classList.add('dark')
} else {
  document.documentElement.classList.remove('dark')
}

const app = createApp(App)

app.use(i18n)
app.use(router)
app.mount('#app')
