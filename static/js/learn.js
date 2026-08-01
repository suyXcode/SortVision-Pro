/**
 * learn.js
 *
 * Drives the /learn page: clicking an algorithm in the left-hand nav
 * fetches its metadata from GET /api/algorithms/<key> (cached after first
 * fetch) and renders it into the detail panel, including the "Visualize
 * This Algorithm" deep link back to /visualizer?algo=<key>.
 */

(function () {
  "use strict";

  const cache = {};

  const els = {
    nav: document.getElementById("learnNav"),
    name: document.getElementById("detailName"),
    stable: document.getElementById("detailStable"),
    inPlace: document.getElementById("detailInPlace"),
    adaptive: document.getElementById("detailAdaptive"),
    best: document.getElementById("detailBest"),
    avg: document.getElementById("detailAvg"),
    worst: document.getElementById("detailWorst"),
    space: document.getElementById("detailSpace"),
    description: document.getElementById("detailDescription"),
    principle: document.getElementById("detailPrinciple"),
    advantages: document.getElementById("detailAdvantages"),
    disadvantages: document.getElementById("detailDisadvantages"),
    applications: document.getElementById("detailApplications"),
    pseudocode: document.getElementById("detailPseudocode"),
    visualizeLink: document.getElementById("detailVisualizeLink"),
  };

  async function loadAlgorithm(key) {
    if (cache[key]) return cache[key];
    const data = await SVApi.get(`/api/algorithms/${key}`);
    cache[key] = data;
    return data;
  }

  function render(meta, key) {
    els.name.textContent = meta.name;
    els.stable.textContent = "Stable: " + (meta.isStable ? "Yes" : "No");
    els.inPlace.textContent = "In Place: " + (meta.isInPlace ? "Yes" : "No");
    els.adaptive.textContent = "Adaptive: " + (meta.isAdaptive ? "Yes" : "No");
    els.best.textContent = meta.bestCase;
    els.avg.textContent = meta.averageCase;
    els.worst.textContent = meta.worstCase;
    els.space.textContent = meta.spaceComplexity;
    els.description.textContent = meta.description;
    els.principle.textContent = meta.workingPrinciple;
    els.advantages.innerHTML = meta.advantages.map((a) => `<li>${a}</li>`).join("");
    els.disadvantages.innerHTML = meta.disadvantages.map((a) => `<li>${a}</li>`).join("");
    els.applications.innerHTML = meta.applications.map((a) => `<li>${a}</li>`).join("");
    els.pseudocode.textContent = meta.pseudoCode;
    els.visualizeLink.href = `/visualizer?algo=${key}`;
  }

  async function selectAlgorithm(key, btn) {
    document.querySelectorAll(".sv-learn-nav-item").forEach((el) => el.classList.remove("active"));
    if (btn) btn.classList.add("active");
    try {
      const meta = await loadAlgorithm(key);
      render(meta, key);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function init() {
    els.nav.addEventListener("click", (e) => {
      const btn = e.target.closest(".sv-learn-nav-item");
      if (!btn) return;
      selectAlgorithm(btn.dataset.key, btn);
    });

    const first = els.nav.querySelector(".sv-learn-nav-item");
    if (first) selectAlgorithm(first.dataset.key, first);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
