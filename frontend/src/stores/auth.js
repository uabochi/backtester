import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { jwtDecode } from "jwt-decode";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5002";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || "");
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);

  const setToken = (newToken) => {
    token.value = newToken;
    localStorage.setItem("token", newToken);
    try {
      user.value = jwtDecode(newToken);
    } catch (error) {
      console.error("Invalid token:", error);
      user.value = null;
    }
  };

  const logout = () => {
    token.value = "";
    user.value = null;
    localStorage.removeItem("token");
  };

  const login = async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      setToken(data.token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const register = async (email, password, name) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        throw new Error("Registration failed");
      }

      const data = await response.json();
      setToken(data.token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  // Initialize user from token if available
  if (token.value) {
    try {
      user.value = jwtDecode(token.value);
    } catch (error) {
      console.error("Invalid stored token:", error);
      logout();
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    logout,
    login,
    register,
  };
});
