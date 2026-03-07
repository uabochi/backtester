<template>
  <form @submit.prevent="handleSubmit" class="strategy-form">
    <div class="form-header">
      <h2>Configure Backtest</h2>
      <p>Set up your trading strategy parameters</p>
    </div>

    <div class="form-grid">
      <!-- Symbol Selection -->
      <div class="form-group">
        <label for="symbol">Symbol</label>
        <select
          id="symbol"
          v-model="formData.symbol"
          @change="updateSymbolTimeframe"
          required
        >
          <option v-for="symbol in symbols" :key="symbol" :value="symbol">
            {{ symbol }}
          </option>
        </select>
      </div>

      <!-- Timeframe Selection -->
      <div class="form-group">
        <label for="timeframe">Timeframe</label>
        <select
          id="timeframe"
          v-model="formData.timeframe"
          @change="updateSymbolTimeframe"
          required
        >
          <option
            v-for="timeframe in timeframes"
            :key="timeframe"
            :value="timeframe"
          >
            {{ timeframe }}
          </option>
        </select>
      </div>

      <!-- Strategy Selection -->
      <div class="form-group">
        <label for="strategy">Strategy</label>
        <select
          id="strategy"
          v-model="formData.strategy"
          @change="updateStrategy"
          required
        >
          <option
            v-for="strategy in strategies"
            :key="strategy.name"
            :value="strategy.name"
          >
            {{ strategy.label }}
          </option>
        </select>
      </div>

      <!-- Initial Cash -->
      <div class="form-group">
        <label for="initial_cash">Initial Cash ($)</label>
        <input
          id="initial_cash"
          type="number"
          v-model.number="formData.initial_cash"
          min="100"
          max="1000000"
          step="100"
          required
        />
      </div>
    </div>

    <!-- Strategy Parameters -->
    <div v-if="currentStrategy.params" class="strategy-params">
      <h3>{{ currentStrategy.label }} Parameters</h3>
      <div class="params-grid">
        <div
          v-for="param in currentStrategy.params"
          :key="param.name"
          class="param-group"
        >
          <label :for="param.name">
            {{
              param.name
                .replace("_", " ")
                .replace(/\b\w/g, (l) => l.toUpperCase())
            }}
            <span class="param-description">{{ param.description }}</span>
          </label>
          <input
            :id="param.name"
            :type="param.type"
            :min="param.min"
            :max="param.max"
            :step="param.type === 'integer' ? 1 : 0.1"
            v-model.number="formData.strategy_params[param.name]"
            required
          />
        </div>
      </div>
    </div>

    <!-- Form Actions -->
    <div class="form-actions">
      <button type="button" @click="resetForm" class="btn-secondary">
        Reset
      </button>
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? "Running..." : "Run Backtest" }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useBacktestStore } from "../stores/backtestStore.js";

const store = useBacktestStore();

// Local form data (copy from store)
const formData = ref({ ...store.form });

const strategies = computed(() => store.strategies);
const dataFiles = computed(() => store.dataFiles);
const symbols = computed(() => store.symbols);
const timeframes = computed(() => store.timeframes);
const currentStrategy = computed(() => store.currentStrategy);
const loading = computed(() => store.isLoading);

// Watch for store changes and update local form
watch(
  () => store.form,
  (newForm) => {
    formData.value = { ...newForm };
  },
  { deep: true },
);

const updateSymbolTimeframe = () => {
  store.updateSymbolTimeframe();
  // Update local form with the new csv_file
  formData.value.csv_file = store.form.csv_file;
};

const updateStrategy = () => {
  store.updateStrategy(formData.value.strategy);
  // Reset params to defaults
  const strategy = strategies.value.find(
    (s) => s.name === formData.value.strategy,
  );
  if (strategy && strategy.params) {
    const defaults = {};
    strategy.params.forEach((param) => {
      defaults[param.name] = param.default;
    });
    formData.value.strategy_params = defaults;
  }
};

const handleSubmit = () => {
  // Update store with local form data
  store.form = { ...formData.value };
  // Emit submit event
  emit("submit");
};

const resetForm = () => {
  store.resetForm();
  formData.value = { ...store.form };
};

// Initialize symbol/timeframe on mount
updateSymbolTimeframe();

// Define emits
const emit = defineEmits(["submit"]);
</script>

<style scoped>
.strategy-form {
  padding: 2rem;
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h2 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}

.form-header p {
  color: #666;
  font-size: 1rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

input,
select {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

.readonly-input {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.strategy-params {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.strategy-params h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.param-group {
  display: flex;
  flex-direction: column;
}

.param-description {
  display: block;
  font-size: 0.8rem;
  color: #666;
  font-weight: normal;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e1e5e9;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

@media (max-width: 768px) {
  .strategy-form {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .params-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
