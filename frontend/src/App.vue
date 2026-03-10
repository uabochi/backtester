<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation Header -->
    <AppHeader v-if="isAuthenticated" />

    <!-- Main Content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Toast Notifications -->
    <ToastContainer />
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import AppHeader from "@/components/layout/AppHeader.vue";
import ToastContainer from "@/components/ui/ToastContainer.vue";

const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);

onMounted(() => {
  // Check for existing token on app load
  const token = localStorage.getItem("token");
  if (token) {
    authStore.setToken(token);
  }
});
</script>

<style>
/* Global styles are now handled by Tailwind CSS */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
