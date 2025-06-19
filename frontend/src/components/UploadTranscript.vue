<template>
  <div class="p-6 max-w-4xl mx-auto bg-white min-h-screen text-gray-900">
    <div class="flex justify-end gap-2 text-sm mb-4">
      <button
        v-for="lang in ['kz', 'ru', 'en']"
        :key="lang"
        @click="setLocale(lang)"
        :class="[
          'w-10 h-10 flex items-center justify-center rounded text-white font-semibold transition',
          'bg-black',
          locale === lang ? 'ring-2 ring-white' : 'hover:bg-opacity-80'
        ]"
      >
        {{ lang.toUpperCase() }}
      </button>
    </div>

    <div class="mb-6 flex justify-center items-start mt-2">
      <img src="/narxoz-logo.svg" alt="Narxoz Logo" class="h-10 w-auto" />
    </div>

    <h2 class="text-2xl font-bold mb-6 text-center">{{ t('upload') }}</h2>

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
          {{ loading ? 'Загрузка...' : t('send') }}
        </button>
      </div>
    </div>

    <div v-if="result" class="mt-8 space-y-6">
      <div>
        <h3 class="text-xl font-semibold mb-2">{{ t('student_info') }}</h3>
        <div class="bg-gray-50 p-4 rounded shadow space-y-1">
          <div><strong>{{ t('name') }}:</strong> {{ result.student_info.name }}</div>
          <div><strong>{{ t('faculty') }}:</strong> {{ result.student_info.faculty }}</div>
          <div><strong>{{ t('program_code') }}:</strong> {{ result.student_info.program_code }}</div>
          <div><strong>{{ t('program_name') }}:</strong> {{ result.student_info.program_name }}</div>
          <div><strong>{{ t('program_group') }}:</strong> {{ result.student_info.program_group }}</div>
          <div><strong>{{ t('entry_year') }}:</strong> {{ result.student_info.entry_year }}</div>
          <div><strong>{{ t('language') }}:</strong> {{ result.student_info.language }}</div>
          <div><strong>{{ t('gpa') }}:</strong> {{ result.student_info.gpa }}</div>
          <div><strong>{{ t('total_credits') }}:</strong> {{ result.student_info.total_credits }}</div>
        </div>
      </div>

      <div>
        <div class="flex justify-center sm:justify-end gap-4 mt-8 mb-8 px-4">
          <button
            @click="downloadJSON"
            class="text-xs bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
          >
            {{ t('download_json') }}
          </button>
          <button
            @click="clearResult"
            class="text-xs bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
          >
            {{ t('clear') }}
          </button>
        </div>
        <h3 class="text-xl font-semibold mb-2">{{ t('courses') }}</h3>

        <table class="w-full text-sm border border-collapse">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1">№</th>
              <th class="border px-2 py-1">{{ t('course_name') }}</th>
              <th class="border px-2 py-1">Кредиты</th>
              <th class="border px-2 py-1">%</th>
              <th class="border px-2 py-1">Буквенная</th>
              <th class="border px-2 py-1">Балл</th>
              <th class="border px-2 py-1">{{ t('traditional') }}</th>
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
                <span v-if="course.is_retake">✔️</span>
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
  const locale = ref('ru')

  const i18n = {
    ru: {
      upload: 'Загрузить транскрипт',
      student_info: 'Информация о студенте',
      name: 'ФИО',
      faculty: 'Факультет',
      program_code: 'Код программы',
      program_name: 'Название программы',
      program_group: 'Группа программ',
      entry_year: 'Год поступления',
      language: 'Язык обучения',
      gpa: 'GPA',
      total_credits: 'Кредиты всего',
      courses: 'Курсы',
      traditional: 'Традиционная',
      course_name: 'Название',
      download_json: 'Скачать JSON',
      clear: 'Очистить',
      send: 'Отправить'
    },
    kz: {
      upload: 'Транскриптті жүктеу',
      student_info: 'Студент туралы ақпарат',
      name: 'Аты-жөні',
      faculty: 'Факультет',
      program_code: 'Бағдарлама коды',
      program_name: 'Бағдарлама атауы',
      program_group: 'Бағдарламалар тобы',
      entry_year: 'Қабылдау жылы',
      language: 'Оқыту тілі',
      gpa: 'GPA',
      total_credits: 'Барлық кредит',
      courses: 'Курстар',
      traditional: 'Дәстүрлі баға',
      course_name: 'Пән атауы',
      download_json: 'JSON жүктеу',
      clear: 'Тазарту',
      send: 'Жіберу'
    },
    en: {
      upload: 'Upload Transcript',
      student_info: 'Student Information',
      name: 'Full Name',
      faculty: 'Faculty',
      program_code: 'Program Code',
      program_name: 'Program Name',
      program_group: 'Program Group',
      entry_year: 'Entry Year',
      language: 'Language',
      gpa: 'GPA',
      total_credits: 'Total Credits',
      courses: 'Courses',
      traditional: 'Traditional Grade',
      course_name: 'Course Name',
      download_json: 'Download JSON',
      clear: 'Clear',
      send: 'Send'
    }
  }

  const t = key => i18n[locale.value][key] || key

  function setLocale(lang) {
    locale.value = lang
    localStorage.setItem('locale', lang)
  }

  onMounted(() => {
    const savedLocale = localStorage.getItem('locale')
    if (savedLocale) locale.value = savedLocale

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
