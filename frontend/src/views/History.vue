<template>
  <div class="history-view">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Backtest History
          </h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            View and analyze your past backtest results
          </p>
        </div>

        <div class="flex items-center space-x-4">
          <!-- Filter Dropdown -->
          <select v-model="filterStatus" class="input w-40">
            <option value="all">All Status</option>
            <option value="completed">Completed</option>
            <option value="running">Running</option>
            <option value="failed">Failed</option>
          </select>

          <!-- Search -->
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search backtests..."
              class="input pl-10 w-64"
            />
            <svg
              class="absolute left-3 top-3 h-4 w-4 text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
      </div>

      <!-- Backtest List -->
      <div class="space-y-4">
        <div
          v-for="backtest in filteredBacktests"
          :key="backtest.id"
          class="card hover:shadow-lg transition-shadow duration-200"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <!-- Status Indicator -->
              <div
                class="w-3 h-3 rounded-full"
                :class="{
                  'bg-green-500': backtest.status === 'completed',
                  'bg-blue-500': backtest.status === 'running',
                  'bg-red-500': backtest.status === 'failed',
                }"
              ></div>

              <div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ backtest.strategyName }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ backtest.symbol }} • {{ backtest.timeframe }} •
                  {{ new Date(backtest.createdAt).toLocaleDateString() }}
                </p>
              </div>
            </div>

            <!-- Results Summary -->
            <div v-if="backtest.status === 'completed'" class="text-right">
              <div class="flex items-center space-x-6">
                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Total Return
                  </p>
                  <p
                    class="text-lg font-semibold"
                    :class="
                      backtest.totalReturn >= 0
                        ? 'text-green-600'
                        : 'text-red-600'
                    "
                  >
                    {{ backtest.totalReturn >= 0 ? "+" : ""
                    }}{{ backtest.totalReturn.toFixed(2) }}%
                  </p>
                </div>

                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Win Rate
                  </p>
                  <p
                    class="text-lg font-semibold text-gray-900 dark:text-white"
                  >
                    {{ backtest.winRate.toFixed(1) }}%
                  </p>
                </div>

                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">Trades</p>
                  <p
                    class="text-lg font-semibold text-gray-900 dark:text-white"
                  >
                    {{ backtest.totalTrades }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Progress for Running Backtests -->
            <div v-else-if="backtest.status === 'running'" class="text-right">
              <div class="w-32">
                <div
                  class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-1"
                >
                  <span>Progress</span>
                  <span>{{ backtest.progress }}%</span>
                </div>
                <div
                  class="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700"
                >
                  <div
                    class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: backtest.progress + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center space-x-2">
              <button
                @click="viewBacktest(backtest)"
                class="btn-secondary text-sm"
              >
                View Details
              </button>

              <button
                v-if="backtest.status === 'completed'"
                @click="reRunBacktest(backtest)"
                class="btn-primary text-sm"
              >
                Re-run
              </button>

              <button
                @click="deleteBacktest(backtest)"
                class="text-red-600 hover:text-red-800 p-2"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Additional Details (Expandable) -->
          <div
            v-if="expandedBacktest === backtest.id"
            class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700"
          >
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- Performance Metrics -->
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">
                  Performance
                </h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Sharpe Ratio</span
                    >
                    <span>{{ backtest.sharpeRatio?.toFixed(2) || "N/A" }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Max Drawdown</span
                    >
                    <span
                      >{{ backtest.maxDrawdown?.toFixed(2) || "N/A" }}%</span
                    >
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Profit Factor</span
                    >
                    <span>{{
                      backtest.profitFactor?.toFixed(2) || "N/A"
                    }}</span>
                  </div>
                </div>
              </div>

              <!-- Trade Statistics -->
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">
                  Trades
                </h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Winning Trades</span
                    >
                    <span>{{ backtest.winningTrades || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Losing Trades</span
                    >
                    <span>{{ backtest.losingTrades || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Avg Win</span
                    >
                    <span>{{ backtest.avgWin?.toFixed(2) || "N/A" }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400"
                      >Avg Loss</span
                    >
                    <span>{{ backtest.avgLoss?.toFixed(2) || "N/A" }}%</span>
                  </div>
                </div>
              </div>

              <!-- Parameters -->
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">
                  Parameters
                </h4>
                <div class="space-y-2 text-sm">
                  <div
                    v-for="(value, key) in backtest.parameters"
                    :key="key"
                    class="flex justify-between"
                  >
                    <span class="text-gray-600 dark:text-gray-400">{{
                      key
                    }}</span>
                    <span>{{ value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="filteredBacktests.length === 0"
          class="card text-center py-12"
        >
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
              d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No backtests found
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{
              searchQuery || filterStatus !== "all"
                ? "Try adjusting your filters."
                : "Start your first backtest to see results here."
            }}
          </p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center mt-8">
        <nav class="flex items-center space-x-2">
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="btn-secondary disabled:opacity-50"
          >
            Previous
          </button>

          <span class="text-sm text-gray-600 dark:text-gray-400">
            Page {{ currentPage }} of {{ totalPages }}
          </span>

          <button
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="btn-secondary disabled:opacity-50"
          >
            Next
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

const toast = useToast();
const router = useRouter();

const backtests = ref([]);
const expandedBacktest = ref(null);
const searchQuery = ref("");
const filterStatus = ref("all");
const currentPage = ref(1);
const pageSize = ref(10);
const totalPages = ref(1);

const filteredBacktests = computed(() => {
  let filtered = backtests.value;

  // Filter by status
  if (filterStatus.value !== "all") {
    filtered = filtered.filter((bt) => bt.status === filterStatus.value);
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (bt) =>
        bt.strategyName.toLowerCase().includes(query) ||
        bt.symbol.toLowerCase().includes(query),
    );
  }

  return filtered;
});

const loadBacktests = async () => {
  try {
    const response = await fetch(
      `/api/backtests?page=${currentPage.value}&limit=${pageSize.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      },
    );

    if (response.ok) {
      const data = await response.json();
      backtests.value = data.backtests;
      totalPages.value = data.totalPages;
    }
  } catch (error) {
    console.error("Failed to load backtests:", error);
    toast.error("Failed to load backtest history");
  }
};

const viewBacktest = (backtest) => {
  if (expandedBacktest.value === backtest.id) {
    expandedBacktest.value = null;
  } else {
    expandedBacktest.value = backtest.id;
  }
};

const reRunBacktest = async (backtest) => {
  try {
    const response = await fetch("/api/backtests", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        strategyId: backtest.strategyId,
        symbol: backtest.symbol,
        timeframe: backtest.timeframe,
        parameters: backtest.parameters,
        startDate: backtest.startDate,
        endDate: backtest.endDate,
      }),
    });

    if (response.ok) {
      toast.success("Backtest started successfully!");
      router.push("/backtest");
    } else {
      throw new Error("Failed to start backtest");
    }
  } catch (error) {
    console.error("Failed to re-run backtest:", error);
    toast.error("Failed to re-run backtest");
  }
};

const deleteBacktest = async (backtest) => {
  if (!confirm("Are you sure you want to delete this backtest?")) {
    return;
  }

  try {
    const response = await fetch(`/api/backtests/${backtest.id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      toast.success("Backtest deleted successfully!");
      loadBacktests();
    } else {
      throw new Error("Failed to delete backtest");
    }
  } catch (error) {
    console.error("Failed to delete backtest:", error);
    toast.error("Failed to delete backtest");
  }
};

watch([currentPage, filterStatus, searchQuery], () => {
  loadBacktests();
});

onMounted(() => {
  loadBacktests();
});
</script>
