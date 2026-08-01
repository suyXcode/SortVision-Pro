/**
 * main.js
 *
 * Site-wide behavior shared by every page: dark/light theme toggle
 * (persisted to localStorage), footer year stamp, and a small toast
 * notification helper (window.SVToast) used by visualizer.js, compare.js,
 * and learn.js to surface API errors without blocking the UI.
 */

(function () {
  "use strict";

  const STORAGE_KEY = "sortvision-pro-theme";

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }

  function initTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
    const initial = stored || (prefersLight ? "light" : "dark");
    applyTheme(initial);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
  }

  document.addEventListener("DOMContentLoaded", () => {
    initTheme();

    const toggleBtn = document.getElementById("themeToggleBtn");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", toggleTheme);
    }

    const yearEl = document.getElementById("footerYear");
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }
  });

  // ------------------------------------------------------------- Toasts --

  function ensureToastStack() {
    let stack = document.querySelector(".sv-toast-stack");
    if (!stack) {
      stack = document.createElement("div");
      stack.className = "sv-toast-stack";
      document.body.appendChild(stack);
    }
    return stack;
  }

  function showToast(message, type) {
    const stack = ensureToastStack();
    const toast = document.createElement("div");
    toast.className = "sv-toast" + (type === "error" ? " sv-toast-error" : "");
    const icon = type === "error" ? "fa-triangle-exclamation" : "fa-circle-check";
    toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${message}</span>`;
    stack.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(10px)";
      toast.style.transition = "all 0.25s ease";
      setTimeout(() => toast.remove(), 260);
    }, 3200);
  }

  window.SVToast = {
    success: (msg) => showToast(msg, "success"),
    error: (msg) => showToast(msg, "error"),
  };

  // ------------------------------------------------------------- API ----

  /**
   * Thin fetch wrapper matching the Flask API's {success, data|error}
   * envelope. Throws an Error with the server's message on failure so
   * callers can just try/catch.
   */
  window.SVApi = {
    async post(url, body) {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body || {}),
      });
      const json = await res.json();
      if (!res.ok || !json.success) {
        throw new Error(json.error || "Request failed.");
      }
      return json.data;
    },
    async get(url) {
      const res = await fetch(url);
      const json = await res.json();
      if (!res.ok || !json.success) {
        throw new Error(json.error || "Request failed.");
      }
      return json.data;
    },
  };
})();
