<template>
  <div v-if="transcript" class="bg-zinc-800 text-white p-6 rounded-xl space-y-6">
    <h3 class="text-xl font-bold text-center">{{ $t('student.transcript_detail') }}</h3>

    <div class="flex flex-col md:flex-row gap-6 justify-center">
      <div class="bg-zinc-700 p-4 rounded-lg flex-1 max-w-md">
        <h4 class="text-lg font-semibold mb-3 text-center border-b border-zinc-600 pb-2">
          {{ $t('student.student_info') }}
        </h4>
        <dl class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
          <template v-for="(value, key) in transcript.student_info" :key="key">
            <dt class="font-medium text-right">{{ $t(`student.${key}`) || key }}</dt>
            <dd class="px-2">{{ value }}</dd>
          </template>
        </dl>
      </div>

      <div class="bg-zinc-700 p-4 rounded-lg flex-1">
        <h4 class="text-lg font-semibold mb-3 text-center border-b border-zinc-600 pb-2">
          {{ $t('courses.courses') }}
        </h4>
        <div class="overflow-auto max-h-80">
          <table class="w-full text-sm border-collapse">
            <thead class="sticky top-0 bg-zinc-800 bg-opacity-90">
              <tr>
                <th class="px-3 py-2 font-medium">№</th>
                <th class="px-3 py-2 font-medium">{{ $t('courses.headers.disciplineName') }}</th>
                <th class="px-3 py-2 font-medium text-center">{{ $t('courses.headers.credits') }}</th>
                <th class="px-3 py-2 font-medium text-center">{{ $t('courses.headers.percent') }}</th>
                <th class="px-3 py-2 font-medium text-center">{{ $t('courses.headers.traditional') }}</th>
                <th class="px-3 py-2 font-medium text-center">{{ $t('courses.retake') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(course, idx) in transcript.courses"
                :key="idx"
                class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500 transition-colors"
              >
                <td class="px-3 py-2 text-center">{{ idx + 1 }}</td>
                <td class="px-3 py-2">{{ course.course_name }}</td>
                <td class="px-3 py-2 text-center">{{ course.credits }}</td>
                <td class="px-3 py-2 text-center">{{ course.percent ?? '-' }}</td>
                <td class="px-3 py-2 text-center">{{ course.grade_traditional }}</td>
                <td class="px-3 py-2 text-center">{{ course.is_retake ? '✔' : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="text-center">
      <button
        @click="downloadJSON"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
      >
        {{ $t('general.download_json') }}
      </button>
    </div>
  </div>

  <p v-else class="text-white text-center">{{ $t('general.loading') }}</p>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  transcriptId: {
    type: Number,
    required: true
  }
})

const transcript = ref(null)

const fetchTranscript = async () => {
  try {
    const { data } = await axios.get(`/transcript/${props.transcriptId}`)
    transcript.value = data
  } catch (err) {
    transcript.value = null
    console.error(err)
  }
}

watch(() => props.transcriptId, fetchTranscript)
onMounted(fetchTranscript)

function downloadJSON() {
  const blob = new Blob([JSON.stringify(transcript.value, null, 2)], { type: 'application/json' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'transcript.json'
  link.click()
}
</script>

<style scoped>
.overflow-auto::-webkit-scrollbar {
  height: 10px;
}
.overflow-auto::-webkit-scrollbar-thumb {
  background-color: rgba(255,255,255,0.2);
  border-radius: 3px;
}
</style>