<template>
  <div class="p-6 max-w-5xl mx-auto bg-white min-h-screen text-gray-900">
    <!-- Language Switcher -->
    <div class="flex justify-end gap-2 text-sm mb-4">
      <button
        v-for="lang in ['kz','ru','en']"
        :key="lang"
        @click="setLocale(lang)"
        :class="[
          'w-10 h-10 flex items-center justify-center rounded text-white font-semibold transition',
          locale === lang ? 'bg-blue-600 ring-2 ring-white' : 'bg-black hover:bg-opacity-80'
        ]"
      >
        {{ lang.toUpperCase() }}
      </button>
    </div>

    <!-- Logo -->
    <div class="flex justify-center items-start mb-6">
      <img src="/narxoz-logo.svg" alt="Narxoz Logo" class="h-10 w-auto" />
    </div>

    <!-- Title -->
    <h2 class="text-2xl font-bold mb-6 text-center">
      {{ t('upload_transcript_and_curriculum') }}
    </h2>

    <!-- Upload Panels -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <!-- Transcript Upload -->
      <div class="space-y-4">
        <h3 class="font-semibold text-lg mb-2">{{ t('transcript_upload') }}</h3>
        <label
          for="trans-upload"
          class="cursor-pointer flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded border border-dashed border-gray-400"
        >
          <span>{{ transcriptFile?.name || t('choose_pdf') }}</span>
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
          :disabled="!transcriptFile || loadingTrans"
          class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ loadingTrans ? t('sending') : t('send') }}
        </button>
      </div>
      <!-- Curriculum Upload -->
      <div class="space-y-4">
        <h3 class="font-semibold text-lg mb-2">{{ t('curriculum_upload') }}</h3>
        <label
          for="curr-upload"
          class="cursor-pointer flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded border border-dashed border-gray-400"
        >
          <span>{{ curriculumFile?.name || t('choose_xlsx') }}</span>
          <input
            id="curr-upload"
            type="file"
            accept=".xls,.xlsx"
            class="hidden"
            @change="onCurriculumChange"
          />
        </label>
        <button
          @click="uploadCurriculum"
          :disabled="!curriculumFile || loadingCurr"
          class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 disabled:opacity-50"
        >
          {{ loadingCurr ? t('sending') : t('send') }}
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="text-red-500 mb-6">{{ error }}</div>

    <!-- Transcript Result -->
    <div v-if="transcriptResult" class="mb-12">
      <h3 class="text-xl font-semibold mb-4">{{ t('student_info') }}</h3>
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-gray-50 p-4 rounded shadow mb-6">
        <div><dt class="font-medium">{{ t('name') }}</dt><dd>{{ transcriptResult.student_info.name }}</dd></div>
        <div><dt class="font-medium">{{ t('faculty') }}</dt><dd>{{ transcriptResult.student_info.faculty }}</dd></div>
        <div><dt class="font-medium">{{ t('program_code') }}</dt><dd>{{ transcriptResult.student_info.program_code }}</dd></div>
        <div><dt class="font-medium">{{ t('program_name') }}</dt><dd>{{ transcriptResult.student_info.program_name }}</dd></div>
        <div><dt class="font-medium">{{ t('program_group') }}</dt><dd>{{ transcriptResult.student_info.program_group }}</dd></div>
        <div><dt class="font-medium">{{ t('entry_year') }}</dt><dd>{{ transcriptResult.student_info.entry_year }}</dd></div>
        <div><dt class="font-medium">{{ t('language') }}</dt><dd>{{ transcriptResult.student_info.language }}</dd></div>
        <div><dt class="font-medium">{{ t('gpa') }}</dt><dd>{{ transcriptResult.student_info.gpa }}</dd></div>
        <div><dt class="font-medium">{{ t('total_credits') }}</dt><dd>{{ transcriptResult.student_info.total_credits }}</dd></div>
      </dl>

      <h3 class="text-xl font-semibold mb-2">{{ t('courses') }}</h3>
      <table class="w-full text-sm border border-collapse mb-4">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">№</th>
            <th class="border px-2 py-1">{{ t('course_name') }}</th>
            <th class="border px-2 py-1">{{ t('credits') }}</th>
            <th class="border px-2 py-1">%</th>
            <th class="border px-2 py-1">{{ t('traditional') }}</th>
            <th class="border px-2 py-1">{{ t('retake') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(course, idx) in transcriptResult.courses"
            :key="idx"
            class="odd:bg-white even:bg-gray-50 hover:bg-gray-200 transition"
          >
            <td class="border px-2 py-1 text-center">{{ idx + 1 }}</td>
            <td class="border px-2 py-1">{{ course.course_name }}</td>
            <td class="border px-2 py-1 text-center">{{ course.credits }}</td>
            <td class="border px-2 py-1 text-center">{{ course.percent ?? '—' }}</td>
            <td class="border px-2 py-1 text-center">{{ course.grade_traditional }}</td>
            <td class="border px-2 py-1 text-center">
              <span v-if="course.is_retake">✔️</span><span v-else>—</span>
            </td>
          </tr>
        </tbody>
      </table>
      <button
        @click="downloadTranscriptJSON"
        class="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
      >
        {{ t('download_json') }}
      </button>
    </div>

    <!-- Curriculum Result -->
    <div v-if="curriculumResult">
      <h3 class="text-xl font-semibold mb-4">{{ t('curriculum_metadata') }}</h3>
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-gray-50 p-4 rounded shadow mb-6">
        <div><dt class="font-medium">{{ t('program_code') }}</dt><dd>{{ curriculumResult.program.program_code }}</dd></div>
        <div><dt class="font-medium">{{ t('program_name') }}</dt><dd>{{ curriculumResult.program.program_name }}</dd></div>
        <div><dt class="font-medium">{{ t('intake_year') }}</dt><dd>{{ curriculumResult.program.intake_year }}</dd></div>
        <div><dt class="font-medium">{{ t('total_credits') }}</dt><dd>{{ curriculumResult.program.total_credits }}</dd></div>
      </dl>

      <!-- Year Tabs -->
      <div class="flex space-x-2 mb-4">
        <button
          v-for="y in years"
          :key="y"
          @click="activeYear = y"
          :class="[
            'px-4 py-2 rounded text-white font-semibold transition',
            activeYear === y
              ? 'bg-blue-600 ring-2 ring-white'
              : 'bg-black hover:bg-opacity-80'
          ]"
        >
          {{ y }} {{ t('course_short') }}
        </button>
      </div>

      <!-- Semester Tabs -->
      <div class="flex space-x-2 mb-6">
        <button
          @click="activeSem = 'fall'"
          :class="[
            'px-4 py-2 rounded text-white font-semibold transition',
            activeSem === 'fall'
              ? 'bg-blue-600 ring-2 ring-white'
              : 'bg-black hover:bg-opacity-80'
          ]"
        >
          {{ t('fall') }}
        </button>
        <button
          @click="activeSem = 'spring'"
          :class="[
            'px-4 py-2 rounded text-white font-semibold transition',
            activeSem === 'spring'
              ? 'bg-blue-600 ring-2 ring-white'
              : 'bg-black hover:bg-opacity-80'
          ]"
        >
          {{ t('spring') }}
        </button>
      </div>

      <!-- Curriculum Table -->
      <table class="w-full text-sm border border-collapse mb-8">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">№</th>
            <th class="border px-2 py-1">{{ t('block_code') }}</th>
            <th class="border px-2 py-1">{{ t('discipline_code') }}</th>
            <th class="border px-2 py-1">{{ t('discipline_name') }}</th>
            <th class="border px-2 py-1">{{ t('discipline_type') }}</th>
            <th class="border px-2 py-1">{{ t('prerequisite') }}</th>
            <th class="border px-2 py-1">{{ t('credits') }}</th>
            <th class="border px-2 py-1">{{ t('contact_hours') }}</th>
            <th class="border px-2 py-1">{{ t('exam_type') }}</th>
            <th class="border px-2 py-1">{{ t('module') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(c, i) in curriculumResult.courses[activeYear][activeSem]"
            :key="i"
            class="odd:bg-white even:bg-gray-50 hover:bg-gray-200 transition"
          >
            <td class="border px-2 py-1 text-center">{{ i + 1 }}</td>
            <td class="border px-2 py-1 text-center">{{ c.block }}</td>
            <td class="border px-2 py-1 text-center">{{ c.discipline_code }}</td>
            <td class="border px-2 py-1">{{ c.discipline_name }}</td>
            <td class="border px-2 py-1">{{ c.discipline_type }}</td>
            <td class="border px-2 py-1">{{ c.prerequisite }}</td>
            <td class="border px-2 py-1 text-center">{{ c.credits }}</td>
            <td class="border px-2 py-1 text-center">{{ c.contact_hours }}</td>
            <td class="border px-2 py-1 text-center">{{ c.exam_type }}</td>
            <td class="border px-2 py-1 text-center">{{ c.module }}</td>
          </tr>
          <tr v-if="!curriculumResult.courses[activeYear][activeSem].length">
            <td colspan="5" class="border px-2 py-1 text-center italic">
              {{ t('no_courses') }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Electives -->
      <div v-if="groups.length">
        <h3 class="text-xl font-semibold mb-4">{{ t('electives') }}</h3>

        <!-- Group Tabs -->
        <div class="flex space-x-2 mb-6">
          <button
            v-for="grp in groups"
            :key="grp"
            @click="activeGroup = grp"
            :class="[
              'px-4 py-2 rounded text-white font-semibold transition',
              activeGroup === grp
                ? 'bg-blue-600 ring-2 ring-white'
                : 'bg-black hover:bg-opacity-80'
            ]"
          >
            {{ t('group') }} {{ grp }}
          </button>
        </div>

        <!-- Electives Table -->
        <table class="w-full text-sm border border-collapse mb-8">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1">№</th>
              <th class="border px-2 py-1">{{ t('block_code') }}</th>
              <th class="border px-2 py-1">{{ t('discipline_code') }}</th>
              <th class="border px-2 py-1">{{ t('discipline_name') }}</th>
              <th class="border px-2 py-1">{{ t('discipline_type') }}</th>
              <th class="border px-2 py-1">{{ t('prerequisite') }}</th>
              <th class="border px-2 py-1">{{ t('credits') }}</th>
              <th class="border px-2 py-1">{{ t('contact_hours') }}</th>
              <th class="border px-2 py-1">{{ t('exam_type') }}</th>
              <th class="border px-2 py-1">{{ t('module') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(e, i) in curriculumResult.electives[activeGroup]"
              :key="i"
              class="odd:bg-white even:bg-gray-50 hover:bg-gray-200 transition"
            >
              <td class="border px-2 py-1 text-center">{{ i + 1 }}</td>
              <td class="border px-2 py-1 text-center">{{ e.block }}</td>
              <td class="border px-2 py-1 text-center">{{ e.discipline_code }}</td>
              <td class="border px-2 py-1">{{ e.discipline_name }}</td>
              <td class="border px-2 py-1">{{ e.discipline_type }}</td>
              <td class="border px-2 py-1">{{ e.prerequisite }}</td>
              <td class="border px-2 py-1 text-center">{{ e.credits }}</td>
              <td class="border px-2 py-1 text-center">{{ e.contact_hours }}</td>
              <td class="border px-2 py-1 text-center">{{ e.exam_type }}</td>
              <td class="border px-2 py-1 text-center">{{ e.module }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <button
        @click="downloadCurriculumJSON"
        class="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700"
      >
        {{ t('download_json') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'

const transcriptFile   = ref(null)
const curriculumFile   = ref(null)
const transcriptResult = ref(null)
const curriculumResult = ref(null)
const loadingTrans     = ref(false)
const loadingCurr      = ref(false)
const error            = ref(null)
const locale           = ref(localStorage.getItem('locale') || 'ru')

const i18n = {
  ru: {
    upload_transcript_and_curriculum: 'Загрузить транскрипт и учебный план',
    transcript_upload: 'Транскрипт',
    choose_pdf: 'Выберите PDF',
    sending: 'Отправка...',
    send: 'Отправить',
    curriculum_upload: 'Учебный план',
    choose_xlsx: 'Выберите XLSX',
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
    course_name: 'Название',
    credits: 'Кредиты',
    traditional: 'Традиционная',
    retake: 'Ретейк',
    download_json: 'Скачать JSON',
    curriculum_metadata: 'Данные программы',
    intake_year: 'Год поступления',
    electives: 'Элективы',
    group: 'Группа',
    no_courses: 'Нет курсов',
    block_code: 'Код блока',
    discipline_code: 'Шифр дисциплины',
    discipline_name: 'Название программы',
    discipline_type: 'Цикл дисциплин',
    module: 'Шифр модуля',
    exam_type: 'Тип экзамена',
    contact_hours: 'Контактных часов в неделю',
    prerequisite: 'Предварительное требование',
    fall: 'Осень',
    spring: 'Весна',
    course_short: 'курс'
  },
  kz: {
    upload_transcript_and_curriculum: 'Транскрипт пен оқу жоспарын жүктеу',
    transcript_upload: 'Транскрипт',
    choose_pdf: 'PDF таңдаңыз',
    sending: 'Жіберілуде...',
    send: 'Жіберу',
    curriculum_upload: 'Оқу жоспары',
    choose_xlsx: 'XLSX таңдаңыз',
    student_info: 'Студент туралы ақпарат',
    name: 'Аты-жөні',
    faculty: 'Факультет',
    program_code: 'Бағдарлама коды',
    program_name: 'Бағдарлама атауы',
    program_group: 'Бағдарлама тобы',
    entry_year: 'Қабылдау жылы',
    language: 'Оқу тілі',
    gpa: 'Жалпы орта балл',
    total_credits: 'Жалпы кредиттер',
    courses: 'Курстар',
    course_name: 'Курс атауы',
    credits: 'Кредиттер',
    traditional: 'Дәстүрлі',
    retake: 'Қайталау',
    download_json: 'JSON жүктеу',
    curriculum_metadata: 'Оқу жоспарының деректері',
    intake_year: 'Қабылдау жылы',
    electives: 'Элективтер',
    group: 'Топ',
    no_courses: 'Курс жоқ',
    block_code: 'Блок коды',
    discipline_code: 'Дисциплина коды',
    discipline_name: 'Бағдарлама атауы',
    discipline_type: 'Дисциплина түрі',
    module: 'Модуль коды',
    exam_type: 'Емтихан түрі',
    contact_hours: 'Аптасына байланыс сағаттары',
    prerequisite: 'Алдын ала талап',
    fall: 'Күз',
    spring: 'Көктем',
    course_short: 'курс'
  },
  en: {
    upload_transcript_and_curriculum: 'Upload transcript and curriculum',
    transcript_upload: 'Transcript',
    choose_pdf: 'Choose PDF',
    sending: 'Sending...',
    send: 'Send',
    curriculum_upload: 'Curriculum',
    choose_xlsx: 'Choose XLSX',
    student_info: 'Student Info',
    name: 'Name',
    faculty: 'Faculty',
    program_code: 'Program Code',
    program_name: 'Program Name',
    program_group: 'Program Group',
    entry_year: 'Entry Year',
    language: 'Language',
    gpa: 'GPA',
    total_credits: 'Total Credits',
    courses: 'Courses',
    course_name: 'Course Name',
    credits: 'Credits',
    traditional: 'Traditional',
    retake: 'Retake',
    download_json: 'Download JSON',
    curriculum_metadata: 'Curriculum Data',
    intake_year: 'Intake Year',
    electives: 'Electives',
    group: 'Group',
    no_courses: 'No courses',
    block_code: 'Block Code',
    discipline_code: 'Discipline cipher',
    discipline_name: 'Program Name',
    discipline_type: 'Discipline Type',
    module: 'Module Code',
    exam_type: 'Exam Type',
    contact_hours: 'Contact hours per week',
    prerequisite: 'Prerequisite',
    fall: 'Fall',
    spring: 'Spring',
    course_short: 'course'
  }
}

const t = key => i18n[locale.value][key] || key
function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

function onTranscriptChange(e) {
  transcriptFile.value = e.target.files[0]
  transcriptResult.value = null
  error.value = null
}
function onCurriculumChange(e) {
  curriculumFile.value = e.target.files[0]
  curriculumResult.value = null
  error.value = null
}

async function uploadTranscript() {
  if (!transcriptFile.value) return
  loadingTrans.value = true; error.value = null
  const form = new FormData(); form.append('file', transcriptFile.value)
  try {
    const { data } = await axios.post(
      'http://localhost:8000/upload-transcript',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    transcriptResult.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loadingTrans.value = false
  }
}

async function uploadCurriculum() {
  if (!curriculumFile.value) return
  loadingCurr.value = true; error.value = null
  const form = new FormData(); form.append('file', curriculumFile.value)
  try {
    const { data } = await axios.post(
      'http://localhost:8000/upload-curriculum',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    curriculumResult.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loadingCurr.value = false
  }
}

function downloadTranscriptJSON() {
  const blob = new Blob([JSON.stringify(transcriptResult.value, null, 2)], { type: 'application/json' })
  const link = document.createElement('a'); link.href = URL.createObjectURL(blob)
  link.download = 'transcript.json'; link.click(); URL.revokeObjectURL(link.href)
}

function downloadCurriculumJSON() {
  const blob = new Blob([JSON.stringify(curriculumResult.value, null, 2)], { type: 'application/json' })
  const link = document.createElement('a'); link.href = URL.createObjectURL(blob)
  link.download = 'curriculum.json'; link.click(); URL.revokeObjectURL(link.href)
}

// Tabs data
const years = computed(() =>
  curriculumResult.value ? Object.keys(curriculumResult.value.courses) : []
)
const activeYear = ref('')
const activeSem = ref('fall')
watch(years, (y) => {
  if (y.length) activeYear.value = y[0]
})

// Electives groups
const groups = computed(() =>
  curriculumResult.value ? Object.keys(curriculumResult.value.electives) : []
)
const activeGroup = ref('')
watch(groups, (g) => {
  if (g.length) activeGroup.value = g[0]
})
</script>
