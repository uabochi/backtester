import axios from "axios";
import { io } from "socket.io-client";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5002";

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds for backtests
  headers: {
    "Content-Type": "application/json",
  },
});

// Socket.IO client
const socket = io(API_URL, {
  transports: ["websocket", "polling"],
  withCredentials: true,
  reconnectionAttempts: 5,
});

socket.on("connect", () => {
  console.log("Connected to backend via Socket.IO: ", socket.id);
});

socket.on("disconnect", () => {
  console.log("Disconnected from backend");
});

socket.on("connect_error", (error) => {
  console.error("Socket connection error:", error);
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || "Server error";
      throw new Error(message);
    } else if (error.request) {
      // Network error
      throw new Error("Network error - please check if backend is running");
    } else {
      // Other error
      throw new Error(error.message || "Unknown error");
    }
  },
);

export const backtestAPI = {
  async runBacktest(params) {
    const response = await api.post("/api/backtest", params);
    return response.data;
  },

  async getStrategies() {
    const response = await api.get("/api/strategies");
    return response.data;
  },

  async getDataFiles() {
    const response = await api.get("/api/data/files");
    return response.data;
  },

  async getDataOptions() {
    const response = await api.get("/api/data/options");
    return response.data;
  },

  async getBacktestResult(id) {
    const response = await api.get(`/api/backtest/${id}`);
    return response.data;
  },

  async healthCheck() {
    const response = await api.get("/api/health");
    return response.data;
  },

  // Streaming backtest functions
  startStreamingBacktest(params) {
    console.log("Sending start_backtest event:", params);
    socket.emit("start_backtest", params);
  },

  play() {
    console.log("Sending play event");
    socket.emit("play");
  },

  pause() {
    console.log("Sending pause event");
    socket.emit("pause");
  },

  stepForward() {
    console.log("Sending step_forward event");
    socket.emit("step_forward");
  },

  reset() {
    console.log("Sending reset event");
    socket.emit("reset");
  },

  onBacktestStarted(callback) {
    socket.on("backtest_started", callback);
  },

  onBarUpdate(callback) {
    socket.on("bar_update", callback);
  },

  onBacktestFinished(callback) {
    socket.on("backtest_finished", callback);
  },

  onError(callback) {
    socket.on("error", callback);
  },

  off(event, callback) {
    socket.off(event, callback);
  },
};

export { socket };

export default api;
