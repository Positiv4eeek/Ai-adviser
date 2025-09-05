<template>
  <div class="space-y-4 bg-zinc-800 p-6 rounded-xl text-white">
    <h2 class="text-xl font-bold">{{ $t('admin.prompts') }}</h2>

    <button @click="showCreateModal = true" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded mb-4">
      {{ $t('admin.addPrompt') }}
    </button>

    <input
      v-model="search"
      type="text"
      :placeholder="$t('admin.searchPrompt')"
      class="mb-4 p-2 rounded w-full bg-zinc-700 text-white placeholder-gray-400"
    />

    <table class="w-full text-sm border-collapse" v-if="filteredPrompts.length">
      <thead>
        <tr class="bg-zinc-700">
          <th class="px-3 py-2 text-left w-1/6">{{ $t('admin.promptName') }}</th>
          <th class="px-3 py-2 text-left w-2/6">{{ $t('admin.promptDescription') }}</th>
          <th class="px-3 py-2 text-left w-3/6">{{ $t('admin.promptContent') }}</th>
          <th class="px-3 py-2 text-center">{{ $t('general.actions') || 'Действия' }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prompt in filteredPrompts" :key="prompt.id" class="hover:bg-zinc-600 group">
          <td class="px-3 py-2 font-semibold truncate max-w-[180px]">{{ prompt.name }}</td>
          <td class="px-3 py-2 text-gray-300 truncate max-w-[240px]">{{ prompt.description }}</td>
          <td class="px-3 py-2 text-gray-200 truncate max-w-[380px]">{{ prompt.content }}</td>
          <td class="px-3 py-2 text-center">
            <div class="flex justify-center gap-2">
              <button @click="startEdit(prompt)" class="bg-gray-700 hover:bg-green-700 text-white px-2 py-1 rounded">
                {{ $t('admin.editPrompt') }}
              </button>
              <button @click="deletePrompt(prompt.id)" class="bg-gray-700 hover:bg-red-700 text-white px-2 py-1 rounded">
                {{ $t('admin.delete') }}
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="text-center text-gray-400">{{ $t('admin.noPrompts') }}</div>

    
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-zinc-800 rounded-lg p-8 w-full max-w-2xl shadow-xl relative">
        <button @click="showCreateModal=false" class="absolute right-3 top-3 text-2xl text-gray-400 hover:text-white">&times;</button>
        <h3 class="text-lg font-bold mb-4">{{ $t('admin.addPrompt') }}</h3>
        <input
          v-model="newPrompt.name"
          class="mb-3 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 text-base"
          :placeholder="$t('admin.promptName')"
        />
        <textarea
          v-model="newPrompt.description"
          class="mb-3 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 resize-y min-h-[60px] text-base"
          :placeholder="$t('admin.promptDescription')"
        />
        <textarea
          v-model="newPrompt.content"
          class="mb-4 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 resize-y min-h-[120px] text-base"
          :placeholder="$t('admin.promptContent')"
        />
        <div class="flex justify-end gap-3">
          <button @click="createPrompt" class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded text-base">
            {{ $t('admin.save') }}
          </button>
          <button @click="showCreateModal=false" class="bg-gray-600 hover:bg-gray-700 text-white px-5 py-2 rounded text-base">
            {{ $t('general.cancel') }}
          </button>
        </div>
      </div>
    </div>

    
    <div v-if="editingPrompt" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-zinc-800 rounded-lg p-8 w-full max-w-2xl shadow-xl relative">
        <button @click="editingPrompt=null" class="absolute right-3 top-3 text-2xl text-gray-400 hover:text-white">&times;</button>
        <h3 class="text-lg font-bold mb-4">{{ $t('admin.editPrompt') }}</h3>
        <input
          v-model="editingPrompt.name"
          class="mb-3 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 text-base"
          :placeholder="$t('admin.promptName')"
        />
        <textarea
          v-model="editingPrompt.description"
          class="mb-3 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 resize-y min-h-[60px] text-base"
          :placeholder="$t('admin.promptDescription')"
        />
        <textarea
          v-model="editingPrompt.content"
          class="mb-4 p-3 w-full rounded bg-zinc-700 border border-zinc-600 text-gray-100 resize-y min-h-[200px] text-base"
          :placeholder="$t('admin.promptContent')"
        />
        <div class="flex justify-end gap-3">
          <button @click="saveEdit" class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded text-base">
            {{ $t('admin.save') }}
          </button>
          <button @click="editingPrompt=null" class="bg-gray-600 hover:bg-gray-700 text-white px-5 py-2 rounded text-base">
            {{ $t('general.cancel') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const prompts = ref([])
const newPrompt = ref({ name: '', description: '', content: '' })
const error = ref('')
const success = ref('')
const search = ref('')
const editingPrompt = ref(null)
const showCreateModal = ref(false)
let originalPrompt = null

const filteredPrompts = computed(() =>
  prompts.value.filter(p =>
    (p.name?.toLowerCase() || '').includes(search.value.toLowerCase()) ||
    (p.description?.toLowerCase() || '').includes(search.value.toLowerCase()) ||
    (p.content?.toLowerCase() || '').includes(search.value.toLowerCase())
  )
)

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
    const res = await axios.post('/admin/prompts', {
      name: newPrompt.value.name,
      description: newPrompt.value.description,
      content: newPrompt.value.content
    })
    prompts.value.push(res.data)
    newPrompt.value = { name: '', description: '', content: '' }
    showCreateModal.value = false
    success.value = t('admin.created')
    setTimeout(() => success.value = '', 2000)
  } catch (e) {
    error.value = e.response?.data?.detail || t('admin.createError')
    setTimeout(() => error.value = '', 2000)
  }
}

function startEdit(prompt) {
  editingPrompt.value = { ...prompt }
  originalPrompt = prompt
}

async function saveEdit() {
  try {
    const { data } = await axios.put(`/admin/prompts/${editingPrompt.value.id}`, {
      name: editingPrompt.value.name,
      description: editingPrompt.value.description,
      content: editingPrompt.value.content
    })

    const idx = prompts.value.findIndex(p => p.id === data.id)
    if (idx !== -1) {
      prompts.value[idx] = data
    }

    editingPrompt.value = null
    success.value = t('admin.updated')
    setTimeout(() => (success.value = ''), 2000)
  } catch (e) {
    console.error(e)
    error.value = e.response?.data?.detail || t('admin.updateError')
    setTimeout(() => (error.value = ''), 2000)
  }
}

async function deletePrompt(id) {
  try {
    await axios.delete(`/admin/prompts/${id}`)
    prompts.value = prompts.value.filter(p => p.id !== id)
    success.value = t('admin.deleted')
    setTimeout(() => success.value = '', 2000)
  } catch (e) {
    error.value = e.response?.data?.detail || t('admin.deleteError')
    setTimeout(() => error.value = '', 2000)
  }
}

onMounted(fetchPrompts)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.rotate-90 {
  transform: rotate(90deg);
}
</style>
