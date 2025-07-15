import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import axios from 'axios'
import { createI18n } from 'vue-i18n'
import messagesKZ from './locales/kz.js'
import messagesRU from './locales/ru.js'
import messagesEN from './locales/en.js'


axios.defaults.baseURL = import.meta.env.VITE_API_URL
const token = localStorage.getItem('token')
console.log('TOKEN:', token)
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const i18n = createI18n({
  legacy: false,             
  globalInjection: true,     
  locale: localStorage.getItem('locale') || 'ru',
  fallbackLocale: 'en',
  messages: {
    kz: messagesKZ,
    ru: messagesRU,
    en: messagesEN,
  },
})

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { faCheck, faMinus } from '@fortawesome/free-solid-svg-icons'
library.add(faCheck, faMinus)

const app = createApp(App)

app.component('FontAwesomeIcon', FontAwesomeIcon)

app.config.globalProperties.$axios = axios


app.use(router)
app.use(i18n)


app.mount('#app')
