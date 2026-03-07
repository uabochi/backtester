import { defineStore } from "pinia";
import { backtestAPI } from "../services/api.js";

export const useBacktestStore = defineStore("backtest", {
  state: () => ({
    // Form data
    form: {
      symbol: "BTCUSDT",
      timeframe: "1h",
      strategy: "sma",
      initial_cash: 10000,
      csv_file: "BTCUSDT_1h.csv",
      strategy_params: {
        short_window: 5,
        long_window: 20,
      },
    },

    // Available options
    strategies: [],
    dataFiles: [],
    symbols: [],
    timeframes: [],
    dataOptions: {},

    // Results
    results: null,
    backtestId: null,

    // UI state
    loading: false,
    error: null,

    // Cache for results
    resultsCache: new Map(),

    // Streaming state
    streamingMode: false,
    isPlaying: false,
    currentBarIndex: 0,
    totalBars: 0,
    bars: [],
    equityCurve: [],
    tradeLog: [],
    currentEquity: 0,
    currentCash: 0,
    positions: {},
  }),

  getters: {
    isLoading: (state) => state.loading,
    hasResults: (state) => state.results !== null,
    currentStrategy: (state) => {
      return state.strategies.find((s) => s.name === state.form.strategy) || {};
    },
    selectedDataFile: (state) => {
      return state.dataFiles.find((f) => f.name === state.form.csv_file) || {};
    },
    isStreaming: (state) => state.streamingMode,
    progress: (state) =>
      state.totalBars > 0 ? (state.currentBarIndex / state.totalBars) * 100 : 0,
  },

  actions: {
    async loadStrategies() {
      try {
        const response = await backtestAPI.getStrategies();
        this.strategies = response.strategies;
        this.error = null;
      } catch (error) {
        this.error = error.message;
        console.error("Failed to load strategies:", error);
      }
    },

    async loadDataFiles() {
      try {
        const response = await backtestAPI.getDataFiles();
        this.dataFiles = response.files;
        this.error = null;
      } catch (error) {
        this.error = error.message;
        console.error("Failed to load data files:", error);
      }
    },

    async loadDataOptions() {
      try {
        const response = await backtestAPI.getDataOptions();
        this.symbols = response.symbols;
        this.timeframes = response.timeframes;
        this.dataOptions = response.data_files;

        // Set default symbol and timeframe if available
        if (this.symbols.length > 0 && this.timeframes.length > 0) {
          this.form.symbol = this.symbols[0];
          this.form.timeframe = this.timeframes[0];
          this.updateSymbolTimeframe();
        }

        this.error = null;
      } catch (error) {
        this.error = error.message;
        console.error("Failed to load data options:", error);
      }
    },

    updateStrategy(strategyName) {
      this.form.strategy = strategyName;
      // Reset strategy params to defaults
      const strategy = this.currentStrategy;
      if (strategy.params) {
        const defaults = {};
        strategy.params.forEach((param) => {
          defaults[param.name] = param.default;
        });
        this.form.strategy_params = defaults;
      }
    },

    updateSymbolTimeframe() {
      const key = `${this.form.symbol}_${this.form.timeframe}`;
      if (this.dataOptions[key]) {
        this.form.csv_file = this.dataOptions[key].filename;
      }
    },

    updateStrategyParam(paramName, value) {
      this.form.strategy_params[paramName] = value;
    },

    async runBacktest() {
      this.loading = true;
      this.error = null;
      this.results = null;

      try {
        const response = await backtestAPI.runBacktest(this.form);
        this.results = response.data;
        this.backtestId = response.backtest_id;

        // Cache the result
        this.resultsCache.set(this.backtestId, this.results);

        return this.results;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Streaming backtest actions
    startStreamingBacktest() {
      // Clean up any existing listeners first
      backtestAPI.off("backtest_started");
      backtestAPI.off("bar_update");
      backtestAPI.off("backtest_finished");
      backtestAPI.off("error");

      this.streamingMode = true;
      this.isPlaying = false;
      this.currentBarIndex = 0;
      this.bars = [];
      this.equityCurve = [];
      this.tradeLog = [];
      this.currentEquity = this.form.initial_cash;
      this.currentCash = this.form.initial_cash;
      this.positions = {};
      this.error = null;

      // Set up socket listeners
      backtestAPI.onBacktestStarted((data) => {
        this.totalBars = data.total_bars;
        this.currentEquity = data.initial_cash;
        this.currentCash = data.initial_cash;
      });

      backtestAPI.onBarUpdate((data) => {
        this.bars.push(data.bar);
        this.equityCurve.push({
          timestamp: data.bar.timestamp,
          equity: data.equity,
        });
        this.currentBarIndex++;
        this.currentEquity = data.equity;
        this.currentCash = data.cash;
        this.positions = data.positions;
        if (data.trade_log) {
          this.tradeLog.push(data.trade_log);
        }
      });

      backtestAPI.onBacktestFinished(() => {
        this.isPlaying = false;
      });

      backtestAPI.onError((error) => {
        this.error = error.message;
        this.isPlaying = false;
      });

      // Start the backtest
      backtestAPI.startStreamingBacktest(this.form);
    },

    playStreaming() {
      if (this.streamingMode) {
        this.isPlaying = true;
        backtestAPI.play();
      }
    },

    pauseStreaming() {
      if (this.streamingMode) {
        this.isPlaying = false;
        backtestAPI.pause();
      }
    },

    stepForwardStreaming() {
      if (this.streamingMode && !this.isPlaying) {
        backtestAPI.stepForward();
      }
    },

    resetStreaming() {
      if (this.streamingMode) {
        this.streamingMode = false;
        this.isPlaying = false;
        this.currentBarIndex = 0;
        this.bars = [];
        this.equityCurve = [];
        this.tradeLog = [];
        this.currentEquity = this.form.initial_cash;
        this.currentCash = this.form.initial_cash;
        this.positions = {};
        backtestAPI.reset();
      }
    },

    clearResults() {
      this.results = null;
      this.backtestId = null;
      this.error = null;
    },

    resetForm() {
      this.form = {
        symbol: "BTCUSDT",
        timeframe: "1h",
        strategy: "sma",
        initial_cash: 10000,
        csv_file: "BTCUSDT_1h.csv",
        strategy_params: {
          short_window: 5,
          long_window: 20,
        },
      };
      this.clearResults();
    },
  },
});
