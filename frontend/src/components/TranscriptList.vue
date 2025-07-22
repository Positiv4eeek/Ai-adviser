<template>
  <div class="space-y-4 bg-zinc-800 p-6 rounded-xl text-white">
    <h2 class="text-xl font-bold">{{ $t('transcript.all_transcripts') }}</h2>

    <input
      v-model="search"
      type="text"
      :placeholder="$t('admin.search_transcript_placeholder')"
      class="mb-4 p-2 rounded w-full bg-zinc-700 text-white placeholder-gray-400"
    />

    <div v-if="loading">{{ $t('general.loading') }}</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <table class="w-full text-sm border-collapse" v-if="filteredTranscripts.length">
      <thead>
        <tr class="bg-zinc-700">
          <th class="px-3 py-2">{{ $t('student.id') }}</th>
          <th class="px-3 py-2">{{ $t('student.student_id') }}</th>
          <th class="px-3 py-2">{{ $t('student.name') }}</th>
          <th class="px-3 py-2">{{ $t('student.faculty') }}</th>
          <th class="px-3 py-2">{{ $t('transcript.date') }}</th>
          <th class="px-3 py-2 text-center">{{ $t('general.actions') || 'Действия' }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="t in filteredTranscripts"
          :key="t.id"
          class="hover:bg-zinc-600"
        >
          <td class="px-3 py-2">{{ t.id }}</td>
          <td class="px-3 py-2">{{ t.student_id }}</td>
          <td class="px-3 py-2">{{ t.student_info?.name || '-' }}</td>
          <td class="px-3 py-2">{{ t.student_info?.faculty || '-' }}</td>
          <td class="px-3 py-2">{{ new Date(t.parsed_at).toLocaleDateString() }}</td>
          <td class="px-3 py-2 text-center">
           <div class="flex justify-center gap-2">
                <button
                @click.stop="$emit('select', t.id)"
                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
                >
                {{ $t('general.details') }}
                </button>
                <button
                @click.stop="deleteTranscript(t.id)"
                class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
                >
                {{ $t('general.delete') }}
                </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="text-center text-gray-400">{{ $t('transcript.no_transcripts') }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const props = defineProps({ userId: String })
const emit = defineEmits(['select'])

const transcripts = ref([])
const loading = ref(false)
const error = ref('')
const search = ref('')
const { t } = useI18n()

const filteredTranscripts = computed(() => {
  const q = search.value.toLowerCase()
  return transcripts.value.filter(t => {
    const name = t.student_info?.name?.toLowerCase() || ''
    const faculty = t.student_info?.faculty?.toLowerCase() || ''
    return name.includes(q) || faculty.includes(q)
  })
})

onMounted(async () => {
  loading.value = true
  try {
    const url = props.userId ? `/transcript?user_id=${props.userId}` : '/transcript'
    const { data } = await axios.get(url)
    transcripts.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
})

async function deleteTranscript(id) {
  if (!confirm(t('transcript.confirm_delete'))) return
  try {
    await axios.delete(`/transcript/${id}`)
    transcripts.value = transcripts.value.filter(t => t.id !== id)
  } catch (e) {
    alert(t('transcript.delete_error') + ': ' + (e.response?.data?.detail || e.message))
  }
}
</script>
