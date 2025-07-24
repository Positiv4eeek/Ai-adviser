<template>
  <div class="space-y-4 max-w-4xl mx-auto">
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
      class="bg-zinc-900 p-4 rounded border border-zinc-700 text-white space-y-4"
    >
      <div v-if="parsedResponse.courses?.length">
        <h4 class="text-white text-base font-semibold mb-2">{{ $t('dashboard.recommended_courses') }}</h4>
        <div
          v-for="course in parsedResponse.courses"
          :key="course.code"
          class="border border-zinc-700 rounded px-3 py-2 bg-zinc-800 mb-2"
        >
          <div class="flex justify-between items-center">
            <div>
              <span class="text-white font-medium">{{ course.name }}</span>
              <span>&nbsp;</span>
              <span class="text-gray-400 text-sm">({{ course.code }}, {{ course.credits }} ECTS)</span>
            </div>
            <span
              class="text-xs rounded px-2 py-0.5"
              :class="{
                'bg-blue-600 text-white': course.type === 'required',
                'bg-green-600 text-white': course.type === 'elective',
                'bg-orange-500 text-white': course.type === 'repeat'
              }"
            >
              {{ $t('dashboard.course_type_' + course.type) }}
            </span>
          </div>
          <div class="text-gray-300 text-sm mt-1 text-left">{{ course.reason }}</div>
          <div v-if="course.prerequisites_met?.length" class="text-gray-500 text-xs mt-1">
            {{ $t('dashboard.prerequisites') }}: {{ course.prerequisites_met.join(', ') }}
          </div>
        </div>
      </div>

      <div v-if="parsedResponse.comment">
        <h4 class="text-yellow-400 font-bold mt-4 mb-1">{{ $t('dashboard.comment') }}</h4>
        <p class="text-gray-300 text-sm leading-relaxed whitespace-pre-line border-l-4 border-yellow-400 pl-4">
          {{ parsedResponse.comment }}
        </p>
      </div>

      <div v-if="!parsedResponse.courses">
        <p class="text-red-500 text-sm">{{ $t('dashboard.json_error') }}</p>
        <pre class="bg-zinc-800 p-2 rounded text-xs text-gray-400 font-mono whitespace-pre-wrap max-h-64 overflow-y-auto">
          {{ recommendations }}
        </pre>
      </div>
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
const parsedResponse = ref({})

function isValidJSON(json) {
  try {
    parsedResponse.value = JSON.parse(json)
    return true
  } catch {
    parsedResponse.value = {}
    return false
  }
}

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
  parsedResponse.value = {}

  try {
    const res = await axios.post('/ai/recommendations', {
      prompt_name: promptName.value
    })
    recommendations.value = res.data.recommendations
    isValidJSON(res.data.recommendations)
  } catch (e) {
    error.value = e.response?.data?.detail || 'AI request failed.'
  } finally {
    loading.value = false
  }
}
</script>
