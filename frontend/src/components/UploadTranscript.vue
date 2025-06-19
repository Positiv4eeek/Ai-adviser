<template>
  <div class="p-6 max-w-4xl mx-auto bg-white min-h-screen text-gray-900">
    <div class="mb-6 flex justify-center items-start mt-2">
      <img src="/narxoz-logo.svg" alt="Narxoz Logo" class="h-10 w-auto" />
    </div>

    <h2 class="text-2xl font-bold mb-6 text-center">Загрузить транскрипт</h2>

    <div class="text-center mb-6 space-y-4">
      <div class="flex flex-col items-center gap-4">
        <label
          for="file-upload"
          class="cursor-pointer inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-5 py-3 rounded border border-dashed border-gray-400 transition"
        >
          <svg class="w-5 h-5 text-black-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1M12 12V4m0 0l-4 4m4-4l4 4" />
          </svg>
          <span class="text-sm text-gray-700">
            {{ file?.name || "Выберите PDF файл транскрипта" }}
          </span>
        </label>
        <input
          id="file-upload"
          type="file"
          accept="application/pdf"
          @change="onFileChange"
          class="hidden"
        />

        <button
          @click="upload"
          :disabled="!file || loading"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ loading ? 'Загрузка...' : 'Отправить' }}
        </button>
      </div>
    </div>

    <div v-if="result" class="mt-8 space-y-6">
      <div>
        <h3 class="text-xl font-semibold mb-2">Информация о студенте</h3>
        <div class="bg-gray-50 p-4 rounded shadow space-y-1">
          <div><strong>ФИО:</strong> {{ result.student_info.name }}</div>
          <div><strong>Факультет:</strong> {{ result.student_info.faculty }}</div>
          <div><strong>Код программы:</strong> {{ result.student_info.program_code }}</div>
          <div><strong>Название программы:</strong> {{ result.student_info.program_name }}</div>
          <div><strong>Группа программ:</strong> {{ result.student_info.program_group }}</div>
          <div><strong>Год поступления:</strong> {{ result.student_info.entry_year }}</div>
          <div><strong>Язык обучения:</strong> {{ result.student_info.language }}</div>
          <div><strong>GPA:</strong> {{ result.student_info.gpa }}</div>
          <div><strong>Кредиты всего:</strong> {{ result.student_info.total_credits }}</div>
        </div>
      </div>

      <div>
        <div class="flex justify-center sm:justify-end gap-4 mt-8 mb-8 px-4">
          <button
            @click="downloadJSON"
            class="text-xs bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
          >
            Скачать JSON
          </button>
          <button
            @click="clearResult"
            class="text-xs bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
          >
            Очистить
          </button>
        </div>
        <h3 class="text-xl font-semibold mb-2">Курсы</h3>

        <table class="w-full text-sm border border-collapse">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1">№</th>
              <th class="border px-2 py-1">Название</th>
              <th class="border px-2 py-1">Кредиты</th>
              <th class="border px-2 py-1">%</th>
              <th class="border px-2 py-1">Буквенная</th>
              <th class="border px-2 py-1">Балл</th>
              <th class="border px-2 py-1">Традиционная</th>
              <th class="border px-2 py-1">Ретейк</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, index) in result.courses" :key="index">
              <td class="border px-2 py-1 text-center">{{ course.code || index + 1 }}</td>
              <td class="border px-2 py-1">{{ course.course_name }}</td>
              <td class="border px-2 py-1 text-center">{{ course.credits }}</td>
              <td class="border px-2 py-1 text-center">{{ course.percent ?? '—' }}</td>
              <td class="border px-2 py-1 text-center">{{ course.grade_letter }}</td>
              <td class="border px-2 py-1 text-center">{{ course.grade_point ?? '—' }}</td>
              <td class="border px-2 py-1 text-center">{{ course.grade_traditional }}</td>
              <td class="border px-2 py-1 text-center">
                <span v-if="course.is_retake">✅</span>
                <span v-else>—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="error" class="text-red-500 mt-4">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const file = ref(null)
const result = ref(null)
const loading = ref(false)
const error = ref(null)

onMounted(() => {
  const saved = localStorage.getItem('transcriptResult')
  if (saved) {
    try {
      result.value = JSON.parse(saved)
    } catch (e) {
      result.value = null
    }
  }
})

function onFileChange(e) {
  file.value = e.target.files[0]
  result.value = null
  error.value = null
}

async function upload() {
  if (!file.value) return
  const formData = new FormData()
  formData.append('file', file.value)
  loading.value = true
  result.value = null
  error.value = null

  try {
    const res = await axios.post('http://localhost:8000/upload-transcript', formData)
    result.value = res.data
    localStorage.setItem('transcriptResult', JSON.stringify(res.data))
  } catch (err) {
    error.value = err.message || 'Ошибка при загрузке'
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  const blob = new Blob([JSON.stringify(result.value, null, 2)], { type: 'application/json' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'transcript.json'
  link.click()
  URL.revokeObjectURL(link.href)
}

function clearResult() {
  result.value = null
  localStorage.removeItem('transcriptResult')
}
</script>
