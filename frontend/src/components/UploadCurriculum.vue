<template>
  <div class="space-y-8">
    <div class="bg-zinc-800 p-6 rounded-xl text-white space-y-4">
      <h2 class="text-2xl font-bold text-center">{{ t('upload.upload_curriculum') }}</h2>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <label
          for="curr-upload"
          class="flex-1 bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded border-gray-600 text-center cursor-pointer min-w-0"
        >
          {{ fileName }}
          <input
            id="curr-upload"
            type="file"
            accept=".xls,.xlsx"
            class="hidden"
            @change="onFileChange"
          />
        </label>
        <button
          @click="upload"
          :disabled="!file || loading"
          class="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded"
        >
          {{ loading ? t('general.loading') : t('upload.send') }}
        </button>
      </div>
      <p v-if="error" class="text-red-500 text-center">{{ error }}</p>
      <p v-if="success" class="text-green-400 text-center">{{ success }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n }     from 'vue-i18n'
import axios           from 'axios'

const { t } = useI18n()

const file    = ref(null)
const loading = ref(false)
const error   = ref('')
const success = ref('')

const fileName = computed(() => file.value?.name || t('upload.choose_xlsx'))

function onFileChange(e) {
  file.value    = e.target.files[0]
  error.value   = ''
  success.value = ''
}

async function upload() {
  if (!file.value) return
  loading.value = true
  error.value   = ''
  success.value = ''

  const form = new FormData()
  form.append('file', file.value)

  try {
    const { data } = await axios.post('/curriculum/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    success.value = t('upload.saved_id', { id: data.id })
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
}
</script>
