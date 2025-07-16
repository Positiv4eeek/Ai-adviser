<template>
  <div class="p-8">
    <h2 class="text-3xl mb-4">{{ $t('nav.dashboard') }}</h2>
    <div v-if="error">
      <p class="text-red-600">{{ error }}</p>
    </div>
    <div v-else-if="user">
      <p>{{ $t('dashboard.greeting', { firstName: user.first_name, lastName: user.last_name }) }}</p>
      <p>{{ $t('dashboard.role', { role: user.role }) }}</p>
    </div>
    <div v-else>
      <p>{{ $t('dashboard.loading') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const user = ref(null)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = t('dashboard.authRequired')
    return
  }
  try {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    const res = await axios.get('auth/me')
    user.value = res.data
  } catch (e) {
    error.value = t('dashboard.fetchError')
  }
})
</script>

<style scoped>

</style>
