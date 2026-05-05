document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const lockedTheme = document.body?.dataset.lockTheme;
    const toggle = document.querySelector("[data-theme-toggle]");
    const endpoint = toggle?.dataset.themeEndpoint;
    const savedTheme = localStorage.getItem("taskflow-theme");
    const csrfToken = document.cookie.split("csrftoken=")[1]?.split(";")[0] || "";

    function applyTheme(theme) {
        root.setAttribute("data-theme", theme);
        localStorage.setItem("taskflow-theme", theme);
        if (toggle) {
            toggle.setAttribute("aria-pressed", String(theme === "dark"));
            toggle.setAttribute("title", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
        }
        window.dispatchEvent(new CustomEvent("taskflow:themechange", { detail: { theme } }));
    }

    if (lockedTheme) {
        applyTheme(lockedTheme);
        return;
    }

    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        applyTheme(root.getAttribute("data-theme") || "light");
    }

    if (toggle) {
        toggle.addEventListener("click", async () => {
            const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
            if (endpoint) {
                try {
                    await fetch(endpoint, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": csrfToken,
                        },
                        body: new URLSearchParams({ theme: nextTheme }),
                    });
                } catch (error) {
                    console.error("Theme sync failed", error);
                }
            }
        });
    }
});
