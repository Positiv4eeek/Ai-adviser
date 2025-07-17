<template>
  <div class="p-8 max-w-md mx-auto text-white space-y-6 bg-zinc-800 rounded-xl">
    <h2 class="text-2xl font-bold text-center">{{ $t('profile.title') }}</h2>

    <div v-if="success" class="text-green-400 text-center">{{ success }}</div>
    <div v-if="error" class="text-red-500 text-center">{{ error }}</div>

    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="block mb-1">{{ $t('profile.firstName') }}</label>
        <input
          v-model="first_name"
          type="text"
          class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        />
      </div>

      <div>
        <label class="block mb-1">{{ $t('profile.lastName') }}</label>
        <input
          v-model="last_name"
          type="text"
          class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        />
      </div>

      <hr class="border-zinc-600" />

      <div>
        <label class="block mb-1">{{ $t('profile.oldPassword') }}</label>
        <input
          v-model="old_password"
          type="password"
          class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        />
      </div>

      <div>
        <label class="block mb-1">{{ $t('profile.newPassword') }}</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
      >
        {{ loading ? $t('profile.saving') : $t('profile.save') }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const first_name = ref('')
const last_name = ref('')
const old_password = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

onMounted(async () => {
  try {
    const { data } = await axios.get('/auth/me')
    first_name.value = data.first_name
    last_name.value = data.last_name
  } catch (e) {
    error.value = t('profile.fetchError')
  }
})

async function submit() {
  error.value = ''
  success.value = ''
  loading.value = true

  const payload = {}
  if (first_name.value.trim()) payload.first_name = first_name.value.trim()
  if (last_name.value.trim()) payload.last_name = last_name.value.trim()

  if (old_password.value || password.value) {
    if (!old_password.value || !password.value) {
      error.value = t('profile.bothPasswordsRequired')
      loading.value = false
      return
    }
    payload.old_password = old_password.value
    payload.password = password.value
  }

  try {
    await axios.patch('/auth/me', payload)
    const updated = await axios.get('/auth/me')
    localStorage.setItem('user', JSON.stringify(updated.data))

    success.value = t('profile.updated')
    old_password.value = ''
    password.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || t('profile.updateError')
  } finally {
    loading.value = false
  }
}
</script>
