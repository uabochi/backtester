<template>
  <div class="candlestick-chart">
    <div class="chart-header">
      <h3>{{ symbol }} {{ timeframe.toUpperCase() }} Price Chart</h3>
      <div class="chart-info">
        <span
          >Current: {{ currentPrice ? formatPrice(currentPrice) : "N/A" }}</span
        >
        <span>Time: {{ currentTime || "N/A" }}</span>
      </div>
    </div>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  BarController,
} from "chart.js";
import {
  CandlestickController,
  CandlestickElement,
} from "chartjs-chart-financial";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  BarController,
  Title,
  Tooltip,
  Legend,
  CandlestickController,
  CandlestickElement,
);

const props = defineProps({
  bars: {
    type: Array,
    default: () => [],
  },
  symbol: {
    type: String,
    default: "BTCUSDT",
  },
  timeframe: {
    type: String,
    default: "1h",
  },
});

const chartCanvas = ref(null);
let chart = null;

const currentPrice = ref(null);
const currentTime = ref(null);

const formatPrice = (price) => {
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(price);
};

const formatTime = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const createChart = () => {
  if (!chartCanvas.value) return;

  const ctx = chartCanvas.value.getContext("2d");

  chart = new ChartJS(ctx, {
    type: "candlestick",
    data: {
      datasets: [
        {
          label: props.symbol,
          data: props.bars.map((bar, index) => ({
            x: index,
            o: bar.open,
            h: bar.high,
            l: bar.low,
            c: bar.close,
          })),
          color: {
            up: "#26a69a",
            down: "#ef5350",
            unchanged: "#999",
          },
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 0, // Disable animation for real-time updates
      },
      scales: {
        x: {
          type: "category",
          labels: props.bars.map((bar, index) => formatTime(bar.timestamp)),
          ticks: {
            maxTicksLimit: 10,
          },
        },
        y: {
          position: "right",
          ticks: {
            callback: function (value) {
              return formatPrice(value);
            },
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const data = context.raw;
              return [
                `Open: ${formatPrice(data.o)}`,
                `High: ${formatPrice(data.h)}`,
                `Low: ${formatPrice(data.l)}`,
                `Close: ${formatPrice(data.c)}`,
              ];
            },
          },
        },
      },
    },
  });
};

const updateChart = () => {
  if (!chart) return;

  // Update data
  chart.data.datasets[0].data = props.bars.map((bar, index) => ({
    x: index,
    o: bar.open,
    h: bar.high,
    l: bar.low,
    c: bar.close,
  }));

  chart.data.labels = props.bars.map((bar, index) => formatTime(bar.timestamp));

  // Update current price and time
  if (props.bars.length > 0) {
    const lastBar = props.bars[props.bars.length - 1];
    currentPrice.value = lastBar.close;
    currentTime.value = formatTime(lastBar.timestamp);
  }

  chart.update("none"); // Update without animation
};

onMounted(() => {
  nextTick(() => {
    createChart();
  });
});

watch(
  () => props.bars,
  () => {
    if (chart) {
      updateChart();
    } else {
      createChart();
    }
  },
  { deep: true },
);
</script>

<style scoped>
.candlestick-chart {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.chart-header h3 {
  margin: 0;
  color: #333;
}

.chart-info {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.chart-info span {
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.chart-container {
  flex: 1;
  position: relative;
}
</style>
