<template>
  <div class="p-6 space-y-6">
    <h2 class="text-2xl font-bold text-center">{{ $t('curriculum.choose_plan') }}</h2>

    <select v-model="selectedId" @change="fetchDetail" class="p-2 rounded bg-zinc-800 text-white">
      <option value="" disabled>{{ $t('curriculum.select_placeholder') }}</option>
      <option v-for="c in curricula" :key="c.id" :value="c.id">
        {{ c.program_code }} – {{ c.program_name }} ({{ c.intake_year }}) ({{ c.language }})
      </option>
    </select>

    <div v-if="detail">
      <CurriculumDetail :data="detail" />
    </div>

    <p v-if="loading" class="text-center">{{ $t('general.loading') }}</p>
    <p v-if="error" class="text-red-500 text-center">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CurriculumDetail from '@/views/CurriculumDetail.vue'

const curricula  = ref([])
const selectedId = ref('')
const detail     = ref(null)
const loading    = ref(false)
const error      = ref('')

onMounted(async () => {
  try {
    const { data } = await axios.get('/curriculum')
    curricula.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  }
})

async function fetchDetail() {
  if (!selectedId.value) return
  loading.value = true
  error.value = detail.value = null
  try {
    const { data } = await axios.get(`/curriculum/${selectedId.value}`)
    detail.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
</style>
