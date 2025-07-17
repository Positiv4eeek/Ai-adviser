<template>
  <div class="p-6 space-y-6 text-white">
    <h2 class="text-4xl font-bold">{{ $t('nav.dashboard') }}</h2>

    <div v-if="error">
      <p class="text-red-600">{{ error }}</p>
    </div>

    <div v-else-if="user">
      <div class="flex gap-4">
        <button
          :class="tabClass(activeTab === 'info')"
          @click="activeTab = 'info'"
        >{{ $t('dashboard.tabInfo') }}</button>

        <button
          :class="tabClass(activeTab === 'settings')"
          @click="activeTab = 'settings'"
        >{{ $t('dashboard.tabSettings') }}</button>

        <button
          :class="tabClass(activeTab === 'transcript_curriculum')"
          @click="activeTab = 'transcript_curriculum'"
        >{{ $t('dashboard.tabTranscriptAndCurriculum') }}</button>

      </div>

      <div v-if="activeTab === 'info'" class="mt-4 space-y-2">
        <p>{{ $t('dashboard.greeting', { firstName: user.first_name, lastName: user.last_name }) }}</p>
        <p>{{ $t('dashboard.role', { role: user.role }) }}</p>
        <p>{{ $t('dashboard.email') }}: {{ user.email }}</p>
      </div>

      <div v-if="activeTab === 'settings'" class="mt-4">
        <ProfileSettings />
      </div>

      <div v-if="activeTab === 'transcript_curriculum'" class="mt-4">
        <UploadTranscript />
      </div>

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
import ProfileSettings from '@/views/Settings.vue'
import UploadTranscript from '@/components/UploadTranscript.vue'

const { t } = useI18n()
const user = ref(null)
const error = ref('')
const activeTab = ref('info')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = t('dashboard.authRequired')
    return
  }
  try {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    const res = await axios.get('/auth/me')
    user.value = res.data
  } catch (e) {
    error.value = t('dashboard.fetchError')
  }
})

const tabClass = (isActive) => [
  'px-4 py-2 font-semibold rounded transition text-white',
  isActive ? 'bg-blue-600' : 'tab-inactive'
]
</script>

<style scoped>
.tab-inactive {
  background-color: rgb(39 39 42);
}
.tab-inactive:hover {
  background-color: rgb(63 63 70);
}
</style>
