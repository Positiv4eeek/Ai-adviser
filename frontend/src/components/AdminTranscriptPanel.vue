<template>
  <div class="space-y-6">

    <TranscriptList @select="selectTranscript" />
    <hr class="border-gray-700" />

    <div v-if="selectedId">
      <TranscriptDetail :transcript-id="selectedId" />
      <div class="text-center mt-4 space-x-4">
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
import TranscriptList from '@/components/TranscriptList.vue'
import TranscriptDetail from '@/components/TranscriptDetail.vue'

const selectedId = ref(null)

function selectTranscript(id) {
  selectedId.value = id
}
</script>
