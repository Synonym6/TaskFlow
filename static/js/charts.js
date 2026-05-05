document.addEventListener("DOMContentLoaded", () => {
    if (typeof Chart === "undefined") {
        return;
    }

    const chartInstances = [];

    function cssVar(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }

    function palette() {
        return {
            primary: cssVar("--primary") || "#6c63ff",
            primaryStrong: cssVar("--primary-strong") || "#4d6bff",
            success: cssVar("--success") || "#20b26b",
            danger: cssVar("--danger") || "#f25572",
            warning: cssVar("--warning") || "#ffb13b",
            info: cssVar("--info") || "#3b82f6",
            text: cssVar("--text") || "#17203b",
            muted: cssVar("--muted") || "#6b7290",
            border: cssVar("--border-strong") || "rgba(103, 112, 169, 0.16)",
            surface: cssVar("--surface") || "#ffffff",
            fill: "rgba(108, 99, 255, 0.12)",
        };
    }

    function destroyCharts() {
        while (chartInstances.length) {
            chartInstances.pop().destroy();
        }
    }

    function createChart(element, config) {
        if (!element) {
            return;
        }
        chartInstances.push(new Chart(element, config));
    }

    function renderDashboardChart(colors) {
        const dashboardChart = document.getElementById("dashboardProgressChart");
        if (!dashboardChart) {
            return;
        }
        const chartData = JSON.parse(dashboardChart.dataset.chart || "{}");

        createChart(dashboardChart, {
            type: "line",
            data: {
                labels: chartData.labels || [],
                datasets: [{
                    label: "Progress",
                    data: chartData.values || [],
                    borderColor: colors.primary,
                    backgroundColor: colors.fill,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: colors.surface,
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 5,
                    tension: 0.42,
                    fill: true,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        displayColors: false,
                        backgroundColor: colors.surface,
                        titleColor: colors.text,
                        bodyColor: colors.text,
                        borderColor: colors.border,
                        borderWidth: 1,
                        padding: 10,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 25,
                            color: colors.muted,
                            callback: (value) => `${value}%`,
                        },
                        grid: { color: colors.border },
                        border: { display: false },
                    },
                    x: {
                        ticks: { color: colors.muted },
                        grid: { display: false },
                        border: { display: false },
                    },
                },
            },
        });
    }

    function renderStatistics(colors) {
        const statisticsRoot = document.querySelector(".statistics-grid[data-stats]");
        if (!statisticsRoot) {
            return;
        }
        const stats = JSON.parse(statisticsRoot.dataset.stats);

        createChart(document.getElementById("completionChart"), {
            type: "line",
            data: {
                labels: stats.completion.labels,
                datasets: [{
                    data: stats.completion.values,
                    borderColor: colors.primary,
                    tension: 0.35,
                    fill: true,
                    backgroundColor: colors.fill,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    x: {
                        ticks: { color: colors.muted },
                        grid: { display: false },
                        border: { display: false },
                    },
                    y: {
                        ticks: { color: colors.muted },
                        grid: { color: colors.border },
                        border: { display: false },
                    },
                },
            },
        });

        createChart(document.getElementById("statusChart"), {
            type: "doughnut",
            data: {
                labels: Object.keys(stats.status),
                datasets: [{
                    data: Object.values(stats.status),
                    backgroundColor: [colors.primary, colors.info, colors.warning, colors.success],
                    borderColor: colors.surface,
                    borderWidth: 2,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: colors.text,
                        },
                    },
                },
            },
        });

        createChart(document.getElementById("priorityChart"), {
            type: "pie",
            data: {
                labels: Object.keys(stats.priority),
                datasets: [{
                    data: Object.values(stats.priority),
                    backgroundColor: [colors.info, colors.warning, colors.danger],
                    borderColor: colors.surface,
                    borderWidth: 2,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: colors.text,
                        },
                    },
                },
            },
        });

        createChart(document.getElementById("projectChart"), {
            type: "bar",
            data: {
                labels: stats.projects.map((item) => item.title),
                datasets: [{
                    data: stats.projects.map((item) => item.progress),
                    backgroundColor: colors.primary,
                    borderRadius: 12,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    x: {
                        ticks: { color: colors.muted },
                        grid: { display: false },
                        border: { display: false },
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: colors.muted },
                        grid: { color: colors.border },
                        border: { display: false },
                    },
                },
            },
        });
    }

    function renderCharts() {
        destroyCharts();
        const colors = palette();
        renderDashboardChart(colors);
        renderStatistics(colors);
    }

    renderCharts();
    window.addEventListener("taskflow:themechange", renderCharts);
});
