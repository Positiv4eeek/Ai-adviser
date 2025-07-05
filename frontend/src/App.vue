<template>
  <div>
    <nav class="p-4 flex justify-center items-center space-x-4">
      <img src="/narxoz-logo.svg" alt="Narxoz Logo" class="h-10 w-auto" />
  
      <router-link to="/" class="text-blue-600 hover:underline">{{ $t('nav.home') }}</router-link>
      <template v-if="!isAuthenticated">
        <router-link to="/login" class="text-blue-600 hover:underline">{{ $t('nav.login') }}</router-link>
        <router-link to="/register" class="text-blue-600 hover:underline">{{ $t('nav.register') }}</router-link>
      </template>
      <template v-else>
        <router-link to="/dashboard" class="text-blue-600 hover:underline">{{ $t('nav.dashboard') }}</router-link>
        <router-link
          to="/"
          @click.prevent="logout"
          class="text-red-600 hover:text-red-800 transition-colors duration-150"
        >
          {{ $t('nav.logout') }}
        </router-link>
        <select
        v-model="locale"
        class="w-16 bg-white text-blue-600 dark:bg-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="kz">KZ</option>
        <option value="ru">RU</option>
        <option value="en">EN</option>
      </select>
      </template>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'


const { locale } = useI18n()

locale.value = localStorage.getItem('locale') || locale.value

watch(locale, (val) => localStorage.setItem('locale', val))


const router = useRouter()
const route = useRoute()


const isAuthenticated = computed(() => {
  void route.fullPath
  return !!localStorage.getItem('token')
})

function logout() {
  localStorage.removeItem('token')
  delete axios.defaults.headers.common['Authorization']
  router.push('/login')
}
</script>

<style scoped>
select:focus {
  outline: none;
}
</style>
