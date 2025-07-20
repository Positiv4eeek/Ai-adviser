<template>
  <div class="space-y-4">
    <h3 class="text-2xl font-semibold">{{ $t('dashboard.ai_history') }}</h3>

    <div v-if="loading">{{ $t('dashboard.loading') }}</div>
    <div v-else-if="logs.length === 0">{{ $t('dashboard.no_history') }}</div>

    <div v-else class="space-y-4">
      <div
        v-for="log in logs"
        :key="log.id"
        class="p-4 rounded bg-zinc-800 border border-zinc-700"
      >
        <p class="text-sm text-gray-400">
          {{ $t('dashboard.prompt_name') }}: <strong>{{ log.prompt_name }}</strong>
          — {{ new Date(log.created_at).toLocaleString() }}
        </p>
        <details class="mt-2">
          <summary class="cursor-pointer text-blue-500">{{ $t('dashboard.prompt_input') }}</summary>
          <pre class="whitespace-pre-wrap text-sm mt-1">{{ log.prompt_input }}</pre>
        </details>
        <div class="mt-3">
          <p class="font-medium mb-1">{{ $t('dashboard.response') }}:</p>
          <div class="bg-zinc-900 p-3 rounded text-sm whitespace-pre-wrap">
            {{ log.response }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const logs = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('/ai/recommendations/history')
    logs.value = res.data
  } catch (e) {
    console.error(e)
    logs.value = []
  } finally {
    loading.value = false
  }
})
</script>
