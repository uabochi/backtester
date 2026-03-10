<template>
  <div class="trading-chart-container">
    <div class="chart-toolbar">
      <div class="toolbar-left">
        <button
          @click="toggleDrawingMode"
          :class="['toolbar-btn', { active: isDrawingMode }]"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
            />
          </svg>
          Draw
        </button>
        <button @click="clearDrawings" class="toolbar-btn">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path
              fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            />
          </svg>
          Clear
        </button>
      </div>
      <div class="toolbar-right">
        <select
          v-model="selectedTimeframe"
          @change="changeTimeframe"
          class="timeframe-select"
        >
          <option value="1m">1m</option>
          <option value="5m">5m</option>
          <option value="15m">15m</option>
          <option value="1h">1h</option>
          <option value="4h">4h</option>
          <option value="1d">1d</option>
        </select>
      </div>
    </div>

    <div ref="chartContainer" class="chart-container"></div>

    <!-- Drawing Tools Panel -->
    <div v-if="isDrawingMode" class="drawing-tools-panel">
      <div class="drawing-tools">
        <button
          v-for="tool in drawingTools"
          :key="tool.id"
          @click="selectDrawingTool(tool.id)"
          :class="['drawing-tool-btn', { active: selectedTool === tool.id }]"
        >
          <component :is="tool.icon" class="w-4 h-4" />
          {{ tool.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { createChart, ColorType } from "lightweight-charts";

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
  height: {
    type: Number,
    default: 400,
  },
  symbol: {
    type: String,
    default: "EURUSD",
  },
});

// Emits
const emit = defineEmits(["timeframeChange", "drawingAdded", "drawingRemoved"]);

// Refs
const chartContainer = ref(null);
const chart = ref(null);
const candlestickSeries = ref(null);
const selectedTimeframe = ref("1h");
const isDrawingMode = ref(false);
const selectedTool = ref(null);

// Drawing tools configuration
const drawingTools = [
  { id: "trendline", name: "Trend Line", icon: "TrendlineIcon" },
  { id: "horizontal", name: "Horizontal Line", icon: "HorizontalIcon" },
  { id: "rectangle", name: "Rectangle", icon: "RectangleIcon" },
  { id: "fibonacci", name: "Fibonacci", icon: "FibonacciIcon" },
];

// Initialize chart
const initChart = () => {
  if (!chartContainer.value) return;

  chart.value = createChart(chartContainer.value, {
    layout: {
      background: { type: ColorType.Solid, color: "transparent" },
      textColor: "#d1d4dc",
    },
    grid: {
      vertLines: { color: "#334155" },
      horzLines: { color: "#334155" },
    },
    crosshair: {
      mode: 1, // CrosshairMode.Normal
    },
    rightPriceScale: {
      borderColor: "#485563",
    },
    timeScale: {
      borderColor: "#485563",
      timeVisible: true,
      secondsVisible: false,
    },
    width: chartContainer.value.clientWidth,
    height: props.height,
  });

  // Create candlestick series
  candlestickSeries.value = chart.value.addCandlestickSeries({
    upColor: "#22c55e",
    downColor: "#ef4444",
    borderVisible: false,
    wickUpColor: "#22c55e",
    wickDownColor: "#ef4444",
  });

  // Load initial data
  if (props.data.length > 0) {
    loadData(props.data);
  }

  // Handle resize
  const resizeObserver = new ResizeObserver(() => {
    if (chart.value && chartContainer.value) {
      chart.value.applyOptions({
        width: chartContainer.value.clientWidth,
      });
    }
  });
  resizeObserver.observe(chartContainer.value);
};

// Load data into chart
const loadData = (data) => {
  if (!candlestickSeries.value) return;

  const formattedData = data.map((item) => ({
    time: item.time,
    open: item.open,
    high: item.high,
    low: item.low,
    close: item.close,
  }));

  candlestickSeries.value.setData(formattedData);

  // Fit content
  chart.value.timeScale().fitContent();
};

// Add trade markers (entry/exit points)
const addTradeMarker = (trade) => {
  if (!candlestickSeries.value) return;

  const marker = {
    time: trade.time,
    position: trade.type === "buy" ? "belowBar" : "aboveBar",
    color: trade.type === "buy" ? "#22c55e" : "#ef4444",
    shape: trade.type === "buy" ? "arrowUp" : "arrowDown",
    text: trade.type === "buy" ? "B" : "S",
    size: 2,
  };

  candlestickSeries.value.markers().push(marker);
};

// Add multiple trade markers
const addTradeMarkers = (trades) => {
  if (!candlestickSeries.value) return;

  const markers = trades.map((trade) => ({
    time: trade.time,
    position: trade.type === "buy" ? "belowBar" : "aboveBar",
    color: trade.type === "buy" ? "#22c55e" : "#ef4444",
    shape: trade.type === "buy" ? "arrowUp" : "arrowDown",
    text: trade.type === "buy" ? "B" : "S",
    size: 2,
  }));

  candlestickSeries.value.setMarkers(markers);
};

// Drawing tools functions
const toggleDrawingMode = () => {
  isDrawingMode.value = !isDrawingMode.value;
  if (!isDrawingMode.value) {
    selectedTool.value = null;
  }
};

const selectDrawingTool = (toolId) => {
  selectedTool.value = toolId;
  // TODO: Implement drawing functionality
};

const clearDrawings = () => {
  // TODO: Clear all drawings
  emit("drawingRemoved");
};

// Timeframe change
const changeTimeframe = () => {
  emit("timeframeChange", selectedTimeframe.value);
};

// Watch for data changes
watch(
  () => props.data,
  (newData) => {
    if (newData && newData.length > 0) {
      loadData(newData);
    }
  },
  { deep: true },
);

// Lifecycle
onMounted(() => {
  initChart();
});

onUnmounted(() => {
  if (chart.value) {
    chart.value.remove();
  }
});

// Expose methods for parent component
defineExpose({
  addTradeMarker,
  addTradeMarkers,
  loadData,
  chart: chart,
});
</script>

<style scoped>
.trading-chart-container {
  @apply bg-gray-900 rounded-lg overflow-hidden border border-gray-700;
}

.chart-toolbar {
  @apply flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700;
}

.toolbar-left {
  @apply flex items-center space-x-2;
}

.toolbar-right {
  @apply flex items-center;
}

.toolbar-btn {
  @apply flex items-center space-x-1 px-3 py-1 text-sm text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors duration-200;
}

.toolbar-btn.active {
  @apply bg-primary-600 text-white;
}

.timeframe-select {
  @apply bg-gray-700 border border-gray-600 rounded px-2 py-1 text-sm text-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-primary-500;
}

.chart-container {
  @apply w-full;
}

.drawing-tools-panel {
  @apply bg-gray-800 border-t border-gray-700 p-3;
}

.drawing-tools {
  @apply flex flex-wrap gap-2;
}

.drawing-tool-btn {
  @apply flex items-center space-x-1 px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors duration-200;
}

.drawing-tool-btn.active {
  @apply bg-primary-600 text-white;
}
</style>
