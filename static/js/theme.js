document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const lockedTheme = document.body?.dataset.lockTheme;
    const toggle = document.querySelector("[data-theme-toggle]");
    const endpoint = toggle?.dataset.themeEndpoint;
    const savedTheme = localStorage.getItem("taskflow-theme");

    if (lockedTheme) {
        root.setAttribute("data-theme", lockedTheme);
        return;
    }

    if (savedTheme) {
        root.setAttribute("data-theme", savedTheme);
    }

    if (toggle) {
        toggle.addEventListener("click", async () => {
            const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
            root.setAttribute("data-theme", nextTheme);
            localStorage.setItem("taskflow-theme", nextTheme);
            window.dispatchEvent(new CustomEvent("taskflow:theme-change", { detail: { theme: nextTheme } }));
            if (endpoint) {
                await fetch(endpoint, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": document.cookie.split("csrftoken=")[1]?.split(";")[0] || "",
                    },
                    body: new URLSearchParams({ theme: nextTheme }),
                });
            }
        });
    }
});
