<template>
  <div class="p-6 space-y-6 text-white">
    <div class="flex gap-4">
      <button
        :class="tabClass(activeTab === 'users')"
        @click="activeTab = 'users'"
      >{{ $t('nav.users') }}</button>

      <button
        :class="tabClass(activeTab === 'transcripts')"
        @click="activeTab = 'transcripts'"
      >{{ $t('nav.transcript') }}</button>

      <button
        :class="tabClass(activeTab === 'curricula')"
        @click="activeTab = 'curricula'"
      >{{ $t('nav.curriculum') }}</button>
    </div>

    <div v-if="activeTab === 'users'">
      <AdminUserPanel />
    </div>

    <div v-if="activeTab === 'transcripts'">
      <AdminTranscriptPanel />
    </div>

    <div v-if="activeTab === 'curricula'">
      <AdminCurriculumPanel />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminUserPanel from '@/components/AdminUserPanel.vue'
import AdminTranscriptPanel from '@/components/AdminTranscriptPanel.vue'
import AdminCurriculumPanel from '@/components/AdminCurriculumPanel.vue'

const activeTab = ref('users')

const tabClass = (isActive) => [
  'px-4 py-2 font-semibold rounded transition text-white',
  isActive ? 'bg-blue-600' : 'tab-inactive'
]
</script>
<style scoped>
.tab-inactive {
  background-color: rgb(39 39 42);
}
.tab-inactive:hover {
  background-color: var (--color-zinc-800);
}
</style>