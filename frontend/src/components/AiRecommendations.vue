<template>
  <div class="space-y-4">
    <div class="flex gap-4 items-center">
      <label class="text-white">{{ $t('dashboard.selectPrompt') }}</label>
      <select v-model="promptName" class="bg-zinc-800 text-white px-3 py-2 rounded border border-zinc-600">
        <option v-for="prompt in prompts" :key="prompt.name" :value="prompt.name">
          {{ prompt.name }} — {{ prompt.description }}
        </option>
      </select>
    </div>

    <button
      :disabled="loading"
      @click="fetchRecommendations"
      class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
    >
      {{ loading ? $t('dashboard.loadingAi') : $t('dashboard.getRecommendations') }}
    </button>

    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div
      v-if="recommendations"
      class="whitespace-pre-wrap bg-zinc-900 p-4 rounded border border-zinc-700 text-white"
    >
      {{ recommendations }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const prompts = ref([])
const promptName = ref('')
const loading = ref(false)
const error = ref('')
const recommendations = ref('')

onMounted(async () => {
  try {
    const res = await axios.get('/ai/prompts')
    prompts.value = res.data
    if (prompts.value.length > 0) {
      promptName.value = prompts.value[0].name
    }
  } catch (e) {
    console.error('Failed to load prompts:', e)
    error.value = 'Failed to load prompts.'
  }
})

async function fetchRecommendations() {
  loading.value = true
  error.value = ''
  recommendations.value = ''

  try {
    const res = await axios.post('/ai/recommendations', {
      prompt_name: promptName.value
    })
    recommendations.value = res.data.recommendations
  } catch (e) {
    error.value = e.response?.data?.detail || 'AI request failed.'
  } finally {
    loading.value = false
  }
}
</script>
