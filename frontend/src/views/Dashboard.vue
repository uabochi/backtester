<template>
  <div class="dashboard">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome back, {{ userName }}!
        </h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Here's an overview of your trading activities
        </p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div
                class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-green-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Total Backtests
              </p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ stats.totalBacktests }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div
                class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-blue-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Active Strategies
              </p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ stats.activeStrategies }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div
                class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-yellow-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Total P&L
              </p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                ${{ stats.totalPnL.toFixed(2) }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div
                class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-purple-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Win Rate
              </p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ stats.winRate.toFixed(1) }}%
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Recent Backtests -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">
              Recent Backtests
            </h3>
            <router-link
              to="/backtest"
              class="text-primary-600 hover:text-primary-500 text-sm font-medium"
            >
              View all →
            </router-link>
          </div>

          <div v-if="recentBacktests.length === 0" class="text-center py-8">
            <svg
              class="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              No backtests yet
            </p>
            <router-link
              to="/backtest"
              class="mt-2 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-primary-600 bg-primary-50 hover:bg-primary-100 dark:bg-primary-900/20 dark:text-primary-400"
            >
              Start your first backtest
            </router-link>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="backtest in recentBacktests"
              :key="backtest.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg dark:bg-gray-800"
            >
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ backtest.strategy }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ backtest.symbol }} • {{ backtest.date }}
                </p>
              </div>
              <div class="text-right">
                <p
                  class="text-sm font-medium"
                  :class="backtest.pnl >= 0 ? 'text-green-600' : 'text-red-600'"
                >
                  {{ backtest.pnl >= 0 ? "+" : ""
                  }}{{ backtest.pnl.toFixed(2) }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ backtest.status }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Quick Actions
          </h3>

          <div class="space-y-3">
            <router-link
              to="/backtest"
              class="flex items-center p-3 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors duration-200 dark:bg-primary-900/20"
            >
              <div class="flex-shrink-0">
                <svg
                  class="w-6 h-6 text-primary-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="ml-3">
                <p
                  class="text-sm font-medium text-primary-900 dark:text-primary-100"
                >
                  Run New Backtest
                </p>
                <p class="text-xs text-primary-700 dark:text-primary-300">
                  Test a trading strategy
                </p>
              </div>
            </router-link>

            <router-link
              to="/strategies"
              class="flex items-center p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors duration-200 dark:bg-blue-900/20"
            >
              <div class="flex-shrink-0">
                <svg
                  class="w-6 h-6 text-blue-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-blue-900 dark:text-blue-100">
                  Create Strategy
                </p>
                <p class="text-xs text-blue-700 dark:text-blue-300">
                  Build a new trading strategy
                </p>
              </div>
            </router-link>

            <button
              @click="showTutorial"
              class="flex items-center w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 dark:bg-gray-800 dark:hover:bg-gray-700"
            >
              <div class="flex-shrink-0">
                <svg
                  class="w-6 h-6 text-gray-600 dark:text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  Help & Tutorials
                </p>
                <p class="text-xs text-gray-600 dark:text-gray-400">
                  Learn how to use Traders Casa
                </p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

const authStore = useAuthStore();
const toast = useToast();

const userName = computed(() => {
  return authStore.user?.name?.split(" ")[0] || "Trader";
});

const stats = ref({
  totalBacktests: 0,
  activeStrategies: 0,
  totalPnL: 0,
  winRate: 0,
});

const recentBacktests = ref([]);

const showTutorial = () => {
  toast.info("Tutorial feature coming soon!");
};

onMounted(async () => {
  // Load dashboard data
  try {
    const response = await fetch("/api/dashboard/stats", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      stats.value = data.stats;
      recentBacktests.value = data.recentBacktests;
    }
  } catch (error) {
    console.error("Failed to load dashboard data:", error);
  }
});
</script>
