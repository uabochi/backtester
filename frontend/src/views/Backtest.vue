<template>
  <div class="backtest-view">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Backtest
        </h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Test your trading strategies with historical data
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Configuration Panel -->
        <div class="lg:col-span-1">
          <div class="card sticky top-8">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">
              Configuration
            </h3>

            <form @submit.prevent="startBacktest" class="space-y-6">
              <!-- Strategy Selection -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Strategy
                </label>
                <select v-model="config.strategy" class="input" required>
                  <option value="">Select a strategy</option>
                  <option
                    v-for="strategy in strategies"
                    :key="strategy.id"
                    :value="strategy.id"
                  >
                    {{ strategy.name }}
                  </option>
                </select>
              </div>

              <!-- Symbol Selection -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Symbol
                </label>
                <select v-model="config.symbol" class="input" required>
                  <option value="EURUSD">EUR/USD</option>
                  <option value="GBPUSD">GBP/USD</option>
                  <option value="USDJPY">USD/JPY</option>
                  <option value="AUDUSD">AUD/USD</option>
                  <option value="USDCAD">USD/CAD</option>
                  <option value="USDCHF">USD/CHF</option>
                  <option value="NZDUSD">NZD/USD</option>
                </select>
              </div>

              <!-- Timeframe -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Timeframe
                </label>
                <select v-model="config.timeframe" class="input" required>
                  <option value="1m">1 Minute</option>
                  <option value="5m">5 Minutes</option>
                  <option value="15m">15 Minutes</option>
                  <option value="1h">1 Hour</option>
                  <option value="4h">4 Hours</option>
                  <option value="1d">1 Day</option>
                </select>
              </div>

              <!-- Date Range -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Start Date
                  </label>
                  <input
                    v-model="config.startDate"
                    type="date"
                    class="input"
                    required
                  />
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    End Date
                  </label>
                  <input
                    v-model="config.endDate"
                    type="date"
                    class="input"
                    required
                  />
                </div>
              </div>

              <!-- Initial Capital -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Initial Capital ($)
                </label>
                <input
                  v-model.number="config.initialCapital"
                  type="number"
                  min="100"
                  step="100"
                  class="input"
                  required
                />
              </div>

              <!-- Strategy Parameters -->
              <div v-if="selectedStrategy">
                <h4
                  class="text-md font-medium text-gray-900 dark:text-white mb-3"
                >
                  {{ selectedStrategy.name }} Parameters
                </h4>

                <div class="space-y-4">
                  <div
                    v-for="param in selectedStrategy.parameters"
                    :key="param.name"
                  >
                    <label
                      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                    >
                      {{ param.label }}
                    </label>

                    <input
                      v-if="param.type === 'number'"
                      v-model.number="config.parameters[param.name]"
                      :type="param.type"
                      :min="param.min"
                      :max="param.max"
                      :step="param.step"
                      class="input"
                      :required="param.required"
                    />

                    <select
                      v-else-if="param.type === 'select'"
                      v-model="config.parameters[param.name]"
                      class="input"
                      :required="param.required"
                    >
                      <option
                        v-for="option in param.options"
                        :key="option.value"
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="space-y-3">
                <button
                  type="submit"
                  :disabled="isRunning || !config.strategy"
                  class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg
                    v-if="isRunning"
                    class="animate-spin -ml-1 mr-3 h-4 w-4 text-white inline"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  {{ isRunning ? "Running Backtest..." : "Start Backtest" }}
                </button>

                <button
                  v-if="isRunning"
                  @click="stopBacktest"
                  type="button"
                  class="w-full btn bg-red-600 hover:bg-red-700 text-white"
                >
                  Stop Backtest
                </button>
              </div>
            </form>

            <!-- Progress -->
            <div v-if="isRunning" class="mt-6">
              <div
                class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2"
              >
                <span>{{ currentStep }}</span>
                <span>{{ progress }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                <div
                  class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart and Results -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Chart -->
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                {{ config.symbol }} - {{ config.timeframe }}
              </h3>
              <div class="flex items-center space-x-2">
                <button
                  @click="toggleChartMode"
                  class="px-3 py-1 text-sm rounded-md"
                  :class="
                    chartMode === 'price'
                      ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/20 dark:text-primary-300'
                      : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                  "
                >
                  Price
                </button>
                <button
                  @click="toggleChartMode"
                  class="px-3 py-1 text-sm rounded-md"
                  :class="
                    chartMode === 'equity'
                      ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/20 dark:text-primary-300'
                      : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                  "
                >
                  Equity
                </button>
              </div>
            </div>

            <div v-if="chartMode === 'price'" class="h-96">
              <TradingChart
                ref="tradingChart"
                :data="chartData"
                :symbol="config.symbol"
                :height="400"
                @timeframeChange="handleTimeframeChange"
              />
            </div>

            <div v-else class="h-96">
              <canvas ref="equityChart" class="w-full h-full"></canvas>
            </div>
          </div>

          <!-- Results -->
          <div v-if="results" class="card">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">
              Results
            </h3>

            <!-- Metrics Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">
                  ${{ results.totalReturn.toFixed(2) }}
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Total Return
                </p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ results.winRate.toFixed(1) }}%
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Win Rate</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ results.totalTrades }}
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Total Trades
                </p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ results.sharpeRatio.toFixed(2) }}
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Sharpe Ratio
                </p>
              </div>
            </div>

            <!-- Trade Table -->
            <div>
              <h4
                class="text-md font-medium text-gray-900 dark:text-white mb-3"
              >
                Recent Trades
              </h4>
              <div class="overflow-x-auto">
                <table
                  class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
                >
                  <thead class="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        Date
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        Type
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        Price
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        P&L
                      </th>
                    </tr>
                  </thead>
                  <tbody
                    class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700"
                  >
                    <tr
                      v-for="trade in results.trades.slice(-10)"
                      :key="trade.id"
                    >
                      <td
                        class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                      >
                        {{ new Date(trade.timestamp).toLocaleDateString() }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span
                          class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                          :class="
                            trade.type === 'buy'
                              ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                              : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
                          "
                        >
                          {{ trade.type.toUpperCase() }}
                        </span>
                      </td>
                      <td
                        class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                      >
                        {{ trade.price.toFixed(5) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm">
                        <span
                          :class="
                            trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                          "
                        >
                          {{ trade.pnl >= 0 ? "+" : ""
                          }}{{ trade.pnl.toFixed(2) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import { useBacktestStore } from "@/stores/backtest";
import { useToast } from "vue-toastification";
import TradingChart from "@/components/charts/TradingChart.vue";

const backtestStore = useBacktestStore();
const toast = useToast();

// Reactive data
const strategies = ref([]);
const chartData = ref([]);
const chartMode = ref("price");
const equityChart = ref(null);

// Computed properties
const isRunning = computed(() => backtestStore.isRunning);
const progress = computed(() => backtestStore.progress);
const currentStep = computed(() => backtestStore.currentStep);
const results = computed(() => backtestStore.results);
const config = computed(() => backtestStore.config);

const selectedStrategy = computed(() => {
  return strategies.value.find((s) => s.id === config.value.strategy);
});

// Methods
const startBacktest = async () => {
  const result = await backtestStore.startBacktest();

  if (result.success) {
    toast.success("Backtest started successfully!");
    // Load sample chart data for demo
    loadSampleChartData();
  } else {
    toast.error(result.error || "Failed to start backtest");
  }
};

const stopBacktest = async () => {
  await backtestStore.stopBacktest();
  toast.info("Backtest stopped");
};

const toggleChartMode = () => {
  chartMode.value = chartMode.value === "price" ? "equity" : "price";
};

const handleTimeframeChange = (timeframe) => {
  config.value.timeframe = timeframe;
  loadSampleChartData();
};

const loadSampleChartData = () => {
  // Generate sample OHLCV data for demo
  const data = [];
  const basePrice = 1.1;
  let currentPrice = basePrice;

  for (let i = 0; i < 100; i++) {
    const time = Date.now() - (100 - i) * 3600000; // 1 hour intervals
    const open = currentPrice;
    const close = open + (Math.random() - 0.5) * 0.01;
    const high = Math.max(open, close) + Math.random() * 0.005;
    const low = Math.min(open, close) - Math.random() * 0.005;
    const volume = Math.floor(Math.random() * 1000) + 100;

    data.push({
      time: Math.floor(time / 1000),
      open,
      high,
      low,
      close,
      volume,
    });

    currentPrice = close;
  }

  chartData.value = data;
};

const loadStrategies = async () => {
  try {
    const response = await fetch("/api/strategies", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      strategies.value = await response.json();
    }
  } catch (error) {
    console.error("Failed to load strategies:", error);
  }
};

onMounted(() => {
  loadStrategies();
  loadSampleChartData();

  // Set default dates
  const today = new Date();
  const oneYearAgo = new Date(today.getTime() - 365 * 24 * 60 * 60 * 1000);

  config.value.startDate = oneYearAgo.toISOString().split("T")[0];
  config.value.endDate = today.toISOString().split("T")[0];
});
</script>
