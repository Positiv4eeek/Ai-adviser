<template>
  <div class="p-6 space-y-8">

    <div class="bg-zinc-800 p-6 rounded-xl text-white space-y-4">
      <h2 class="text-2xl font-bold text-center">{{ $t('upload.upload_curriculum') }}</h2>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <label
          for="curr-upload"
          class="flex-1 bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded border border-dashed border-gray-600 text-center cursor-pointer min-w-0"
        >
          {{ curriculumFile?.name || $t('upload.choose_xlsx') }}
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
          :disabled="!curriculumFile || loading"
          class="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded"
        >
          {{ loading ? $t('general.loading') : $t('upload.send') }}
        </button>
      </div>
      <p v-if="error" class="text-red-500 text-center">{{ error }}</p>
    </div>


    <div v-if="curriculumResult" class="w-fit bg-zinc-800 p-6 rounded-xl text-white space-y-6 mx-auto">
      <div class="flex flex-col md:flex-row gap-6 justify-center">

        <div class="bg-zinc-700 p-4 rounded-lg flex-1 max-w-md">
          <h3 class="text-xl font-semibold mb-4 text-center border-b border-zinc-600 pb-2">{{ $t('curriculum.curriculum_metadata') }}</h3>
          <dl class="space-y-3 text-sm">
            <div>
              <dt class="font-medium">{{ $t('curriculum.program_code') }}</dt>
              <dd>{{ curriculumResult.program.program_code }}</dd>
            </div>
            <div>
              <dt class="font-medium">{{ $t('curriculum.program_name') }}</dt>
              <dd>{{ curriculumResult.program.program_name }}</dd>
            </div>
            <div>
              <dt class="font-medium">{{ $t('curriculum.intake_year') }}</dt>
              <dd>{{ curriculumResult.program.intake_year }}</dd>
            </div>
            <div>
              <dt class="font-medium">{{ $t('curriculum.total_credits') }}</dt>
              <dd>{{ curriculumResult.program.total_credits }}</dd>
            </div>
          </dl>
        </div>

        <div class= "w-full bg-zinc-700 p-4 rounded-lg flex-1">
          <h3 class="text-xl font-semibold mb-4 text-center border-b border-zinc-600 pb-2">{{ $t('courses.courses') }}</h3>

          <div class="flex flex-wrap gap-2 mb-4">
            <button
              @click="activeSem = 'fall'"
              :class="tabClass(activeSem === 'fall')"
            >
              {{ $t('tabs.fall') }}
            </button>
            <button
              @click="activeSem = 'spring'"
              :class="tabClass(activeSem === 'spring')"
            >
              {{ $t('tabs.spring') }}
            </button>
          </div>
          <div class="flex flex-wrap gap-2 mb-4">
            <button
              v-for="y in years"
              :key="y"
              @click="activeYear = y"
              :class="tabClass(activeYear === y)"
            >
              {{ y }} {{ $t('tabs.course_short') }}
            </button>
          </div>

          <div class="overflow-auto max-h-96">
            <table class="w-full text-sm border-collapse">
              <thead class="sticky top-0 bg-zinc-800 bg-opacity-90">
                <tr>
                  <th class="px-3 py-2 font-medium text-white">{{ $t('courses.headers.index') }}</th>
                  <th class="px-3 py-2 font-medium text-white">{{ $t('courses.headers.blockCode') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineCode') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineName') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineType') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.prerequisite') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.credits') }}</th>
                  <!-- <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.contactHours') }}</th> -->
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.examType') }}</th>
                  <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.module') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(c,i) in curriculumResult.courses[activeYear][activeSem]"
                  :key="i"
                  class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500 transition-colors"
                >
                  <td class="px-3 py-2 text-center">{{ i + 1 }}</td>
                  <td class="px-3 py-2 text-center">{{ c.block }}</td>
                  <td class="px-3 py-2 text-center">{{ c.discipline_code }}</td>
                  <td class="px-3 py-2">{{ c.discipline_name }}</td>
                  <td class="px-3 py-2">{{ c.discipline_type }}</td>
                  <td class="px-3 py-2">{{ c.prerequisite || '—' }}</td>
                  <td class="px-3 py-2 text-center">{{ c.credits }}</td>
                  <!-- <td class="px-3 py-2 text-center">{{ c.contact_hours }}</td> -->
                  <td class="px-3 py-2 text-center">{{ c.exam_type }}</td>
                  <td class="px-3 py-2 text-center">{{ c.module }}</td>
                </tr>
                <tr v-if="!curriculumResult.courses[activeYear][activeSem].length">
                  <td colspan="10" class="border px-2 py-1 text-center italic">
                    {{ $t('general.no_courses') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>


      <div v-if="groups.length" class="bg-zinc-700 p-4 rounded-lg flex-1 space-y-4">
        <h3 class="text-xl font-semibold mb-4 text-center border-b border-zinc-600 pb-2">{{ $t('electives.electives') }}</h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="grp in groups"
            :key="grp"
            @click="activeGroup = grp"
            :class="tabClass(activeGroup === grp)"
          >
            {{ $t('electives.group') }} {{ grp }}
          </button>
        </div>
        <div class="overflow-auto max-h-80">
          <table class="w-full text-sm border-collapse">
            <thead class="sticky top-0 bg-zinc-800 bg-opacity-90">
              <tr>
                <th class="px-3 py-2 font-medium text-white">{{ $t('courses.headers.index') }}</th>
                <th class="px-3 py-2 font-medium text-white">{{ $t('courses.headers.blockCode') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineCode') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineName') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.disciplineType') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.prerequisite') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.credits') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.contactHours') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.examType') }}</th>
                <th class="px-3 py-2 text-center font-medium text-white">{{ $t('courses.headers.module') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(e,i) in curriculumResult.electives[activeGroup]"
                :key="i"
                class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500 transition-colors"
              >
                <td class="px-3 py-2 text-center">{{ i + 1 }}</td>
                <td class="px-3 py-2 text-center">{{ e.block }}</td>
                <td class="px-3 py-2 text-center">{{ e.discipline_code }}</td>
                <td class="px-3 py-2">{{ e.discipline_name }}</td>
                <td class="px-3 py-2">{{ e.discipline_type }}</td>
                <td class="px-3 py-2">{{ e.prerequisite || '—' }}</td>
                <td class="px-3 py-2 text-center">{{ e.credits }}</td>
                <td class="px-3 py-2 text-center">{{ e.contact_hours }}</td>
                <td class="px-3 py-2 text-center">{{ e.exam_type }}</td>
                <td class="px-3 py-2 text-center">{{ e.module }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>


      <div class="text-center">
        <button
          @click="downloadCurriculumJSON"
          class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded"
        >
          {{ $t('general.download_json') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'

const curriculumFile   = ref(null)
const curriculumResult = ref(null)
const loading          = ref(false)
const error            = ref('')

const years      = computed(() =>
  curriculumResult.value ? Object.keys(curriculumResult.value.courses) : []
)
const activeYear = ref('')
watch(years, y => { if (y.length) activeYear.value = y[0] })

const activeSem   = ref('fall')
const groups      = computed(() =>
  curriculumResult.value ? Object.keys(curriculumResult.value.electives) : []
)
const activeGroup = ref('')
watch(groups, g => { if (g.length) activeGroup.value = g[0] })

function onCurriculumChange(e) {
  curriculumFile.value = e.target.files[0]
  curriculumResult.value = null
  error.value = null
}

async function uploadCurriculum() {
  if (!curriculumFile.value) return
  loading.value = true; error.value = null
  const form = new FormData()
  form.append('file', curriculumFile.value)
  try {
    const { data } = await axios.post('/upload-curriculum', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    curriculumResult.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
}

function downloadCurriculumJSON() {
  const blob = new Blob([JSON.stringify(curriculumResult.value, null, 2)], {
    type: 'application/json'
  })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'curriculum.json'
  link.click()
}

const tabClass = isActive => [
  'px-4 py-2 rounded text-white font-semibold transition',
  isActive
    ? 'bg-blue-600 ring-2 ring-white'
    : 'bg-black hover:bg-opacity-80'
]
</script>

<style scoped>
.overflow-auto::-webkit-scrollbar {
  height: 8px;
}
.overflow-auto::-webkit-scrollbar-thumb {
  background-color: rgba(255,255,255,0.2);
  border-radius: 4px;
}
</style>
