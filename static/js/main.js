function getCsrfToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; csrftoken=`);
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
    return "";
}

document.addEventListener("DOMContentLoaded", () => {
    const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
    const sidebar = document.getElementById("sidebar");
    const sidebarClose = document.querySelector("[data-sidebar-close]");

    const setSidebarState = (isOpen) => {
        if (!sidebar || !sidebarToggle) {
            return;
        }
        sidebar.classList.toggle("is-open", isOpen);
        document.body.classList.toggle("has-open-sidebar", isOpen);
        sidebarToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    };

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", () => {
            setSidebarState(!sidebar.classList.contains("is-open"));
        });
    }

    if (sidebarClose) {
        sidebarClose.addEventListener("click", () => setSidebarState(false));
    }

    const landingMenuToggle = document.querySelector("[data-landing-menu-toggle]");
    const landingMobileMenu = document.getElementById("landingMobileMenu");
    if (landingMenuToggle && landingMobileMenu) {
        landingMenuToggle.addEventListener("click", () => {
            const isOpen = landingMobileMenu.classList.toggle("is-open");
            landingMenuToggle.classList.toggle("is-open", isOpen);
            landingMenuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        });

        landingMobileMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                landingMobileMenu.classList.remove("is-open");
                landingMenuToggle.classList.remove("is-open");
                landingMenuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            setSidebarState(false);
            if (landingMobileMenu && landingMenuToggle) {
                landingMobileMenu.classList.remove("is-open");
                landingMenuToggle.classList.remove("is-open");
                landingMenuToggle.setAttribute("aria-expanded", "false");
            }
        }
    });

    document.querySelectorAll("form[data-submit-state]").forEach((form) => {
        form.addEventListener("submit", () => {
            const button = form.querySelector("[data-submit-button]");
            if (!button || button.disabled) {
                return;
            }
            const label = button.dataset.loadingLabel || `${button.textContent.trim()}...`;
            button.dataset.originalLabel = button.innerHTML;
            button.innerHTML = `<span class="btn-loading" aria-hidden="true"></span>${label}`;
            button.disabled = true;
            form.classList.add("is-submitting");
        });
    });

    document.querySelectorAll("form[data-language-switch]").forEach((form) => {
        const select = form.querySelector('select[name="language"]');
        const nextInput = form.querySelector("[data-language-next]");
        if (!select || !nextInput) {
            return;
        }
        form.addEventListener("submit", () => {
            const target = select.value === "ru" ? form.dataset.nextRu : form.dataset.nextEn;
            if (target) {
                nextInput.value = target;
            }
        });
    });

    document.querySelectorAll(".checklist-toggle").forEach((input) => {
        input.addEventListener("change", async () => {
            await fetch(input.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
        });
    });

    const markAllButton = document.querySelector("[data-mark-all-read]");
    if (markAllButton) {
        markAllButton.addEventListener("click", async () => {
            const response = await fetch(markAllButton.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
            if (response.ok) {
                window.location.reload();
            }
        });
    }

    document.querySelectorAll("[data-password-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const wrapper = button.closest(".auth-password");
            const input = wrapper?.querySelector("input");
            if (!input) {
                return;
            }
            const reveal = input.type === "password";
            input.type = reveal ? "text" : "password";
            button.classList.toggle("is-active", reveal);
        });
    });
});
