/**
 * compare.js
 *
 * Drives the /compare page: generates one shared random array, sends it
 * plus a list of selected algorithm keys to POST /api/compare, then
 * renders four Chart.js bar charts (time, comparisons, swaps, memory) and
 * a full results table. Also wires up the comparison report download.
 */

(function () {
  "use strict";

  let sharedArray = [];
  let lastResults = [];

  const els = {
    sizeVal: document.getElementById("cSizeVal"),
    arraySize: document.getElementById("cArraySize"),
    minValue: document.getElementById("cMinValue"),
    maxValue: document.getElementById("cMaxValue"),
    generateBtn: document.getElementById("cGenerateBtn"),
    runBtn: document.getElementById("runCompareBtn"),
    downloadBtn: document.getElementById("cDownloadBtn"),
    tableBody: document.getElementById("compareTableBody"),
  };

  async function generateSharedArray() {
    try {
      const size = parseInt(els.arraySize.value, 10);
      const minValue = parseInt(els.minValue.value, 10);
      const maxValue = parseInt(els.maxValue.value, 10);
      const data = await SVApi.post("/api/array/random", { size, minValue, maxValue });
      sharedArray = data.array;
      SVToast.success(`Generated a shared array of ${sharedArray.length} values.`);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function selectedAlgorithms() {
    return Array.from(document.querySelectorAll("#algoChecks input:checked")).map((el) => el.value);
  }

  async function runComparison() {
    const algorithms = selectedAlgorithms();
    if (algorithms.length < 2) {
      SVToast.error("Select at least 2 algorithms to compare.");
      return;
    }
    if (!sharedArray.length) {
      await generateSharedArray();
    }
    try {
      const data = await SVApi.post("/api/compare", { array: sharedArray, algorithms });
      lastResults = data.results;
      renderCharts(lastResults);
      renderTable(lastResults);
      els.downloadBtn.disabled = false;
      SVToast.success(`Compared ${lastResults.length} algorithms on ${sharedArray.length} values.`);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function renderCharts(results) {
    const labels = results.map((r) => r.algorithm);
    SVCharts.createBarChart("chartTime", labels, results.map((r) => r.executionTimeMs), "Time (ms)");
    SVCharts.createBarChart("chartComparisons", labels, results.map((r) => r.comparisons), "Comparisons");
    SVCharts.createBarChart("chartSwaps", labels, results.map((r) => r.swaps), "Swaps");
    SVCharts.createBarChart("chartMemory", labels, results.map((r) => r.memoryUsageKb), "Memory (KB)");
  }

  function renderTable(results) {
    els.tableBody.innerHTML = results
      .map(
        (r) => `
      <tr>
        <td>${r.algorithm}</td>
        <td>${r.executionTimeMs.toFixed(3)}</td>
        <td>${r.comparisons.toLocaleString()}</td>
        <td>${r.swaps.toLocaleString()}</td>
        <td>${r.memoryUsageKb.toFixed(2)}</td>
        <td>${r.isStable ? "Yes" : "No"}</td>
        <td>${r.isInPlace ? "Yes" : "No"}</td>
        <td>${r.sortedSuccessfully ? "Yes" : "No"}</td>
      </tr>`
      )
      .join("");
  }

  async function downloadCompareReport() {
    if (!lastResults.length) return;
    try {
      const res = await fetch("/api/export/compare-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ results: lastResults }),
      });
      if (!res.ok) throw new Error("Failed to generate comparison report.");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "comparison_report.txt";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      SVToast.error(err.message);
    }
  }

  function init() {
    els.arraySize.addEventListener("input", () => (els.sizeVal.textContent = els.arraySize.value));
    els.generateBtn.addEventListener("click", generateSharedArray);
    els.runBtn.addEventListener("click", runComparison);
    els.downloadBtn.addEventListener("click", downloadCompareReport);
    generateSharedArray();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
