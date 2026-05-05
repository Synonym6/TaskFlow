document.addEventListener("DOMContentLoaded", () => {
    const board = document.querySelector("[data-kanban-endpoint]");
    if (!board || typeof Sortable === "undefined") {
        return;
    }

    const endpoint = board.dataset.kanbanEndpoint;
    const csrfToken = document.cookie.split("csrftoken=")[1]?.split(";")[0] || "";

    document.querySelectorAll(".kanban-list").forEach((column) => {
        new Sortable(column, {
            group: "taskflow-kanban",
            animation: 180,
            onEnd: async (event) => {
                const taskId = event.item.dataset.taskId;
                const status = event.to.dataset.status;
                const position = Array.from(event.to.children).indexOf(event.item);
                await fetch(endpoint, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: JSON.stringify({
                        task_id: taskId,
                        status,
                        position,
                    }),
                });
            },
        });
    });
});
