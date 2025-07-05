<template>
  <div class="p-6 max-w-5xl mx-auto bg-white min-h-screen text-gray-900">

    <!-- Title -->
    <h2 class="text-2xl font-bold mb-6 text-center">
      {{ $t('upload.upload_transcript_and_curriculum') }}
    </h2>

    <!-- Upload Panels -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <!-- Transcript Upload -->
      <div class="space-y-4">
        <h3 class="font-semibold text-lg mb-2">
          {{ $t('upload.transcript_upload') }}
        </h3>
        <label
          for="trans-upload"
          class="cursor-pointer flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded border border-dashed border-gray-400"
        >
          <span>
            {{ transcriptFile?.name || $t('upload.choose_pdf') }}
          </span>
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
          {{ loadingTrans ? $t('upload.sending') : $t('upload.send') }}
        </button>
      </div>

      <!-- Curriculum Upload -->
      <div class="space-y-4">
        <h3 class="font-semibold text-lg mb-2">
          {{ $t('upload.curriculum_upload') }}
        </h3>
        <label
          for="curr-upload"
          class="cursor-pointer flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded border border-dashed border-gray-400"
        >
          <span>
            {{ curriculumFile?.name || $t('upload.choose_xlsx') }}
          </span>
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
          {{ loadingCurr ? $t('upload.sending') : $t('upload.send') }}
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="text-red-500 mb-6">{{ error }}</div>

    <!-- Transcript Result -->
    <div v-if="transcriptResult" class="mb-12">
      <h3 class="text-xl font-semibold mb-4">{{ $t('student.student_info') }}</h3>
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-gray-50 p-4 rounded shadow mb-6">
        <div><dt class="font-medium">{{ $t('student.name') }}</dt><dd>{{ transcriptResult.student_info.name }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.faculty') }}</dt><dd>{{ transcriptResult.student_info.faculty }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.program_code') }}</dt><dd>{{ transcriptResult.student_info.program_code }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.program_name') }}</dt><dd>{{ transcriptResult.student_info.program_name }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.program_group') }}</dt><dd>{{ transcriptResult.student_info.program_group }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.entry_year') }}</dt><dd>{{ transcriptResult.student_info.entry_year }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.language') }}</dt><dd>{{ transcriptResult.student_info.language }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.gpa') }}</dt><dd>{{ transcriptResult.student_info.gpa }}</dd></div>
        <div><dt class="font-medium">{{ $t('student.total_credits') }}</dt><dd>{{ transcriptResult.student_info.total_credits }}</dd></div>
      </dl>

      <h3 class="text-xl font-semibold mb-2">{{ $t('courses.courses') }}</h3>
      <table class="w-full text-sm border border-collapse mb-4">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">{{ $t('courses.headers.index') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.disciplineName') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.credits') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.percent') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.traditional') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.retake') }}</th>
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
        {{ $t('general.download_json') }}
      </button>
    </div>

    <!-- Curriculum Result & Electives -->
    <div v-if="curriculumResult">
      <h3 class="text-xl font-semibold mb-4">{{ $t('curriculum.curriculum_metadata') }}</h3>
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-gray-50 p-4 rounded shadow mb-6">
        <div><dt class="font-medium">{{ $t('courses.headers.blockCode') }}</dt><dd>{{ curriculumResult.program.program_code }}</dd></div>
        <div><dt class="font-medium">{{ $t('curriculum.intake_year') }}</dt><dd>{{ curriculumResult.program.intake_year }}</dd></div>
        <div><dt class="font-medium">{{ $t('curriculum.total_credits') }}</dt><dd>{{ curriculumResult.program.total_credits }}</dd></div>
      </dl>

      <!-- Course Year Tabs -->
      <div class="flex space-x-2 mb-4">
        <button
          v-for="y in years"
          :key="y"
          @click="activeYear = y"
          :class="yearBtnClass(y === activeYear)"
        >
          {{ y }} {{ $t('tabs.course_short') }}
        </button>
      </div>

      <!-- Semester Tabs -->
      <div class="flex space-x-2 mb-6">
        <button
          @click="activeSem = 'fall'"
          :class="yearBtnClass(activeSem === 'fall')"
        >
          {{ $t('tabs.fall') }}
        </button>
        <button
          @click="activeSem = 'spring'"
          :class="yearBtnClass(activeSem === 'spring')"
        >
          {{ $t('tabs.spring') }}
        </button>
      </div>

      <!-- Curriculum Table -->
      <table class="w-full text-sm border border-collapse mb-8">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">{{ $t('courses.headers.index') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.blockCode') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.disciplineCode') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.disciplineName') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.disciplineType') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.prerequisite') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.credits') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.contactHours') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.examType') }}</th>
            <th class="border px-2 py-1">{{ $t('courses.headers.module') }}</th>
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
            <td colspan="10" class="border px-2 py-1 text-center italic">
              {{ $t('general.no_courses') }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Electives -->
      <div v-if="groups.length">
        <h3 class="text-xl font-semibold mb-4">{{ $t('electives.electives') }}</h3>
        <div class="flex space-x-2 mb-6">
          <button
            v-for="grp in groups"
            :key="grp"
            @click="activeGroup = grp"
            :class="yearBtnClass(activeGroup === grp)"
          >
            {{ $t('electives.group') }} {{ grp }}
          </button>
        </div>
        <table class="w-full text-sm border border-collapse mb-8">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1">{{ $t('courses.headers.index') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.blockCode') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.disciplineCode') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.disciplineName') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.disciplineType') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.prerequisite') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.credits') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.contactHours') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.examType') }}</th>
              <th class="border px-2 py-1">{{ $t('courses.headers.module') }}</th>
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
        <button
          @click="downloadCurriculumJSON"
          class="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700"
        >
          {{ $t('general.download_json') }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t, locale } = useI18n()


const transcriptFile   = ref(null)
const curriculumFile   = ref(null)
const transcriptResult = ref(null)
const curriculumResult = ref(null)
const loadingTrans     = ref(false)
const loadingCurr      = ref(false)
const error            = ref(null)


const years      = computed(() => curriculumResult.value ? Object.keys(curriculumResult.value.courses) : [])
const activeYear = ref('')
watch(years, val => { if (val.length) activeYear.value = val[0] })

const activeSem = ref('fall')

const groups      = computed(() => curriculumResult.value ? Object.keys(curriculumResult.value.electives) : [])
const activeGroup = ref('')
watch(groups, val => { if (val.length) activeGroup.value = val[0] })


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
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'transcript.json'
  link.click()
}
function downloadCurriculumJSON() {
  const blob = new Blob([JSON.stringify(curriculumResult.value, null, 2)], { type: 'application/json' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'curriculum.json'
  link.click()
}

const yearBtnClass = isActive => (
  [
    'px-4 py-2 rounded text-white font-semibold transition',
    isActive
      ? 'bg-blue-600 ring-2 ring-white'
      : 'bg-black hover:bg-opacity-80'
  ]
)
</script>

<style scoped>

</style>
