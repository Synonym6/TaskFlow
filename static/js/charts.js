document.addEventListener("DOMContentLoaded", () => {
    const getChartTheme = () => {
        const isDarkTheme = document.documentElement.getAttribute("data-theme") === "dark";
        return {
            textColor: isDarkTheme ? "#98A4C9" : "#8A90A6",
            gridColor: isDarkTheme ? "rgba(159, 176, 255, 0.14)" : "rgba(232, 234, 243, 0.9)",
            tooltipBg: isDarkTheme ? "#0B1120" : "#101428",
            pointBorder: isDarkTheme ? "#121B31" : "#ffffff",
        };
    };

    const dashboardChart = document.getElementById("dashboardProgressChart");
    let dashboardChartInstance = null;
    if (dashboardChart) {
        const chartData = JSON.parse(dashboardChart.dataset.chart || "{}");
        const colors = getChartTheme();
        dashboardChartInstance = new Chart(dashboardChart, {
            type: "line",
            data: {
                labels: chartData.labels || [],
                datasets: [{
                    label: "Progress",
                    data: chartData.values || [],
                    borderColor: "#6C4DFF",
                    backgroundColor: "rgba(108, 77, 255, 0.12)",
                    pointBackgroundColor: "#6C4DFF",
                    pointBorderColor: colors.pointBorder,
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
                        backgroundColor: colors.tooltipBg,
                        padding: 10,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 25,
                            color: colors.textColor,
                            callback: (value) => `${value}%`,
                        },
                        grid: { color: colors.gridColor },
                        border: { display: false },
                    },
                    x: {
                        ticks: { color: colors.textColor },
                        grid: { display: false },
                        border: { display: false },
                    },
                },
            },
        });
    }

    window.addEventListener("taskflow:theme-change", () => {
        if (!dashboardChartInstance) {
            return;
        }
        const colors = getChartTheme();
        dashboardChartInstance.data.datasets[0].pointBorderColor = colors.pointBorder;
        dashboardChartInstance.options.plugins.tooltip.backgroundColor = colors.tooltipBg;
        dashboardChartInstance.options.scales.y.ticks.color = colors.textColor;
        dashboardChartInstance.options.scales.y.grid.color = colors.gridColor;
        dashboardChartInstance.options.scales.x.ticks.color = colors.textColor;
        dashboardChartInstance.update();
    });

    const statisticsRoot = document.querySelector(".statistics-grid[data-stats]");
    if (!statisticsRoot) {
        return;
    }
    const stats = JSON.parse(statisticsRoot.dataset.stats);

    new Chart(document.getElementById("completionChart"), {
        type: "line",
        data: {
            labels: stats.completion.labels,
            datasets: [{ data: stats.completion.values, borderColor: "#6c63ff", tension: 0.35, fill: true, backgroundColor: "rgba(108,99,255,.12)" }],
        },
        options: { responsive: true, maintainAspectRatio: false },
    });

    new Chart(document.getElementById("statusChart"), {
        type: "doughnut",
        data: {
            labels: Object.keys(stats.status),
            datasets: [{ data: Object.values(stats.status), backgroundColor: ["#6c63ff", "#4d6bff", "#ffb13b", "#20b26b"] }],
        },
        options: { responsive: true, maintainAspectRatio: false },
    });

    new Chart(document.getElementById("priorityChart"), {
        type: "pie",
        data: {
            labels: Object.keys(stats.priority),
            datasets: [{ data: Object.values(stats.priority), backgroundColor: ["#4d6bff", "#ffb13b", "#f25572"] }],
        },
        options: { responsive: true, maintainAspectRatio: false },
    });

    new Chart(document.getElementById("projectChart"), {
        type: "bar",
        data: {
            labels: stats.projects.map((item) => item.title),
            datasets: [{ data: stats.projects.map((item) => item.progress), backgroundColor: "#6c63ff", borderRadius: 12 }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 100 } },
        },
    });
});
