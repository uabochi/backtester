<template>
  <div class="equity-chart">
    <div class="chart-header">
      <h3>Equity Curve</h3>
      <div class="chart-controls">
        <button
          @click="toggleLogScale"
          :class="{ active: logScale }"
          class="scale-btn"
        >
          Log Scale
        </button>
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
  LogarithmicScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

const chartCanvas = ref(null);
const chart = ref(null);
const logScale = ref(false);

const toggleLogScale = () => {
  logScale.value = !logScale.value;
  updateChart();
};

const updateChart = () => {
  if (!chart.value || !props.data.length) return;

  const labels = props.data.map((point) => {
    const timestamp = point.timestamp;
    // Format timestamp for display
    if (typeof timestamp === "string") {
      return timestamp.split(" ")[0] || timestamp; // Use date part only
    }
    return timestamp;
  });

  const equityData = props.data.map((point) => point.equity);

  chart.value.data = {
    labels,
    datasets: [
      {
        label: "Portfolio Equity",
        data: equityData,
        borderColor: "#667eea",
        backgroundColor: "rgba(102, 126, 234, 0.1)",
        fill: true,
        tension: 0.1,
        pointRadius: 0,
        pointHoverRadius: 4,
        pointBackgroundColor: "#667eea",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
      },
    ],
  };

  chart.value.options.scales.y = {
    type: logScale.value ? "logarithmic" : "linear",
    beginAtZero: !logScale.value,
    ticks: {
      callback: function (value) {
        return "$" + value.toLocaleString();
      },
    },
    grid: {
      color: "rgba(0, 0, 0, 0.05)",
    },
  };

  chart.value.update();
};

const createChart = () => {
  if (!chartCanvas.value) return;

  const ctx = chartCanvas.value.getContext("2d");

  chart.value = new ChartJS(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: "index",
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `Equity: $${context.parsed.y.toLocaleString()}`;
            },
          },
        },
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: "Time",
          },
          grid: {
            display: false,
          },
        },
        y: {
          display: true,
          title: {
            display: true,
            text: "Portfolio Value ($)",
          },
        },
      },
    },
  });

  updateChart();
};

onMounted(() => {
  nextTick(() => {
    createChart();
  });
});

watch(
  () => props.data,
  () => {
    nextTick(() => {
      if (!chart.value) {
        createChart();
      } else {
        updateChart();
      }
    });
  },
  { deep: true },
);
</script>

<style scoped>
.equity-chart {
  padding: 2rem;
  background: white;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
}

.scale-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e1e5e9;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.scale-btn:hover {
  background: #f8f9fa;
}

.scale-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.chart-container {
  height: 400px;
  position: relative;
}

@media (max-width: 768px) {
  .equity-chart {
    padding: 1rem;
  }

  .chart-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
