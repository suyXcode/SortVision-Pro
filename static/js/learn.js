/**
 * learn.js
 *
 * Drives the /learn page. All algorithm content (description, complexity,
 * pseudocode, etc.) is now rendered server-side directly into the page
 * (see templates/learn.html) so it's crawlable without JavaScript — this
 * script's only job is to show the selected algorithm's panel and hide
 * the rest, and to keep the URL hash in sync for shareable deep links.
 */

(function () {
  "use strict";

  const nav = document.getElementById("learnNav");
  if (!nav) return;

  const navItems = Array.from(nav.querySelectorAll(".sv-learn-nav-item"));
  const panels = Array.from(document.querySelectorAll(".sv-learn-detail"));

  function selectAlgorithm(key, { updateHash = true } = {}) {
    let matched = false;
    panels.forEach((panel) => {
      const isMatch = panel.dataset.key === key;
      panel.hidden = !isMatch;
      if (isMatch) matched = true;
    });
    if (!matched) return;

    navItems.forEach((item) => item.classList.toggle("active", item.dataset.key === key));

    if (updateHash && history.replaceState) {
      history.replaceState(null, "", `#${key}`);
    }
  }

  nav.addEventListener("click", (e) => {
    const btn = e.target.closest(".sv-learn-nav-item");
    if (!btn) return;
    selectAlgorithm(btn.dataset.key);
  });

  // Deep-link support: /learn#quick opens straight to Quick Sort.
  const hashKey = window.location.hash.replace("#", "");
  if (hashKey && panels.some((p) => p.dataset.key === hashKey)) {
    selectAlgorithm(hashKey, { updateHash: false });
  }
})();
