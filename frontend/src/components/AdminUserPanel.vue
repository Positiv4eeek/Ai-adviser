<template>
  <div class="space-y-4 bg-zinc-800 p-6 rounded-xl text-white">
    <h2 class="text-xl font-bold">{{ $t('admin.users_title') }}</h2>

    <input
      v-model="search"
      type="text"
      :placeholder="$t('admin.search_user_placeholder')"
      class="mb-4 p-2 rounded w-full bg-zinc-700 text-white placeholder-gray-400"
    />

    <div v-if="loading">{{ $t('general.loading') }}</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <table class="w-full text-sm border-collapse" v-if="filteredUsers.length">
      <thead>
        <tr class="bg-zinc-700">
          <th class="px-3 py-2">{{ $t('admin.id') }}</th>
          <th class="px-3 py-2">{{ $t('admin.name') }}</th>
          <th class="px-3 py-2">{{ $t('admin.email')}}</th>
          <th class="px-3 py-2">{{ $t('admin.role') }}</th>
          <th class="px-3 py-2">{{ $t('admin.registered_at') }}</th>
          <th class="px-3 py-2 text-center">{{ $t('general.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in filteredUsers"
          :key="user.id"
          class="hover:bg-zinc-600"
        >
          <td class="px-3 py-2">{{ user.id }}</td>
          <td class="px-3 py-2">{{ user.first_name }} {{ user.last_name }}</td>
          <td class="px-3 py-2">{{ user.email }}</td>
          <td class="px-3 py-2 capitalize">{{ user.role }}</td>
          <td class="px-3 py-2">{{ new Date(user.created_at).toLocaleDateString() }}</td>
          <td class="px-3 py-2 text-center">
            <div class="flex justify-center gap-2">
              <button
                @click="toggleRole(user)"
                class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded"
              >
                {{ $t('admin.toggle_role') }}
              </button>
              <button
                @click="deleteUser(user.id)"
                class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
              >
                {{ $t('general.delete') }}
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="text-center text-gray-400">{{ $t('admin.no_users') }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const users = ref([])
const search = ref('')
const error = ref('')
const loading = ref(false)

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await axios.get('/admin/users')
    users.value = data
  } catch (e) {
    error.value = t('admin.error_fetch')
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  const query = search.value.toLowerCase()
  return users.value.filter(user => {
    const fullName = `${user.first_name} ${user.last_name}`.toLowerCase()
    return (
      fullName.includes(query) ||
      user.email.toLowerCase().includes(query) ||
      user.role.toLowerCase().includes(query) ||
      user.id.toLowerCase().includes(query)
    )
  })
})

async function toggleRole(user) {
  const newRole = user.role === 'admin' ? 'student' : 'admin'
  try {
    await axios.patch(`/admin/users/${user.id}`, { role: newRole })
    await fetchUsers()
  } catch (e) {
    error.value = t('admin.error_toggle_role')
  }
}

async function deleteUser(id) {
  if (!confirm(t('admin.confirm_delete_user'))) return
  try {
    await axios.delete(`/admin/users/${id}`)
    users.value = users.value.filter(u => u.id !== id)
  } catch (e) {
    error.value = t('admin.error_delete')
  }
}

onMounted(fetchUsers)
</script>
