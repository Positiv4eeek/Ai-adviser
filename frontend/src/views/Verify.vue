<template>
  <div class="p-8 max-w-sm mx-auto">
    <h2 class="text-2xl mb-4">{{ t('nav.verify') }}</h2>
    <form @submit.prevent="submit">
      <input
        v-model="email"
        type="email"
        :placeholder="t('verify.email')"
        required
        class="block mb-2 p-2 border rounded w-full"
      />
      <input
        v-model="code"
        :placeholder="t('verify.code')"
        required
        class="block mb-4 p-2 border rounded w-full"
      />
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center items-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50"
      >
        <span v-if="!loading">{{ t('verify.submit') }}</span>
        <span v-else>{{ t('verify.loading') }}</span>
      </button>
    </form>

    <p v-if="success" class="mt-4 text-green-600">
      {{ t('verify.success') }} {{ t('verify.redirecting') }}
    </p>
    <p v-if="error" class="mt-4 text-red-600">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t }    = useI18n()
const route    = useRoute()
const router   = useRouter()
const email    = ref(route.query.email || '')
const code     = ref(route.query.code  || '')
const loading  = ref(false)
const success  = ref(false)
const error    = ref('')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await axios.post('/auth/verify', { email: email.value, code: code.value })
    success.value = true
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || t('verify.error')
  } finally {
    loading.value = false
  }
}
</script>
