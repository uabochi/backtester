<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <div
          class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary-100"
        >
          <svg
            class="h-6 w-6 text-primary-600"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
            />
          </svg>
        </div>
        <h2
          class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white"
        >
          Create your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Start building trading strategies with Traders Casa
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="name" class="sr-only">Full Name</label>
            <input
              id="name"
              name="name"
              type="text"
              autocomplete="name"
              required
              v-model="form.name"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              placeholder="Full Name"
            />
          </div>
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="form.email"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              placeholder="Password"
            />
          </div>
          <div>
            <label for="confirmPassword" class="sr-only"
              >Confirm Password</label
            >
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.confirmPassword"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              placeholder="Confirm Password"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            id="agree-terms"
            name="agree-terms"
            type="checkbox"
            required
            v-model="form.agreeTerms"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded dark:bg-gray-800 dark:border-gray-600"
          />
          <label
            for="agree-terms"
            class="ml-2 block text-sm text-gray-900 dark:text-gray-300"
          >
            I agree to the
            <a href="#" class="text-primary-600 hover:text-primary-500"
              >Terms of Service</a
            >
            and
            <a href="#" class="text-primary-600 hover:text-primary-500"
              >Privacy Policy</a
            >
          </label>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading || !form.agreeTerms"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span
              v-if="isLoading"
              class="absolute left-1/2 transform -translate-x-1/2"
            >
              <svg
                class="animate-spin h-4 w-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            </span>
            <span v-else>Create Account</span>
          </button>
        </div>

        <div class="text-center">
          <router-link
            to="/login"
            class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
          >
            Already have an account? Sign in
          </router-link>
        </div>

        <div v-if="error" class="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                class="h-5 w-5 text-red-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-800 dark:text-red-400">{{ error }}</p>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const form = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  agreeTerms: false,
});

const isLoading = ref(false);
const error = ref("");

const validateForm = () => {
  if (form.password !== form.confirmPassword) {
    error.value = "Passwords do not match";
    return false;
  }

  if (form.password.length < 6) {
    error.value = "Password must be at least 6 characters";
    return false;
  }

  return true;
};

const handleRegister = async () => {
  if (!validateForm()) return;

  isLoading.value = true;
  error.value = "";

  const result = await authStore.register(form.email, form.password, form.name);

  if (result.success) {
    toast.success("Account created successfully!");
    router.push("/dashboard");
  } else {
    error.value = result.error || "Registration failed";
  }

  isLoading.value = false;
};
</script>
