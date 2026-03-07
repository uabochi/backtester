<template>
  <div class="metrics-cards">
    <div class="metric-card">
      <div class="metric-icon">💰</div>
      <div class="metric-content">
        <h3>Total Return</h3>
        <p class="metric-value" :class="getReturnClass(metrics.total_return)">
          {{ formatPercentage(metrics.total_return) }}
        </p>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">📈</div>
      <div class="metric-content">
        <h3>Final Equity</h3>
        <p class="metric-value">${{ formatCurrency(metrics.final_equity) }}</p>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">📊</div>
      <div class="metric-content">
        <h3>Sharpe Ratio</h3>
        <p class="metric-value">
          {{ formatNumber(metrics.sharpe_ratio) }}
        </p>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">🎯</div>
      <div class="metric-content">
        <h3>Win Rate</h3>
        <p class="metric-value">
          {{ formatPercentage(metrics.win_rate) }}
        </p>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">🔄</div>
      <div class="metric-content">
        <h3>Total Trades</h3>
        <p class="metric-value">
          {{ metrics.total_trades }}
        </p>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">📉</div>
      <div class="metric-content">
        <h3>Max Drawdown</h3>
        <p class="metric-value negative">
          {{ formatPercentage(metrics.max_drawdown) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  metrics: {
    type: Object,
    required: true,
  },
});

const formatPercentage = (value) => {
  if (value === null || value === undefined) return "N/A";
  // Handle both numbers and strings
  const numValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numValue)) return "N/A";
  return `${numValue >= 0 ? "+" : ""}${numValue.toFixed(2)}%`;
};

const formatCurrency = (value) => {
  if (value === null || value === undefined) return "N/A";
  // Handle both numbers and strings
  const numValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numValue)) return "N/A";
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numValue);
};

const formatNumber = (value) => {
  if (value === null || value === undefined) return "N/A";
  // Handle both numbers and strings
  const numValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numValue)) return "N/A";
  return numValue.toFixed(2);
};

const getReturnClass = (returnValue) => {
  if (returnValue === null || returnValue === undefined) return "";
  return returnValue >= 0 ? "positive" : "negative";
};
</script>

<style scoped>
.metrics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
  background: #f8f9fa;
}

.metric-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.metric-content {
  flex: 1;
}

.metric-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.metric-value.positive {
  color: #28a745;
}

.metric-value.negative {
  color: #dc3545;
}

@media (max-width: 768px) {
  .metrics-cards {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .metric-card {
    padding: 1rem;
  }

  .metric-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }

  .metric-value {
    font-size: 1.5rem;
  }
}
</style>
