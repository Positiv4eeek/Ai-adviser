<template>
  <div v-if="data" class="space-y-8">

    <div v-if="!hideMetadata" class="bg-zinc-800 p-6 rounded-xl text-white space-y-6">
      <h2 class="text-2xl font-bold text-center">
        {{ $t('curriculum.curriculum_metadata') }}
      </h2>
      <div class="bg-zinc-700 p-4 rounded-lg max-w-md mx-auto">
        <dl class="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
          <dt class="font-medium">{{ $t('curriculum.program_code') }}</dt>
          <dd>{{ d.program.program_code }}</dd>
          <dt class="font-medium">{{ $t('curriculum.program_name') }}</dt>
          <dd>{{ d.program.program_name }}</dd>
          <dt class="font-medium">{{ $t('curriculum.intake_year') }}</dt>
          <dd>{{ d.program.intake_year }}</dd>
          <dt class="font-medium">{{ $t('curriculum.total_credits') }}</dt>
          <dd>{{ d.program.total_credits }}</dd>
        </dl>
      </div>
    </div>


    <div class="bg-zinc-800 p-6 rounded-xl text-white space-y-4">
      <h2 class="text-2xl font-bold text-center">{{ $t('courses.courses') }}</h2>

      <div class="flex flex-wrap justify-center gap-2 mb-4">
        <button @click="activeSem = 'fall'" :class="tabClass(activeSem === 'fall')">
          {{ $t('tabs.fall') }}
        </button>
        <button @click="activeSem = 'spring'" :class="tabClass(activeSem === 'spring')">
          {{ $t('tabs.spring') }}
        </button>
      </div>

      <div class="flex flex-wrap justify-center gap-2 mb-4">
        <button
          v-for="y in years"
          :key="y"
          @click="activeYear = y"
          :class="tabClass(activeYear === y)"
        >
          {{ y }} {{ $t('tabs.course_short') }}
        </button>
      </div>

      <div class="bg-zinc-800 p-0 rounded-lg overflow-auto max-h-96">
        <table class="w-full text-sm border-collapse">
          <thead class="sticky top-0 bg-neutral-900 bg-opacity-100">
            <tr>
              <th class="px-3 py-2">{{ $t('courses.headers.index') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.blockCode') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineCode') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineName') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineType') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.prerequisite') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.credits') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.contactHours') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.examType') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.module') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(c, idx) in d.courses[activeYear]?.[activeSem] || []"
              :key="idx"
              class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500"
            >
              <td class="px-3 py-2 text-center">{{ idx + 1 }}</td>
              <td class="px-3 py-2">{{ c.block }}</td>
              <td class="px-3 py-2">{{ c.discipline_code }}</td>
              <td class="px-3 py-2">{{ c.discipline_name }}</td>
              <td class="px-3 py-2">{{ c.discipline_type }}</td>
              <td class="px-3 py-2">{{ c.prerequisite }}</td>
              <td class="px-3 py-2 text-center">{{ c.credits }}</td>
              <td class="px-3 py-2 text-center">{{ c.contact_hours ?? '—' }}</td>
              <td class="px-3 py-2 text-center">{{ c.exam_type }}</td>
              <td class="px-3 py-2 text-center">{{ c.module }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


    <div v-if="groups.length" class="bg-zinc-800 p-6 rounded-xl text-white space-y-4">
      <h2 class="text-2xl font-bold text-center">{{ $t('electives.electives') }}</h2>
      <div class="flex flex-wrap justify-center gap-2 mb-4">
        <button
          v-for="grp in groups"
          :key="grp"
          @click="activeGroup = grp"
          :class="tabClass(activeGroup === grp)"
        >
          {{ $t('electives.group') }} {{ grp }}
        </button>
      </div>

      <div class="bg-zinc-700 p-0 rounded-lg overflow-auto max-h-80">
        <table class="w-full text-sm border-collapse">
          <thead class="sticky top-0 bg-neutral-900 bg-opacity-90">
            <tr>
              <th class="px-3 py-2">{{ $t('courses.headers.index') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.blockCode') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineCode') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineName') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.disciplineType') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.prerequisite') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.credits') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.contactHours') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.examType') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.module') }}</th>
              <th class="px-3 py-2">{{ $t('courses.headers.is_available') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(e, idx) in d.electives[activeGroup] || []"
              :key="idx"
              class="odd:bg-zinc-700 even:bg-zinc-600 hover:bg-zinc-500"
            >
              <td class="px-3 py-2 text-center">{{ idx + 1 }}</td>
              <td class="px-3 py-2">{{ e.block }}</td>
              <td class="px-3 py-2">{{ e.discipline_code }}</td>
              <td class="px-3 py-2">{{ e.discipline_name }}</td>
              <td class="px-3 py-2">{{ e.discipline_type }}</td>
              <td class="px-3 py-2">{{ e.prerequisite }}</td>
              <td class="px-3 py-2 text-center">{{ e.credits }}</td>
              <td class="px-3 py-2 text-center">{{ e.contact_hours ?? '—' }}</td>
              <td class="px-3 py-2 text-center">{{ e.exam_type }}</td>
              <td class="px-3 py-2 text-center">{{ e.module }}</td>
              <td class="px-3 py-2 text-center">
                <label class="inline-flex items-center cursor-default">
                  <input
                    type="checkbox"
                    :checked="e.is_available"
                    :disabled="!isAdmin"
                    @change="toggleAvailability(e)"
                    class="sr-only peer"
                  />
                  <div
                    class="w-5 h-5 rounded border border-gray-300 
                          peer-checked:bg-blue-600 peer-checked:border-blue-600 
                          transition flex items-center justify-center"
                    :class="{ 'cursor-pointer': isAdmin, 'opacity-100': !isAdmin }"
                  >
                    <svg v-if="e.is_available" class="w-3 h-3 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </label>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <p v-else class="text-white text-center mt-10">{{ $t('general.loading') }}</p>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  curriculumId: { type: [String, Number], required: true },
  hideMetadata: { type: Boolean, default: false },
  isAdmin: { type: Boolean, default: false }
})

const { t } = useI18n()

const data = ref(null)
const error = ref(null)

const d = computed(() => data.value || { program: {}, courses: {}, electives: {} })

async function fetchDetail() {
  try {
    const res = await axios.get(`/curriculum/${props.curriculumId}`)
    data.value = res.data
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
    console.error(t('curriculum.fetch_error'), error.value)
  }
}

async function toggleAvailability(elective) {
  try {
    await axios.patch(`/curriculum/elective/${elective.id}`, {
      is_available: !elective.is_available
    })
    elective.is_available = !elective.is_available
  } catch (err) {
    console.error(t('curriculum.toggle_error'), err)
  }
}

watch(() => props.curriculumId, fetchDetail, { immediate: true })

const years = computed(() => Object.keys(d.value.courses))
const activeYear = ref('')
watch(years, v => { if (v.length) activeYear.value = v[0] })

const activeSem = ref('fall')

const groups = computed(() => Object.keys(d.value.electives))
const activeGroup = ref('')
watch(groups, v => { if (v.length) activeGroup.value = v[0] })

const tabClass = isActive => [
  'px-4 py-2 rounded text-white font-semibold transition',
  isActive ? 'bg-blue-600 ring-2 ring-white' : 'bg-black hover:bg-opacity-80'
]
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
