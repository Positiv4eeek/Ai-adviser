<template>
  <div>
    <nav class="p-4 flex justify-center items-center space-x-4">
      <img src="/narxoz-logo.svg" alt="Narxoz Logo" class="h-10 w-auto" />

      <router-link to="/" class="text-blue-600 hover:underline">{{ $t('nav.home') }}</router-link>

      <template v-if="isAuthenticated">
        <router-link to="/dashboard" class="text-blue-600 hover:underline">{{ $t('nav.dashboard') }}</router-link>
        <router-link v-if="isAdmin" to="/admin" class="text-blue-600 hover:underline">{{ $t('nav.admin_panel') }}</router-link>
        <a
          href="#"
          @click.prevent="logout"
          class="text-red-600 hover:text-red-800 transition-colors duration-150"
        >
          {{ $t('nav.logout') }}
        </a>
      </template>

      <template v-else>
        <router-link to="/login" class="text-blue-600 hover:underline">{{ $t('nav.login') }}</router-link>
        <router-link to="/register" class="text-blue-600 hover:underline">{{ $t('nav.register') }}</router-link>
      </template>

      <select
        v-model="locale"
        class="w-16 bg-white text-blue-600 dark:bg-zinc-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-zinc-700"
      >
        <option value="kz">KZ</option>
        <option value="ru">RU</option>
        <option value="en">EN</option>
      </select>
    </nav>

    <router-view />
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import axios from 'axios'

const { locale } = useI18n()
locale.value = localStorage.getItem('locale') || locale.value
watch(locale, (val) => {
  localStorage.setItem('locale', val)
})

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const isAdmin = computed(() => {
  try {
    const user = JSON.parse(localStorage.getItem('user'))
    return user?.role === 'admin'
  } catch {
    return false
  }
})

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  delete axios.defaults.headers.common['Authorization']
  window.location.reload()
  router.push('/login')
}
</script>

<style scoped>
select:focus {
  outline: none;
}
</style>
