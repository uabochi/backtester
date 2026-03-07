<template>
  <div class="backtest-page">
    <div class="container">
      <div class="mode-toggle">
        <button
          @click="toggleMode"
          :class="['mode-btn', { active: isStreaming }]"
        >
          {{ isStreaming ? "Streaming Mode" : "Batch Mode" }}
        </button>
      </div>

      <div class="form-section">
        <StrategyForm @submit="handleBacktest" />
      </div>

      <div class="results-section" v-if="hasResults || loading || isStreaming">
        <!-- Streaming Controls -->
        <div v-if="isStreaming" class="streaming-controls">
          <div class="control-buttons">
            <button
              @click="startStreaming"
              :disabled="isPlaying"
              class="btn-primary"
            >
              Start Streaming
            </button>
            <button
              @click="playPause"
              :disabled="!streamingStarted"
              class="btn-secondary"
            >
              {{ isPlaying ? "Pause" : "Play" }}
            </button>
            <button
              @click="stepForward"
              :disabled="isPlaying || !streamingStarted"
              class="btn-secondary"
            >
              Step Forward
            </button>
            <button @click="resetStreaming" class="btn-secondary">Reset</button>
          </div>
          <div v-if="streamingStarted" class="progress-info">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <span>{{ currentBarIndex }} / {{ totalBars }} bars</span>
          </div>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Running backtest... This may take a few moments.</p>
        </div>

        <div
          v-else-if="hasResults || (isStreaming && bars.length > 0)"
          class="results"
        >
          <ResultsHeader :backtest-id="backtestId" @reset="resetForm" />
          <MetricsCards :metrics="currentMetrics" />

          <!-- Show candlestick chart in streaming mode, equity chart in batch mode -->
          <CandlestickChart
            v-if="isStreaming"
            :bars="bars"
            :symbol="store.form.symbol"
            :timeframe="store.form.timeframe"
          />
          <EquityCurveChart v-else :data="chartData" />

          <TradesTable :trades="tradeLog" />
        </div>
      </div>

      <div v-if="error" class="error-message">
        <div class="error-icon">⚠️</div>
        <h3>Error</h3>
        <p>{{ error }}</p>
        <button @click="clearError" class="btn-secondary">Dismiss</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useBacktestStore } from "../stores/backtestStore.js";
import StrategyForm from "../components/StrategyForm.vue";
import ResultsHeader from "../components/ResultsHeader.vue";
import MetricsCards from "../components/MetricsCards.vue";
import EquityCurveChart from "../components/EquityCurveChart.vue";
import CandlestickChart from "../components/CandlestickChart.vue";
import TradesTable from "../components/TradesTable.vue";

const store = useBacktestStore();

const hasResults = computed(() => store.hasResults);
const loading = computed(() => store.isLoading);
const error = computed(() => store.error);
const results = computed(() => store.results);
const backtestId = computed(() => store.backtestId);

// Streaming properties
const isStreaming = computed(() => store.isStreaming);
const isPlaying = computed(() => store.isPlaying);
const currentBarIndex = computed(() => store.currentBarIndex);
const totalBars = computed(() => store.totalBars);
const progress = computed(() => store.progress);
const bars = computed(() => store.bars);
const equityCurve = computed(() => store.equityCurve);
const tradeLog = computed(() => store.tradeLog);
const streamingStarted = computed(() => store.bars.length > 0);

const chartData = computed(() =>
  isStreaming ? equityCurve.value : results.value?.equity_curve || [],
);
const currentMetrics = computed(() => {
  if (isStreaming.value) {
    const totalTrades = tradeLog.value.length;
    const winningTrades = tradeLog.value.filter(
      (t) => t.type === "SELL" && t.price > 0,
    ).length;
    return {
      total_return: (
        ((store.currentEquity - store.form.initial_cash) /
          store.form.initial_cash) *
        100
      ).toFixed(2),
      final_equity: store.currentEquity.toFixed(2),
      total_trades: totalTrades,
      winning_trades: winningTrades,
      win_rate:
        totalTrades > 0 ? ((winningTrades / totalTrades) * 100).toFixed(2) : 0,
      sharpe_ratio: 0.0,
      max_drawdown: 0.0,
    };
  }
  return results.value?.metrics || {};
});

const handleBacktest = async () => {
  if (isStreaming.value) {
    store.startStreamingBacktest();
  } else {
    try {
      await store.runBacktest();
    } catch (error) {
      console.error("Backtest failed:", error);
    }
  }
};

const toggleMode = () => {
  store.streamingMode = !store.streamingMode;
};

const startStreaming = () => {
  store.startStreamingBacktest();
};

const playPause = () => {
  if (isPlaying.value) {
    store.pauseStreaming();
  } else {
    store.playStreaming();
  }
};

const stepForward = () => {
  store.stepForwardStreaming();
};

const resetStreaming = () => {
  store.resetStreaming();
};

const resetForm = () => {
  store.resetForm();
};

const clearError = () => {
  store.error = null;
};

// Load initial data
onMounted(async () => {
  await Promise.all([store.loadStrategies(), store.loadDataOptions()]);
});
</script>

<style scoped>
.backtest-page {
  min-height: 100vh;
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.form-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  margin-bottom: 2rem;
  overflow: hidden;
}

.results-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  overflow: hidden;
}

.loading {
  padding: 4rem 2rem;
  text-align: center;
  color: #666;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
  text-align: center;
  color: #c33;
}

.error-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.error-message h3 {
  margin-bottom: 0.5rem;
  color: #c33;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.btn-secondary:hover {
  background: #5a6268;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
}
</style>
