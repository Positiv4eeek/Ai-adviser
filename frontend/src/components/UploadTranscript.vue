<template>
  <div class="space-y-8">

    <div v-if="transcriptResult && !showUploadForm" class="text-center">
      <button
        @click="showUploadForm = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
      >
        {{ $t('upload.upload_new_transcript') }}
      </button>
    </div>


    <div
      v-if="!transcriptResult || showUploadForm"
      class="bg-zinc-800 p-6 rounded-xl text-white space-y-4"
    >
      <h2 class="text-2xl font-bold text-center">
        {{ $t('upload.upload_transcript') }}
      </h2>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <label
          for="trans-upload"
          class="flex-1 bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded border-gray-600 text-center cursor-pointer min-w-0"
        >
          {{ transcriptFile?.name || $t('upload.choose_pdf') }}
          <input
            id="trans-upload"
            type="file"
            accept="application/pdf"
            class="hidden"
            @change="onTranscriptChange"
          />
        </label>
        <button
          @click="uploadTranscript"
          :disabled="!transcriptFile || loading"
          class="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded"
        >
          {{ loading ? $t('general.loading') : $t('upload.send') }}
        </button>
      </div>

      <p v-if="error" class="text-red-500 text-center">{{ error }}</p>
      <p v-if="noTranscript && !error" class="text-yellow-400 text-center">
        {{ $t('upload.no_transcript_found') }}
      </p>
    </div>

    <div
      v-if="transcriptResult"
      class="w-fit bg-zinc-800 p-6 rounded-xl text-white space-y-6 mx-auto"
    >
      <div class="flex flex-col md:flex-row gap-6 justify-center">

        <div class="bg-zinc-700 p-4 rounded-lg flex-1 max-w-md">
          <h3 class="text-xl font-semibold mb-4 text-center border-b border-zinc-600 pb-2">
            {{ $t('student.student_info') }}
          </h3>
          <dl class="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
            <dt class="font-medium text-right">{{ $t('student.name') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.name }}</dd>

            <dt class="font-medium text-right">{{ $t('student.faculty') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.faculty }}</dd>

            <dt class="font-medium text-right">{{ $t('student.program_code') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.program_code }}</dd>

            <dt class="font-medium text-right">{{ $t('student.program_name') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.program_name }}</dd>

            <dt class="font-medium text-right">{{ $t('student.program_group') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.program_group }}</dd>

            <dt class="font-medium text-right">{{ $t('student.entry_year') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.entry_year }}</dd>

            <dt class="font-medium text-right">{{ $t('student.language') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.language }}</dd>

            <dt class="font-medium text-right">{{ $t('student.gpa') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.gpa }}</dd>

            <dt class="font-medium text-right">{{ $t('student.total_credits') }}</dt>
            <dd class="px-2">{{ transcriptResult.student_info.total_credits }}</dd>
          </dl>
        </div>


        <div class="bg-zinc-700 p-4 rounded-lg flex-1">
          <h3 class="text-xl font-semibold mb-4 text-center border-b border-zinc-600 pb-2">
            {{ $t('courses.courses') }}
          </h3>
          <div class="overflow-auto max-h-80">
            <table class="w-full text-sm border-collapse">
              <thead class="sticky top-0 bg-zinc-800 bg-opacity-90">
                <tr>
                  <th class="px-3 py-2 font-medium text-white">№</th>
                  <th class="px-3 py-2 font-medium text-white">{{ $t('courses.headers.disciplineName') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.credits') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.percent') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.traditional') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.retake') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(course, idx) in transcriptResult.courses"
                  :key="idx"
                  class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500 transition-colors"
                >
                  <td class="px-3 py-2 text-center">{{ idx + 1 }}</td>
                  <td class="px-3 py-2">{{ course.course_name }}</td>
                  <td class="px-3 py-2 text-center">{{ course.credits }}</td>
                  <td class="px-3 py-2 text-center">
                    <span v-if="course.percent !== null && course.percent !== undefined">
                      {{ course.percent }}
                    </span>
                    <span v-else>-</span>
                  </td>
                  <td class="px-3 py-2 text-center">{{ course.grade_traditional }}</td>
                  <td class="px-3 py-2 text-center">
                    <span v-if="course.is_retake">✔</span>
                    <span v-else>-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="text-center">
        <button
          @click="downloadTranscriptJSON"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
        >
          {{ $t('general.download_json') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const transcriptFile = ref(null)
const transcriptResult = ref(null)
const showUploadForm = ref(false)
const loading = ref(false)
const error = ref('')
const noTranscript = ref(false)

function onTranscriptChange(e) {
  transcriptFile.value = e.target.files[0]
  transcriptResult.value = null
  error.value = null
  noTranscript.value = false
}

async function fetchUserTranscript() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await axios.get('/transcript/current')
    transcriptResult.value = data
    noTranscript.value = false
  } catch (e) {
    if (e.response?.status === 404) {
      noTranscript.value = true
    } else {
      error.value = 'Не удалось загрузить транскрипт'
    }
  } finally {
    loading.value = false
  }
}

async function uploadTranscript() {
  if (!transcriptFile.value) return
  loading.value = true
  error.value = null

  const form = new FormData()
  form.append('file', transcriptFile.value)

  try {
    await axios.post('/transcript/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    await fetchUserTranscript()
    showUploadForm.value = false
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
}

function downloadTranscriptJSON() {
  const blob = new Blob([JSON.stringify(transcriptResult.value, null, 2)], {
    type: 'application/json'
  })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'transcript.json'
  link.click()
}

onMounted(() => {
  fetchUserTranscript()
})
</script>

<style scoped>
.overflow-auto::-webkit-scrollbar {
  height: 10px;
}
.overflow-auto::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}
</style>
