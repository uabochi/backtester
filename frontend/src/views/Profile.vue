<template>
  <div class="profile-view">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Profile
        </h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Manage your account settings and preferences
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Information -->
        <div class="lg:col-span-2">
          <div class="card">
            <h2
              class="text-xl font-semibold text-gray-900 dark:text-white mb-6"
            >
              Profile Information
            </h2>

            <form @submit.prevent="updateProfile" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                  >
                    First Name
                  </label>
                  <input
                    v-model="profileForm.firstName"
                    type="text"
                    class="input"
                    required
                  />
                </div>

                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                  >
                    Last Name
                  </label>
                  <input
                    v-model="profileForm.lastName"
                    type="text"
                    class="input"
                    required
                  />
                </div>
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Email Address
                </label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="input"
                  required
                />
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Bio
                </label>
                <textarea
                  v-model="profileForm.bio"
                  rows="4"
                  class="input"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="isUpdating"
                  class="btn-primary disabled:opacity-50"
                >
                  {{ isUpdating ? "Updating..." : "Update Profile" }}
                </button>
              </div>
            </form>
          </div>

          <!-- Change Password -->
          <div class="card mt-8">
            <h2
              class="text-xl font-semibold text-gray-900 dark:text-white mb-6"
            >
              Change Password
            </h2>

            <form @submit.prevent="changePassword" class="space-y-6">
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Current Password
                </label>
                <input
                  v-model="passwordForm.currentPassword"
                  type="password"
                  class="input"
                  required
                />
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  New Password
                </label>
                <input
                  v-model="passwordForm.newPassword"
                  type="password"
                  class="input"
                  required
                  minlength="8"
                />
              </div>

              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Confirm New Password
                </label>
                <input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  class="input"
                  required
                  minlength="8"
                />
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="isChangingPassword"
                  class="btn-primary disabled:opacity-50"
                >
                  {{ isChangingPassword ? "Changing..." : "Change Password" }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Account Stats -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Account Statistics
            </h3>

            <div class="space-y-4">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >Member Since</span
                >
                <span class="font-medium">{{
                  new Date(user.createdAt).toLocaleDateString()
                }}</span>
              </div>

              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >Total Backtests</span
                >
                <span class="font-medium">{{ user.totalBacktests || 0 }}</span>
              </div>

              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >Active Strategies</span
                >
                <span class="font-medium">{{
                  user.activeStrategies || 0
                }}</span>
              </div>

              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Total P&L</span>
                <span
                  class="font-medium"
                  :class="
                    (user.totalPnL || 0) >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  "
                >
                  {{ (user.totalPnL || 0) >= 0 ? "+" : ""
                  }}{{ (user.totalPnL || 0).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Preferences -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Preferences
            </h3>

            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >Email Notifications</span
                >
                <input
                  v-model="preferences.emailNotifications"
                  type="checkbox"
                  class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
              </div>

              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Dark Mode</span>
                <input
                  v-model="preferences.darkMode"
                  type="checkbox"
                  class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
              </div>

              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >Auto-save Backtests</span
                >
                <input
                  v-model="preferences.autoSave"
                  type="checkbox"
                  class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
              </div>
            </div>

            <div class="mt-4">
              <button
                @click="updatePreferences"
                :disabled="isUpdatingPreferences"
                class="btn-secondary w-full disabled:opacity-50"
              >
                {{ isUpdatingPreferences ? "Saving..." : "Save Preferences" }}
              </button>
            </div>
          </div>

          <!-- Danger Zone -->
          <div class="card border-red-200 dark:border-red-800">
            <h3 class="text-lg font-medium text-red-600 dark:text-red-400 mb-4">
              Danger Zone
            </h3>

            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Once you delete your account, there is no going back. Please be
              certain.
            </p>

            <button @click="showDeleteModal = true" class="btn-danger w-full">
              Delete Account
            </button>
          </div>
        </div>
      </div>

      <!-- Delete Account Modal -->
      <div
        v-if="showDeleteModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        @click="showDeleteModal = false"
      >
        <div
          class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white dark:bg-gray-800"
          @click.stop
        >
          <div class="mt-3">
            <h3 class="text-lg font-medium text-red-600 dark:text-red-400 mb-4">
              Delete Account
            </h3>

            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              This action cannot be undone. This will permanently delete your
              account and remove all your data from our servers.
            </p>

            <div class="mb-4">
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Type "DELETE" to confirm
              </label>
              <input
                v-model="deleteConfirmation"
                type="text"
                class="input"
                placeholder="DELETE"
              />
            </div>

            <div class="flex justify-end space-x-3">
              <button @click="showDeleteModal = false" class="btn-secondary">
                Cancel
              </button>
              <button
                @click="deleteAccount"
                :disabled="deleteConfirmation !== 'DELETE' || isDeleting"
                class="btn-danger disabled:opacity-50"
              >
                {{ isDeleting ? "Deleting..." : "Delete Account" }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useToast } from "vue-toastification";
import { useAuthStore } from "../stores/auth";

const toast = useToast();
const authStore = useAuthStore();

const user = ref({});
const showDeleteModal = ref(false);
const deleteConfirmation = ref("");
const isUpdating = ref(false);
const isChangingPassword = ref(false);
const isUpdatingPreferences = ref(false);
const isDeleting = ref(false);

const profileForm = reactive({
  firstName: "",
  lastName: "",
  email: "",
  bio: "",
});

const passwordForm = reactive({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const preferences = reactive({
  emailNotifications: true,
  darkMode: false,
  autoSave: true,
});

const loadProfile = async () => {
  try {
    const response = await fetch("/api/user/profile", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      user.value = data.user;
      Object.assign(profileForm, data.user);
      Object.assign(preferences, data.preferences || preferences);
    }
  } catch (error) {
    console.error("Failed to load profile:", error);
    toast.error("Failed to load profile");
  }
};

const updateProfile = async () => {
  isUpdating.value = true;

  try {
    const response = await fetch("/api/user/profile", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(profileForm),
    });

    if (response.ok) {
      toast.success("Profile updated successfully!");
      loadProfile();
    } else {
      throw new Error("Failed to update profile");
    }
  } catch (error) {
    console.error("Failed to update profile:", error);
    toast.error("Failed to update profile");
  } finally {
    isUpdating.value = false;
  }
};

const changePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    toast.error("New passwords do not match");
    return;
  }

  isChangingPassword.value = true;

  try {
    const response = await fetch("/api/user/change-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        currentPassword: passwordForm.currentPassword,
        newPassword: passwordForm.newPassword,
      }),
    });

    if (response.ok) {
      toast.success("Password changed successfully!");
      passwordForm.currentPassword = "";
      passwordForm.newPassword = "";
      passwordForm.confirmPassword = "";
    } else {
      throw new Error("Failed to change password");
    }
  } catch (error) {
    console.error("Failed to change password:", error);
    toast.error("Failed to change password");
  } finally {
    isChangingPassword.value = false;
  }
};

const updatePreferences = async () => {
  isUpdatingPreferences.value = true;

  try {
    const response = await fetch("/api/user/preferences", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(preferences),
    });

    if (response.ok) {
      toast.success("Preferences updated successfully!");
    } else {
      throw new Error("Failed to update preferences");
    }
  } catch (error) {
    console.error("Failed to update preferences:", error);
    toast.error("Failed to update preferences");
  } finally {
    isUpdatingPreferences.value = false;
  }
};

const deleteAccount = async () => {
  isDeleting.value = true;

  try {
    const response = await fetch("/api/user/delete", {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      toast.success("Account deleted successfully");
      authStore.logout();
      // Redirect to login page
      window.location.href = "/login";
    } else {
      throw new Error("Failed to delete account");
    }
  } catch (error) {
    console.error("Failed to delete account:", error);
    toast.error("Failed to delete account");
  } finally {
    isDeleting.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>
