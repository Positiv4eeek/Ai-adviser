<template>
  <div class="space-y-6">

    <UploadCurriculum />
    <hr class="border-gray-700" />

    <CurriculumList @select="selectCurriculum" />
    <hr class="border-gray-700" />

    <div v-if="selectedId" class="mt-4">
      <CurriculumDetail v-if="selectedId" :curriculum-id="selectedId" :is-admin="userRole === 'admin'" />
      <div class="text-center mt-4">
        <button
          @click="selectedId = null"
          class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
        >
          {{ $t('general.hide_details') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import UploadCurriculum from '@/components/UploadCurriculum.vue'
import CurriculumList from '@/components/CurriculumList.vue'
import CurriculumDetail from '@/components/CurriculumDetail.vue'

const selectedId = ref(null)
const userRole = ref(null)

const selectCurriculum = (id) => {
  selectedId.value = id
}

onMounted(async () => {
  try {
    const { data } = await axios.get('/auth/me')
    userRole.value = data.role
  } catch (err) {
    console.error('Ошибка при получении роли:', err)
  }
})
</script>
