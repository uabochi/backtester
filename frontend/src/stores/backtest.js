import { defineStore } from "pinia";
import { ref, reactive } from "vue";
import api from "@/services/api";
import { io } from "socket.io-client";

export const useBacktestStore = defineStore("backtest", () => {
  // State
  const isRunning = ref(false);
  const progress = ref(0);
  const currentStep = ref("");
  const results = ref(null);
  const error = ref(null);
  const socket = ref(null);

  // Configuration
  const config = reactive({
    strategy: "",
    symbol: "EURUSD",
    timeframe: "1h",
    startDate: "",
    endDate: "",
    initialCapital: 10000,
    parameters: {},
  });

  // Socket connection
  const connectSocket = () => {
    if (socket.value) return;

    const API_BASE_URL =
      import.meta.env.VITE_API_URL || "http://localhost:5002";
    socket.value = io(API_BASE_URL);

    socket.value.on("backtest_progress", (data) => {
      progress.value = data.progress;
      currentStep.value = data.step;
    });

    socket.value.on("backtest_complete", (data) => {
      results.value = data.results;
      isRunning.value = false;
      progress.value = 100;
      currentStep.value = "Complete";
    });

    socket.value.on("backtest_error", (data) => {
      error.value = data.error;
      isRunning.value = false;
    });
  };

  const disconnectSocket = () => {
    if (socket.value) {
      socket.value.off("backtest_progress");
      socket.value.off("backtest_complete");
      socket.value.off("backtest_error");
      socket.value.disconnect();
      socket.value = null;
    }
  };

  // Actions
  const startBacktest = async () => {
    try {
      isRunning.value = true;
      progress.value = 0;
      currentStep.value = "Initializing...";
      error.value = null;
      results.value = null;

      connectSocket();

      const response = await api.post("/api/backtest", config);

      if (response.status !== 200) {
        throw new Error("Backtest failed to start");
      }

      return { success: true, backtestId: response.data.backtestId };
    } catch (err) {
      error.value = err.message;
      isRunning.value = false;
      return { success: false, error: err.message };
    }
  };

  const stopBacktest = async () => {
    try {
      await api.post("/api/backtest/stop");
      isRunning.value = false;
      disconnectSocket();
    } catch (err) {
      console.error("Failed to stop backtest:", err);
    }
  };

  const updateConfig = (newConfig) => {
    Object.assign(config, newConfig);
  };

  const reset = () => {
    isRunning.value = false;
    progress.value = 0;
    currentStep.value = "";
    results.value = null;
    error.value = null;
    disconnectSocket();
  };

  return {
    // State
    isRunning,
    progress,
    currentStep,
    results,
    error,
    config,

    // Actions
    startBacktest,
    stopBacktest,
    updateConfig,
    reset,
    connectSocket,
    disconnectSocket,
  };
});
