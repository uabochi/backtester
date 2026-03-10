import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "@/views/Dashboard.vue";
import Backtest from "@/views/Backtest.vue";
import Strategies from "@/views/Strategies.vue";
import History from "@/views/History.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Profile from "@/views/Profile.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/backtest",
    name: "Backtest",
    component: Backtest,
    meta: { requiresAuth: true },
  },
  {
    path: "/strategies",
    name: "Strategies",
    component: Strategies,
    meta: { requiresAuth: true },
  },
  {
    path: "/history",
    name: "History",
    component: History,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");
  } else if (
    (to.name === "Login" || to.name === "Register") &&
    isAuthenticated
  ) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
