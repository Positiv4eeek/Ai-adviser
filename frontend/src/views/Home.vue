<template>
  <div class="p-8 max-w-xl mx-auto text-white space-y-6">
    <h1 class="text-3xl font-bold">{{ $t('home.welcome') }}</h1>

    <p class="text-lg">
      {{ $t('home.intro') }}
    </p>

    <div class="text-lg">
      <p>
        {{ $t('home.prompt') }}
        <router-link to="/login" class="text-blue-500 underline hover:text-blue-400">{{ $t('nav.login') }}</router-link>
        {{ $t('home.or') }}
        <router-link to="/register" class="text-blue-500 underline hover:text-blue-400">{{ $t('nav.register') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<style scoped>
</style>
