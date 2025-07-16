<template>
  <div class="p-8 max-w-sm mx-auto">
    <h2 class="text-2xl mb-4">{{ $t('nav.login') }}</h2>
    <form @submit.prevent="submit">
      <input
        v-model="email"
        type="email"
        :placeholder="$t('login.email')"
        required
        class="block mb-2 p-2 border rounded w-full"
      />
      <input
        v-model="password"
        type="password"
        :placeholder="$t('login.password')"
        required
        class="block mb-4 p-2 border rounded w-full"
      />
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center items-center px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 disabled:opacity-50"
      >
        <span v-if="!loading">{{ $t('login.submit') }}</span>
        <span v-else>{{ $t('login.loading') }}</span>
      </button>
    </form>

    <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.append('username', email.value)
    params.append('password', password.value)

    const res = await axios.post('/auth/token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    localStorage.setItem('token', res.data.access_token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`

    const userRes = await axios.get('/auth/me')
    localStorage.setItem('user', JSON.stringify(userRes.data))

    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || t('login.error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>

</style>
