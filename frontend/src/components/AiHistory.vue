<template>
  <div class="space-y-4 max-w-4xl mx-auto">
    <div v-if="loading">{{ $t('dashboard.loading') }}</div>
    <div v-else-if="logs.length === 0">{{ $t('dashboard.no_history') }}</div>

    <div v-else class="space-y-4">
      <div
        v-for="log in logs"
        :key="log.id"
        class="p-4 rounded bg-zinc-800 border border-zinc-700 transition-all duration-300"
      >
        <div class="flex justify-between">
          <div class="flex flex-col">
            <span class="text-sm text-gray-400">
              {{ log.student_name }}:
              <strong class="text-white">{{ log.prompt_name }}</strong>
            </span>
            <span class="text-xs text-gray-500 mt-1 text-left">
              {{ log.specialty }} {{ log.entry_year }}
            </span>
            <span class="text-xs text-gray-500 mt-1 text-left">
              {{ new Date(log.created_at).toLocaleString() }}
            </span>
          </div>

          <button
            class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
            @click="toggleDetails(log.id)"
          >
            {{ expandedLogs.has(log.id) ? $t('dashboard.hide_details') : $t('dashboard.show_details') }}
          </button>
        </div>

        <transition name="fade">
          <div v-if="expandedLogs.has(log.id)" class="mt-3 space-y-3">

            <div v-if="isValidJSON(log.response)">
              <div class="bg-zinc-900 p-4 rounded border border-zinc-700 space-y-4">

                <div v-if="parsedResponse.courses?.length">
                  <h4 class="text-white text-base font-semibold mb-2">{{ $t('dashboard.recommended_courses') }}</h4>
                  <div
                    v-for="course in parsedResponse.courses"
                    :key="course.code"
                    class="border border-zinc-700 rounded px-3 py-2 bg-zinc-800 mb-2"
                  >
                    <div class="flex justify-between items-center">
                      <div>
                        <span class="text-white font-medium">{{ course.name }}</span>
                        <span>&nbsp;</span>
                        <span class="text-gray-400 text-sm">({{ course.code }}, {{ course.credits }} ECTS)</span>
                      </div>
                      <span
                        class="text-xs rounded px-2 py-0.5"
                        :class="{
                          'bg-blue-600 text-white': course.type === 'required',
                          'bg-green-600 text-white': course.type === 'elective',
                          'bg-orange-500 text-white': course.type === 'repeat'
                        }"
                      >
                        {{ $t('dashboard.course_type_' + course.type) }}
                      </span>
                    </div>
                    <div class="text-gray-300 text-sm mt-1 text-left">{{ course.reason }}</div>
                    <div v-if="course.prerequisites_met?.length" class="text-gray-500 text-xs mt-1">
                      {{ $t('dashboard.prerequisites') }}: {{ course.prerequisites_met.join(', ') }}
                    </div>
                  </div>
                </div>

                <div v-if="parsedResponse.comment">
                  <h4 class="text-yellow-400 font-bold mt-4 mb-1">{{ $t('dashboard.comment') }}</h4>
                  <p class="text-gray-300 text-sm leading-relaxed whitespace-pre-line border-l-4 border-yellow-400 pl-4">
                    {{ parsedResponse.comment }}
                  </p>
                </div>
              </div>
            </div>

            <div v-else>
              <p class="text-red-500 text-sm">{{ $t('dashboard.json_error') }}</p>
              <pre class="bg-zinc-900 p-2 rounded text-xs text-gray-400 font-mono whitespace-pre-wrap max-h-64 overflow-y-auto">
                {{ log.response }}
              </pre>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const logs = ref([])
const loading = ref(true)
const expandedLogs = ref(new Set())
const parsedResponse = ref({})

const toggleDetails = (id) => {
  if (expandedLogs.value.has(id)) {
    expandedLogs.value.delete(id)
  } else {
    expandedLogs.value.add(id)
  }
}

function isValidJSON(json) {
  try {
    parsedResponse.value = JSON.parse(json)
    return true
  } catch {
    parsedResponse.value = {}
    return false
  }
}

onMounted(async () => {
  try {
    const res = await axios.get('/ai/recommendations/history')
    logs.value = res.data
  } catch (e) {
    console.error(e)
    logs.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}
</style>
