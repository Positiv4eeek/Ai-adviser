<template>
  <div class="space-y-6">

    <UploadCurriculum />
    <hr class="border-gray-700" />

    <CurriculumList @select="selectCurriculum" />

    <div v-if="selectedId" class="mt-4">
      <CurriculumDetail v-if="selectedId" :curriculum-id="selectedId" />
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
import { ref } from 'vue'
import UploadCurriculum from '@/components/UploadCurriculum.vue'
import CurriculumList from '@/components/CurriculumList.vue'
import CurriculumDetail from '@/components/CurriculumDetail.vue'

const selectedId = ref(null)

const selectCurriculum = (id) => {
  selectedId.value = id
}
</script>
