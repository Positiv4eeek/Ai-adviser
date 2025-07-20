<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold">{{ $t('admin.prompts') }}</h2>

    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="success" class="text-green-500">{{ success }}</div>

    <form @submit.prevent="createPrompt" class="space-y-4 bg-zinc-800 p-4 rounded">
      <input
        v-model="newPrompt.name"
        type="text"
        class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        :placeholder="$t('admin.promptName')"
        required
      />
      <textarea
        v-model="newPrompt.content"
        class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        :placeholder="$t('admin.promptContent')"
        rows="4"
        required
      ></textarea>
      <button
        type="submit"
        class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
      >
        {{ $t('admin.addPrompt') }}
      </button>
    </form>

    <div v-if="prompts.length === 0" class="text-gray-400">
      {{ $t('admin.noPrompts') }}
    </div>

    <div v-for="prompt in prompts" :key="prompt.id" class="bg-zinc-800 p-4 rounded space-y-2">
      <input
        v-model="prompt.name"
        class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
      />
      <textarea
        v-model="prompt.content"
        class="w-full p-2 rounded bg-zinc-700 border border-zinc-600"
        rows="4"
      ></textarea>
      <div class="flex justify-end gap-2">
        <button
          @click="updatePrompt(prompt)"
          class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
        >
          {{ $t('admin.save') }}
        </button>
        <button
          @click="deletePrompt(prompt.id)"
          class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
        >
          {{ $t('admin.delete') }}
        </button>
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
const newPrompt = ref({ name: '', content: '' })
const error = ref('')
const success = ref('')

async function fetchPrompts() {
  try {
    const res = await axios.get('/admin/prompts')
    prompts.value = res.data
  } catch (e) {
    error.value = t('admin.fetchError')
  }
}

async function createPrompt() {
  try {
    const res = await axios.post('/admin/prompts', newPrompt.value)
    prompts.value.push(res.data)
    newPrompt.value = { name: '', content: '' }
    success.value = t('admin.created')
  } catch (e) {
    error.value = e.response?.data?.detail || t('admin.createError')
  }
}

async function updatePrompt(prompt) {
  try {
    await axios.patch(`/admin/prompts/${prompt.id}`, {
      name: prompt.name,
      content: prompt.content
    })
    success.value = t('admin.updated')
  } catch (e) {
    error.value = e.response?.data?.detail || t('admin.updateError')
  }
}

async function deletePrompt(id) {
  try {
    await axios.delete(`/admin/prompts/${id}`)
    prompts.value = prompts.value.filter(p => p.id !== id)
    success.value = t('admin.deleted')
  } catch (e) {
    error.value = e.response?.data?.detail || t('admin.deleteError')
  }
}

onMounted(fetchPrompts)
</script>
