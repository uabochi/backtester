<template>
  <div class="results-header">
    <div class="header-content">
      <div class="title-section">
        <h2>Backtest Results</h2>
        <p v-if="backtestId" class="backtest-id">ID: {{ backtestId }}</p>
      </div>
      <div class="actions">
        <button @click="exportResults" class="btn-secondary">
          📊 Export CSV
        </button>
        <button @click="$emit('reset')" class="btn-primary">
          🔄 New Backtest
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  backtestId: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["reset"]);

const exportResults = () => {
  // TODO: Implement CSV export
  alert("CSV export feature coming soon!");
};
</script>

<style scoped>
.results-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section h2 {
  margin: 0 0 0.25rem 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.backtest-id {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-family: monospace;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .actions {
    width: 100%;
    justify-content: center;
  }

  .btn-primary,
  .btn-secondary {
    flex: 1;
    max-width: 150px;
  }
}
</style>
