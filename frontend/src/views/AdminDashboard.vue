<template>
  <div class="p-6 space-y-6 text-white">
    <h2 class="text-4xl font-bold">{{ $t('nav.dashboard') }}</h2>
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

      <button
        :class="tabClass(activeTab === 'prompts')"
        @click="activeTab = 'prompts'"
      >{{ $t('nav.prompts') }}</button>
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
    <div v-if="activeTab === 'prompts'">
      <AdminPromptPanel />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminUserPanel from '@/components/AdminUserPanel.vue'
import AdminTranscriptPanel from '@/components/AdminTranscriptPanel.vue'
import AdminCurriculumPanel from '@/components/AdminCurriculumPanel.vue'
import AdminPromptPanel from '@/components/AdminPromptPanel.vue'

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