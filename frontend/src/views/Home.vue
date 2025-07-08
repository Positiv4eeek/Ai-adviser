<template>
  <div>
    <h1 class="text-3xl mb-4">{{ $t('home.welcome') }}</h1>

    <UploadTranscript v-if="isAuthenticated" />

    <div v-else class="p-4">
      <p>
        {{ $t('home.prompt') }} 
        <router-link to="/login" class="text-blue-600 underline">{{ $t('nav.login') }}</router-link>
        {{ $t('home.or') }}
        <router-link to="/register" class="text-blue-600 underline">{{ $t('nav.register') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import UploadTranscript from '@/components/UploadTranscript.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('token')
})
</script>

<style scoped>

</style>
