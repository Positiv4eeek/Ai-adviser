<template>
  <div class="p-8 max-w-sm mx-auto">
    <h2 class="text-2xl mb-4">{{ t('nav.register') }}</h2>
    <form @submit.prevent="submit">
      <input
        v-model="firstName"
        :placeholder="t('register.firstName')"
        required
        class="block mb-2 p-2 border rounded w-full"
      />
      <input
        v-model="lastName"
        :placeholder="t('register.lastName')"
        required
        class="block mb-2 p-2 border rounded w-full"
      />
      <input
        v-model="email"
        type="email"
        :placeholder="t('register.email')"
        required
        class="block mb-2 p-2 border rounded w-full"
      />
      <input
        v-model="password"
        type="password"
        :placeholder="t('register.password')"
        required
        class="block mb-4 p-2 border rounded w-full"
      />
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center items-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50"
      >
        <span v-if="!loading">{{ t('register.submit') }}</span>
        <span v-else>{{ t('register.loading') }}</span>
      </button>
    </form>

    <p v-if="success" class="mt-4 text-green-600">
      {{ t('register.verificationSent') }}
    </p>
    <p v-if="error" class="mt-4 text-red-600">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const firstName = ref('')
const lastName  = ref('')
const email     = ref('')
const password  = ref('')
const success   = ref(false)
const error     = ref('')
const loading   = ref(false)
const router    = useRouter()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post('/auth/register', {
      first_name: firstName.value,
      last_name:  lastName.value,
      email:      email.value,
      password:   password.value,
      role:       'student'
    })
    if (res.status === 201) {
      success.value = true
      setTimeout(() => {
        router.push({ path: '/verify', query: { email: email.value } })
      }, 1000)
    }
  } catch (e) {
    error.value = e.response?.data?.detail || t('register.error')
  } finally {
    loading.value = false
  }
}
</script>
