<template>
  <div class="bg-zinc-800 p-6 rounded-xl space-y-4 text-white max-w-3xl">
    <h3 class="text-2xl font-bold">{{ $t('admin.aiSettingsTitle') }}</h3>

    <div v-if="loading" class="text-gray-400">{{ $t('general.loading') }}</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="success" class="text-green-500">{{ success }}</div>

    <div v-if="!loading">
      <label class="block mb-1">{{ $t('admin.model') }}</label>
      <input v-model="form.model" class="w-full mb-4 p-2 rounded bg-zinc-700 border border-zinc-600" />

      <label class="block mb-1">{{ $t('admin.systemPrompt') }}</label>
      <textarea v-model="form.system_prompt" class="w-full mb-4 p-2 rounded bg-zinc-700 border border-zinc-600 min-h-[100px]" />

      <label class="block mb-1">{{ $t('admin.temperature') }} (0–2)</label>
      <input type="number" step="0.1" min="0" max="2" v-model.number="form.temperature" class="w-full mb-4 p-2 rounded bg-zinc-700 border border-zinc-600" />

      <label class="block mb-1">{{ $t('admin.maxTokens') }}</label>
      <input type="number" min="1" v-model.number="form.max_tokens" class="w-full mb-4 p-2 rounded bg-zinc-700 border border-zinc-600" />

      <button @click="save" :disabled="saving" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white">
        {{ saving ? $t('general.saving') : $t('general.save') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const form = ref({
  model: '',
  system_prompt: '',
  temperature: 0.7,
  max_tokens: 1000
})

const loading = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref('')

onMounted(fetchSettings)

async function fetchSettings() {
  loading.value = true
  try {
    const res = await axios.get('/admin/ai-settings')
    Object.assign(form.value, res.data)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load settings'
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    await axios.put('/admin/ai-settings', form.value)
    success.value = t('admin.settingsSaved')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to save settings'
  } finally {
    saving.value = false
    setTimeout(() => {
      success.value = ''
      error.value = ''
    }, 2500)
  }
}
</script>
