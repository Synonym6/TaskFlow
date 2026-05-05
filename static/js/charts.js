document.addEventListener("DOMContentLoaded", () => {
    const dashboardChart = document.getElementById("dashboardProgressChart");
    if (dashboardChart) {
        const chartData = JSON.parse(dashboardChart.dataset.chart || "{}");
        new Chart(dashboardChart, {
            type: "line",
            data: {
                labels: chartData.labels || [],
                datasets: [{
                    label: "Progress",
                    data: chartData.values || [],
                    borderColor: "#6C4DFF",
                    backgroundColor: "rgba(108, 77, 255, 0.12)",
                    pointBackgroundColor: "#6C4DFF",
                    pointBorderColor: "#ffffff",
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
                        backgroundColor: "#101428",
                        padding: 10,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 25,
                            color: "#8A90A6",
                            callback: (value) => `${value}%`,
                        },
                        grid: { color: "rgba(232, 234, 243, 0.9)" },
                        border: { display: false },
                    },
                    x: {
                        ticks: { color: "#8A90A6" },
                        grid: { display: false },
                        border: { display: false },
                    },
                },
            },
        });
    }

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
