/**
 * visualizer.js
 *
 * Drives the main /visualizer dashboard:
 *   - Random array generation / manual array entry (calls the Flask API)
 *   - Algorithm selection + live complexity badges + learning panel
 *   - Running a sort (fetches the full step list from the API in one call)
 *   - Animating the returned steps bar-by-bar with pause/resume/reset and
 *     a speed slider, all driven by setTimeout so it can be paused cleanly
 *   - Populating the results grid, run chart, and triggering report export
 *
 * The backend computes ALL steps up front (see algorithms/base.py); this
 * script's only job is to play that step list back at a controllable pace.
 */

(function () {
  "use strict";

  const state = {
    array: [],
    algoKey: "bubble",
    algoMeta: {},           // cache of /api/algorithms/<key> responses
    steps: [],
    stepIndex: 0,
    playing: false,
    paused: false,
    timerId: null,
    lastResult: null,
  };

  // ------------------------------------------------------------ Elements --

  const els = {
    sizeVal: document.getElementById("sizeVal"),
    arraySize: document.getElementById("arraySize"),
    minValue: document.getElementById("minValue"),
    maxValue: document.getElementById("maxValue"),
    generateBtn: document.getElementById("generateBtn"),
    manualInput: document.getElementById("manualInput"),
    useManualBtn: document.getElementById("useManualBtn"),
    algoSelect: document.getElementById("algoSelect"),
    speedRange: document.getElementById("speedRange"),
    sortBtn: document.getElementById("sortBtn"),
    pauseBtn: document.getElementById("pauseBtn"),
    resumeBtn: document.getElementById("resumeBtn"),
    resetBtn: document.getElementById("resetBtn"),
    fullscreenBtn: document.getElementById("fullscreenBtn"),
    fullscreenLabel: document.getElementById("fullscreenLabel"),
    algoTitle: document.getElementById("algoTitle"),
    badgeBest: document.getElementById("badgeBest"),
    badgeAvg: document.getElementById("badgeAvg"),
    badgeWorst: document.getElementById("badgeWorst"),
    badgeSpace: document.getElementById("badgeSpace"),
    barCanvas: document.getElementById("barCanvas"),
    canvasEmpty: document.getElementById("canvasEmpty"),
    sortProgress: document.getElementById("sortProgress"),
    stepCounter: document.getElementById("stepCounter"),
    downloadReportBtn: document.getElementById("downloadReportBtn"),
    root: document.getElementById("visualizerRoot"),
  };

  const resultEls = {
    resAlgo: document.getElementById("resAlgo"),
    resTime: document.getElementById("resTime"),
    resComparisons: document.getElementById("resComparisons"),
    resSwaps: document.getElementById("resSwaps"),
    resMemory: document.getElementById("resMemory"),
    resLength: document.getElementById("resLength"),
    resStable: document.getElementById("resStable"),
    resInPlace: document.getElementById("resInPlace"),
    resSorted: document.getElementById("resSorted"),
  };

  const learnEls = {
    name: document.getElementById("learnAlgoName"),
    description: document.getElementById("learnDescription"),
    principle: document.getElementById("learnPrinciple"),
    advantages: document.getElementById("learnAdvantages"),
    disadvantages: document.getElementById("learnDisadvantages"),
    applications: document.getElementById("learnApplications"),
    pseudocode: document.getElementById("learnPseudocode"),
  };

  // -------------------------------------------------------- Bar rendering --

  function renderStaticArray(array) {
    els.barCanvas.innerHTML = "";
    if (!array.length) {
      els.canvasEmpty.classList.remove("d-none");
      return;
    }
    els.canvasEmpty.classList.add("d-none");
    const max = Math.max(...array, 1);
    const min = Math.min(...array, 0);
    const range = Math.max(max - min, 1);

    array.forEach((value) => {
      const bar = document.createElement("div");
      bar.className = "sv-bar";
      const heightPct = 8 + ((value - min) / range) * 92;
      bar.style.height = heightPct + "%";
      bar.title = value;
      els.barCanvas.appendChild(bar);
    });
  }

  function renderStep(step, array) {
    const bars = els.barCanvas.children;
    const max = Math.max(...step.array, 1);
    const min = Math.min(...step.array, 0);
    const range = Math.max(max - min, 1);

    for (let i = 0; i < step.array.length; i++) {
      const bar = bars[i];
      if (!bar) continue;
      const heightPct = 8 + ((step.array[i] - min) / range) * 92;
      bar.style.height = heightPct + "%";
      bar.title = step.array[i];
      bar.className = "sv-bar";
    }

    step.indices.forEach((i) => {
      const bar = bars[i];
      if (!bar) return;
      bar.classList.add("sv-b-" + mapAction(step.action));
    });

    (step.sortedIndices || []).forEach((i) => {
      const bar = bars[i];
      if (bar && !step.indices.includes(i)) bar.classList.add("sv-b-sorted");
    });
  }

  function mapAction(action) {
    if (action === "overwrite") return "swap";
    if (action === "default") return "default";
    return action;
  }

  // ------------------------------------------------------- Array sourcing --

  async function generateRandomArray() {
    try {
      const size = parseInt(els.arraySize.value, 10);
      const minValue = parseInt(els.minValue.value, 10);
      const maxValue = parseInt(els.maxValue.value, 10);
      const data = await SVApi.post("/api/array/random", { size, minValue, maxValue });
      setArray(data.array);
      SVToast.success(`Generated a random array of ${data.array.length} values.`);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  async function useManualArray() {
    try {
      const data = await SVApi.post("/api/array/validate", { raw: els.manualInput.value });
      setArray(data.array);
      SVToast.success(`Loaded a manual array of ${data.array.length} values.`);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function setArray(array) {
    stopPlayback();
    state.array = array;
    state.steps = [];
    state.stepIndex = 0;
    state.lastResult = null;
    renderStaticArray(array);
    updateProgress(0, 0);
    resetResults();
    els.downloadReportBtn.disabled = true;
    setPlaybackButtons({ canSort: array.length > 0, canPause: false, canResume: false });
  }

  // -------------------------------------------------------- Algorithm info --

  async function loadAlgoMeta(key) {
    if (state.algoMeta[key]) return state.algoMeta[key];
    const data = await SVApi.get(`/api/algorithms/${key}`);
    state.algoMeta[key] = data;
    return data;
  }

  async function onAlgoChange() {
    state.algoKey = els.algoSelect.value;
    try {
      const meta = await loadAlgoMeta(state.algoKey);
      applyAlgoMeta(meta);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function applyAlgoMeta(meta) {
    els.algoTitle.textContent = meta.name;
    els.badgeBest.textContent = "Best: " + meta.bestCase;
    els.badgeAvg.textContent = "Avg: " + meta.averageCase;
    els.badgeWorst.textContent = "Worst: " + meta.worstCase;
    els.badgeSpace.textContent = "Space: " + meta.spaceComplexity;

    learnEls.name.textContent = meta.name;
    learnEls.description.textContent = meta.description;
    learnEls.principle.textContent = meta.workingPrinciple;
    learnEls.advantages.innerHTML = meta.advantages.map((a) => `<li>${a}</li>`).join("");
    learnEls.disadvantages.innerHTML = meta.disadvantages.map((a) => `<li>${a}</li>`).join("");
    learnEls.applications.innerHTML = meta.applications.map((a) => `<li>${a}</li>`).join("");
    learnEls.pseudocode.textContent = meta.pseudoCode;
  }

  // ------------------------------------------------------------- Sorting --

  async function runSort() {
    if (!state.array.length) {
      SVToast.error("Generate or enter an array first.");
      return;
    }
    try {
      setPlaybackButtons({ canSort: false, canPause: false, canResume: false });
      const result = await SVApi.post(`/api/sort/${state.algoKey}`, { array: state.array });
      state.lastResult = result;
      state.steps = result.steps;
      state.stepIndex = 0;
      renderStaticArray(result.originalArray);
      state.playing = true;
      state.paused = false;
      setPlaybackButtons({ canSort: false, canPause: true, canResume: false });
      playFrom(0);
    } catch (err) {
      SVToast.error(err.message);
      setPlaybackButtons({ canSort: true, canPause: false, canResume: false });
    }
  }

  function speedToDelayMs() {
    const speed = parseInt(els.speedRange.value, 10); // 1 (slow) - 100 (fast)
    const minDelay = 4;
    const maxDelay = 260;
    return Math.round(maxDelay - ((speed - 1) / 99) * (maxDelay - minDelay));
  }

  function playFrom(index) {
    clearTimer();
    const step = () => {
      if (state.paused) return;
      if (index >= state.steps.length) {
        finishPlayback();
        return;
      }
      renderStep(state.steps[index], state.array);
      updateProgress(index + 1, state.steps.length);
      state.stepIndex = index + 1;
      index += 1;
      state.timerId = setTimeout(step, speedToDelayMs());
    };
    step();
  }

  function pausePlayback() {
    state.paused = true;
    clearTimer();
    setPlaybackButtons({ canSort: false, canPause: false, canResume: true });
  }

  function resumePlayback() {
    if (!state.steps.length) return;
    state.paused = false;
    setPlaybackButtons({ canSort: false, canPause: true, canResume: false });
    playFrom(state.stepIndex);
  }

  function resetPlayback() {
    stopPlayback();
    if (state.lastResult) {
      renderStaticArray(state.lastResult.originalArray);
      state.array = state.lastResult.originalArray;
    } else {
      renderStaticArray(state.array);
    }
    state.steps = [];
    state.stepIndex = 0;
    updateProgress(0, 0);
    resetResults();
    els.downloadReportBtn.disabled = true;
    setPlaybackButtons({ canSort: state.array.length > 0, canPause: false, canResume: false });
  }

  function stopPlayback() {
    clearTimer();
    state.playing = false;
    state.paused = false;
  }

  function clearTimer() {
    if (state.timerId) {
      clearTimeout(state.timerId);
      state.timerId = null;
    }
  }

  function finishPlayback() {
    state.playing = false;
    state.paused = false;
    updateProgress(state.steps.length, state.steps.length);
    setPlaybackButtons({ canSort: true, canPause: false, canResume: false });
    if (state.lastResult) {
      populateResults(state.lastResult);
      SVCharts.createMultiMetricChart("statsChart", state.lastResult);
      els.downloadReportBtn.disabled = false;
      state.array = state.lastResult.sortedArray;
    }
  }

  function updateProgress(current, total) {
    const pct = total ? Math.round((current / total) * 100) : 0;
    els.sortProgress.style.width = pct + "%";
    els.stepCounter.textContent = `Step ${current} / ${total}`;
  }

  function setPlaybackButtons({ canSort, canPause, canResume }) {
    els.sortBtn.disabled = !canSort;
    els.pauseBtn.disabled = !canPause;
    els.resumeBtn.disabled = !canResume;
  }

  function resetResults() {
    Object.values(resultEls).forEach((el) => (el.textContent = "—"));
  }

  function populateResults(result) {
    resultEls.resAlgo.textContent = result.algorithm;
    resultEls.resTime.textContent = result.executionTimeMs.toFixed(3) + " ms";
    resultEls.resComparisons.textContent = result.comparisons.toLocaleString();
    resultEls.resSwaps.textContent = result.swaps.toLocaleString();
    resultEls.resMemory.textContent = result.memoryUsageKb.toFixed(2) + " KB";
    resultEls.resLength.textContent = result.arrayLength;
    resultEls.resStable.textContent = result.isStable ? "Yes" : "No";
    resultEls.resInPlace.textContent = result.isInPlace ? "Yes" : "No";
    resultEls.resSorted.textContent = result.sortedSuccessfully ? "Yes" : "No";
  }

  // -------------------------------------------------------------- Export --

  async function downloadReport() {
    if (!state.lastResult) return;
    try {
      const res = await fetch("/api/export/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ result: state.lastResult }),
      });
      if (!res.ok) throw new Error("Failed to generate report.");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${state.lastResult.algorithm.toLowerCase().replace(/\s+/g, "_")}_report.txt`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  // ------------------------------------------------------------- Tabs UI --

  function initTabs() {
    document.querySelectorAll(".sv-tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".sv-tab").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const target = tab.dataset.tab;
        document.querySelectorAll(".sv-tab-panel").forEach((panel) => {
          panel.classList.toggle("d-none", panel.dataset.panel !== target);
        });
      });
    });
  }

  // ------------------------------------------------------------ Fullscreen --
  //
  // Prefers the real browser Fullscreen API (covers the whole screen,
  // responds correctly to Esc, works with screen readers/OS chrome) and
  // falls back to a CSS-only "fullscreen" class for browsers that don't
  // support requestFullscreen on arbitrary elements (e.g. iOS Safari).

  let fullscreenIsFallback = false;

  function nativeFullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || null;
  }

  function requestNativeFullscreen(el) {
    const request = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!request) return Promise.reject(new Error("Fullscreen API not supported."));
    const result = request.call(el);
    return result instanceof Promise ? result : Promise.resolve();
  }

  function exitNativeFullscreen() {
    const exit = document.exitFullscreen || document.webkitExitFullscreen;
    if (!exit) return Promise.resolve();
    const result = exit.call(document);
    return result instanceof Promise ? result : Promise.resolve();
  }

  function isFullscreenActive() {
    return !!nativeFullscreenElement() || els.root.classList.contains("sv-fullscreen");
  }

  function syncFullscreenUI(isFull) {
    const icon = els.fullscreenBtn.querySelector("i");
    icon.className = isFull ? "fa-solid fa-compress" : "fa-solid fa-expand";
    els.fullscreenLabel.textContent = isFull ? "Exit Fullscreen" : "Fullscreen";
    els.root.classList.toggle("sv-fullscreen", isFull);
  }

  async function enterFullscreen() {
    try {
      await requestNativeFullscreen(els.root);
      fullscreenIsFallback = false;
      // syncFullscreenUI runs via the fullscreenchange listener below.
    } catch (err) {
      fullscreenIsFallback = true;
      syncFullscreenUI(true);
    }
  }

  async function exitFullscreen() {
    if (nativeFullscreenElement()) {
      await exitNativeFullscreen();
      // syncFullscreenUI runs via the fullscreenchange listener below.
    } else {
      fullscreenIsFallback = false;
      syncFullscreenUI(false);
    }
  }

  function toggleFullscreen() {
    if (isFullscreenActive()) {
      exitFullscreen();
    } else {
      enterFullscreen();
    }
  }

  function initFullscreenListeners() {
    const handler = () => {
      // Native fullscreen was exited (including via Esc) or entered outside
      // our own toggle call — keep the button/icon/layout in sync either way.
      if (fullscreenIsFallback) return;
      syncFullscreenUI(!!nativeFullscreenElement());
    };
    document.addEventListener("fullscreenchange", handler);
    document.addEventListener("webkitfullscreenchange", handler);
  }

  // ----------------------------------------------------------------- Init --

  function init() {
    initTabs();

    els.arraySize.addEventListener("input", () => (els.sizeVal.textContent = els.arraySize.value));
    els.generateBtn.addEventListener("click", generateRandomArray);
    els.useManualBtn.addEventListener("click", useManualArray);
    els.algoSelect.addEventListener("change", onAlgoChange);
    els.sortBtn.addEventListener("click", runSort);
    els.pauseBtn.addEventListener("click", pausePlayback);
    els.resumeBtn.addEventListener("click", resumePlayback);
    els.resetBtn.addEventListener("click", resetPlayback);
    els.downloadReportBtn.addEventListener("click", downloadReport);
    els.fullscreenBtn.addEventListener("click", toggleFullscreen);
    initFullscreenListeners();

    // Preselect algorithm from ?algo= query param, if present.
    const params = new URLSearchParams(window.location.search);
    const preselect = params.get("algo");
    if (preselect && els.algoSelect.querySelector(`option[value="${preselect}"]`)) {
      els.algoSelect.value = preselect;
    }
    state.algoKey = els.algoSelect.value;
    onAlgoChange();

    generateRandomArray();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
