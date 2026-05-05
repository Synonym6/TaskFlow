document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = document.cookie.split("csrftoken=")[1]?.split(";")[0] || "";

    async function postForm(url, payload) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: new URLSearchParams(payload),
        });
        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }
        return response.json();
    }

    document.querySelectorAll(".checklist-toggle").forEach((input) => {
        input.addEventListener("change", async () => {
            const row = input.closest("[data-check-row]");
            try {
                const data = await postForm(input.dataset.url, {});
                row?.classList.toggle("is-done", Boolean(data.is_done));
            } catch (error) {
                input.checked = !input.checked;
            }
        });
    });

    document.querySelectorAll(".subtask-toggle").forEach((input) => {
        input.addEventListener("change", async () => {
            const row = input.closest(".task-subtask-row");
            const badge = row?.querySelector("[data-subtask-status]");
            try {
                const data = await postForm(input.dataset.url, {});
                row?.classList.toggle("is-done", data.status === "done");
                if (badge) {
                    badge.textContent = data.status_label;
                    badge.className = `task-status-badge task-status-badge--${data.status}`;
                    badge.setAttribute("data-subtask-status", "");
                }
            } catch (error) {
                input.checked = !input.checked;
            }
        });
    });

    const statusSelect = document.querySelector("[data-task-status-select]");
    if (statusSelect) {
        statusSelect.addEventListener("change", async () => {
            const value = statusSelect.value;
            if (value === "overdue") {
                return;
            }
            try {
                await postForm(statusSelect.dataset.url, { status: value });
            } catch (error) {
                window.location.reload();
            }
        });
    }

    const prioritySelect = document.querySelector("[data-task-priority-select]");
    if (prioritySelect) {
        prioritySelect.addEventListener("change", async () => {
            try {
                await postForm(prioritySelect.dataset.url, { priority: prioritySelect.value });
            } catch (error) {
                window.location.reload();
            }
        });
    }

    const showActivityButton = document.querySelector("[data-show-activity]");
    if (showActivityButton) {
        showActivityButton.addEventListener("click", () => {
            document.querySelectorAll(".task-activity-item.is-extra").forEach((item) => {
                item.hidden = false;
            });
            showActivityButton.remove();
        });
    }
});
