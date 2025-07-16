<template>
  <div class="space-y-4 bg-zinc-800 p-6 rounded-xl text-white">
    <h2 class="text-xl font-bold">{{ $t('curriculum.all_curricula') }}</h2>

    <input
      v-model="search"
      type="text"
      :placeholder="$t('admin.search_curriculum_placeholder')"
      class="w-full p-2 rounded bg-zinc-700 text-white placeholder-gray-400"
    />

    <div v-if="loading">{{ $t('general.loading') }}</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <table class="w-full text-sm border-collapse" v-if="filteredCurricula.length">
      <thead>
        <tr class="bg-zinc-700">
          <th class="px-3 py-2">ID</th>
          <th class="px-3 py-2">{{ $t('student.program_code') }}</th>
          <th class="px-3 py-2">{{ $t('student.program_name') }}</th>
          <th class="px-3 py-2">{{ $t('student.intake_year') }}</th>
          <th class="px-3 py-2">{{ $t('student.language') }}</th>
          <th class="px-3 py-2 text-center">{{ $t('general.actions') || 'Действия' }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="c in filteredCurricula"
          :key="c.id"
          class="hover:bg-zinc-600"
        >
          <td class="px-3 py-2">{{ c.id }}</td>
          <td class="px-3 py-2">{{ c.program_code }}</td>
          <td class="px-3 py-2">{{ c.program_name }}</td>
          <td class="px-3 py-2">{{ c.intake_year }}</td>
          <td class="px-3 py-2">{{ c.language }}</td>
          <td class="px-3 py-2 text-center space-x-2">
            <button
              @click="$emit('select', c.id)"
              class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
            >
              {{ $t('general.details')}}
            </button>
            <button
              @click="deleteCurriculum(c.id)"
              class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
            >
              {{ $t('general.delete')}}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="text-center text-gray-400">{{ $t('curriculum.no_curricula') }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['select'])

const curricula = ref([])
const search = ref('')
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/curriculum')
    curricula.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
})

const filteredCurricula = computed(() => {
  const s = search.value.toLowerCase()
  return curricula.value.filter(c =>
    c.program_name?.toLowerCase().includes(s) ||
    c.program_code?.toLowerCase().includes(s) ||
    c.language?.toLowerCase().includes(s)
  )
})

async function deleteCurriculum(id) {
  if (!confirm('Вы уверены, что хотите удалить учебный план?')) return
  try {
    await axios.delete(`/curriculum/${id}`)
    curricula.value = curricula.value.filter(c => c.id !== id)
  } catch (e) {
    alert('Ошибка при удалении: ' + (e.response?.data?.detail || e.message))
  }
}
</script>
