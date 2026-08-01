/**
 * charts.js
 *
 * Small reusable Chart.js factory helpers shared by the single-run stats
 * chart (visualizer.js) and the four comparison charts (compare.js). Keeps
 * chart color/styling consistent across the app without duplicating
 * Chart.js configuration in both places.
 */

(function () {
  "use strict";

  function readColor(varName) {
    return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
  }

  const PALETTE = [
    "#d4af37", "#3d6ec2", "#38c98f", "#e0475a", "#b06ee0", "#f2c94c", "#5b8de0", "#e69a2c", "#7fd1ff",
  ];

  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.color = "#a9b0c9";

  function baseGridOptions() {
    const gridColor = "rgba(255,255,255,0.06)";
    return {
      scales: {
        x: { grid: { color: gridColor }, ticks: { color: "#a9b0c9" } },
        y: { grid: { color: gridColor }, ticks: { color: "#a9b0c9" }, beginAtZero: true },
      },
      plugins: {
        legend: { display: false },
        tooltip: { backgroundColor: "#131a33", borderColor: "#d4af37", borderWidth: 1, padding: 10 },
      },
      responsive: true,
      maintainAspectRatio: false,
    };
  }

  /** Create (or recreate) a single-metric bar chart on the given canvas id. */
  function createBarChart(canvasId, labels, data, label) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    if (canvas._chartInstance) {
      canvas._chartInstance.destroy();
    }

    const chart = new Chart(canvas.getContext("2d"), {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label,
            data,
            backgroundColor: labels.map((_, i) => PALETTE[i % PALETTE.length]),
            borderRadius: 6,
            maxBarThickness: 56,
          },
        ],
      },
      options: baseGridOptions(),
    });

    canvas._chartInstance = chart;
    return chart;
  }

  /** Create a single-run "multi metric" comparison bar chart (execution snapshot). */
  function createMultiMetricChart(canvasId, result) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    if (canvas._chartInstance) {
      canvas._chartInstance.destroy();
    }

    const chart = new Chart(canvas.getContext("2d"), {
      type: "bar",
      data: {
        labels: ["Time (ms)", "Comparisons", "Swaps", "Memory (KB)"],
        datasets: [
          {
            label: result.algorithm,
            data: [
              result.executionTimeMs,
              result.comparisons,
              result.swaps,
              result.memoryUsageKb,
            ],
            backgroundColor: [PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]],
            borderRadius: 6,
            maxBarThickness: 56,
          },
        ],
      },
      options: baseGridOptions(),
    });

    canvas._chartInstance = chart;
    return chart;
  }

  window.SVCharts = { createBarChart, createMultiMetricChart, PALETTE };
})();
