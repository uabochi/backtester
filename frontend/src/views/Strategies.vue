<template>
  <div class="strategies-view">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Strategies
          </h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            Create and manage your trading strategies
          </p>
        </div>

        <button
          @click="showCreateModal = true"
          class="btn-primary flex items-center"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clip-rule="evenodd"
            />
          </svg>
          New Strategy
        </button>
      </div>

      <!-- Strategies Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Strategy Card -->
        <div
          v-for="strategy in strategies"
          :key="strategy.id"
          class="card hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          @click="editStrategy(strategy)"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div
                class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center mr-3"
              >
                <svg
                  class="w-5 h-5 text-primary-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ strategy.name }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ strategy.description }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span
                class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                :class="
                  strategy.status === 'active'
                    ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
                "
              >
                {{ strategy.status }}
              </span>
            </div>
          </div>

          <!-- Strategy Stats -->
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div class="text-center">
              <p class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ strategy.backtests }}
              </p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Backtests</p>
            </div>
            <div class="text-center">
              <p class="text-lg font-semibold text-green-600">
                {{ strategy.winRate }}%
              </p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Win Rate</p>
            </div>
            <div class="text-center">
              <p
                class="text-lg font-semibold"
                :class="
                  strategy.totalPnL >= 0 ? 'text-green-600' : 'text-red-600'
                "
              >
                {{ strategy.totalPnL >= 0 ? "+" : ""
                }}{{ strategy.totalPnL.toFixed(0) }}
              </p>
              <p class="text-xs text-gray-600 dark:text-gray-400">P&L</p>
            </div>
          </div>

          <!-- Last Updated -->
          <div class="text-xs text-gray-500 dark:text-gray-400">
            Last updated:
            {{ new Date(strategy.updatedAt).toLocaleDateString() }}
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="strategies.length === 0"
          class="col-span-full card text-center py-12"
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
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No strategies
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Get started by creating your first trading strategy.
          </p>
          <div class="mt-6">
            <button @click="showCreateModal = true" class="btn-primary">
              Create Strategy
            </button>
          </div>
        </div>
      </div>

      <!-- Create/Edit Strategy Modal -->
      <div
        v-if="showCreateModal || showEditModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        @click="closeModals"
      >
        <div
          class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white dark:bg-gray-800"
          @click.stop
        >
          <div class="mt-3">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              {{ showEditModal ? "Edit Strategy" : "Create New Strategy" }}
            </h3>

            <form @submit.prevent="saveStrategy" class="space-y-4">
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Strategy Name
                </label>
                <input
                  v-model="strategyForm.name"
                  type="text"
                  class="input"
                  required
                />
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Description
                </label>
                <textarea
                  v-model="strategyForm.description"
                  rows="3"
                  class="input"
                  placeholder="Describe your trading strategy..."
                ></textarea>
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Strategy Type
                </label>
                <select v-model="strategyForm.type" class="input" required>
                  <option value="trend-following">Trend Following</option>
                  <option value="mean-reversion">Mean Reversion</option>
                  <option value="breakout">Breakout</option>
                  <option value="scalping">Scalping</option>
                  <option value="swing">Swing Trading</option>
                </select>
              </div>

              <!-- Strategy Parameters -->
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Parameters
                </label>

                <div class="space-y-3">
                  <div
                    v-for="(param, index) in strategyForm.parameters"
                    :key="index"
                    class="flex items-center space-x-3"
                  >
                    <input
                      v-model="param.name"
                      placeholder="Parameter name"
                      class="flex-1 input text-sm"
                    />
                    <select v-model="param.type" class="input text-sm w-24">
                      <option value="number">Number</option>
                      <option value="boolean">Boolean</option>
                      <option value="select">Select</option>
                    </select>
                    <input
                      v-if="param.type === 'number'"
                      v-model.number="param.defaultValue"
                      type="number"
                      placeholder="Default"
                      class="input text-sm w-20"
                    />
                    <input
                      v-else
                      v-model="param.defaultValue"
                      placeholder="Default"
                      class="input text-sm w-20"
                    />
                    <button
                      @click="removeParameter(index)"
                      type="button"
                      class="text-red-600 hover:text-red-800 p-1"
                    >
                      <svg
                        class="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                  </div>
                </div>

                <button
                  @click="addParameter"
                  type="button"
                  class="mt-2 text-sm text-primary-600 hover:text-primary-500"
                >
                  + Add Parameter
                </button>
              </div>

              <div class="flex justify-end space-x-3 pt-4">
                <button
                  @click="closeModals"
                  type="button"
                  class="btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="isSaving"
                  class="btn-primary disabled:opacity-50"
                >
                  {{
                    isSaving ? "Saving..." : showEditModal ? "Update" : "Create"
                  }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useToast } from "vue-toastification";
import api from "@/services/api";

const toast = useToast();

const strategies = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const isSaving = ref(false);
const editingStrategy = ref(null);

const strategyForm = reactive({
  name: "",
  description: "",
  type: "trend-following",
  parameters: [
    { name: "fastPeriod", type: "number", defaultValue: 9 },
    { name: "slowPeriod", type: "number", defaultValue: 21 },
  ],
});

const loadStrategies = async () => {
  try {
    const response = await api.get("/api/strategies");
    strategies.value = response.data;
  } catch (error) {
    console.error("Failed to load strategies:", error);
    toast.error("Failed to load strategies");
  }
};

const saveStrategy = async () => {
  isSaving.value = true;
  try {
    const url = showEditModal.value
      ? `/api/strategies/${editingStrategy.value.id}`
      : "/api/strategies";

    // Use api.put or api.post based on the mode
    const response = showEditModal.value
      ? await api.put(url, strategyForm)
      : await api.post(url, strategyForm);

    toast.success(
      `Strategy ${showEditModal.value ? "updated" : "created"} successfully!`,
    );
    closeModals();
    loadStrategies();
  } catch (error) {
    console.error("Failed to save strategy:", error);
    toast.error("Failed to save strategy");
  } finally {
    isSaving.value = false;
  }
};

const editStrategy = (strategy) => {
  editingStrategy.value = strategy;
  Object.assign(strategyForm, {
    name: strategy.name,
    description: strategy.description,
    type: strategy.type,
    parameters: [...strategy.parameters],
  });
  showEditModal.value = true;
};

const addParameter = () => {
  strategyForm.parameters.push({
    name: "",
    type: "number",
    defaultValue: "",
  });
};

const removeParameter = (index) => {
  strategyForm.parameters.splice(index, 1);
};

const closeModals = () => {
  showCreateModal.value = false;
  showEditModal.value = false;
  editingStrategy.value = null;

  // Reset form
  Object.assign(strategyForm, {
    name: "",
    description: "",
    type: "trend-following",
    parameters: [
      { name: "fastPeriod", type: "number", defaultValue: 9 },
      { name: "slowPeriod", type: "number", defaultValue: 21 },
    ],
  });
};

onMounted(() => {
  loadStrategies();
});
</script>
