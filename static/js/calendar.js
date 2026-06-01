document.addEventListener("DOMContentLoaded", () => {
    const calendarRoot = document.getElementById("calendarApp");
    if (!calendarRoot) {
        return;
    }
    const events = JSON.parse(calendarRoot.dataset.events || "[]");
    const emptyText = calendarRoot.dataset.emptyText || "No data";
    const weekText = calendarRoot.dataset.weekText || "Week";
    const dayText = calendarRoot.dataset.dayText || "Day";
    const addTaskText = calendarRoot.dataset.addTaskText || "Add task";
    const createTaskUrl = calendarRoot.dataset.createTaskUrl || "/tasks/create/";
    const weekdays = JSON.parse(calendarRoot.dataset.weekdays || '["Mo","Tu","We","Th","Fr","Sa","Su"]');
    const grouped = events.reduce((acc, event) => {
        acc[event.date] = acc[event.date] || [];
        acc[event.date].push(event);
        return acc;
    }, {});
    const viewButtons = document.querySelectorAll(".calendar-view-btn");

    const month = Number(calendarRoot.dataset.month) - 1;
    const year = Number(calendarRoot.dataset.year);
    const selectedDate = new Date();

    function createTaskLink(dateKey) {
        const link = document.createElement("a");
        link.className = "calendar-add-link";
        link.href = `${createTaskUrl}?date=${dateKey}`;
        link.textContent = addTaskText;
        return link;
    }

    function appendEvents(container, dateKey) {
        const eventsForDay = grouped[dateKey] || [];
        const eventList = document.createElement("div");
        eventList.className = "calendar-events";
        eventsForDay.slice(0, 3).forEach((event) => {
            const link = document.createElement("a");
            link.href = event.url;
            link.className = `calendar-event calendar-event--${event.status || "default"}`;
            link.textContent = event.title;
            eventList.appendChild(link);
        });
        if (eventsForDay.length > 3) {
            const more = document.createElement("span");
            more.className = "calendar-more";
            more.textContent = `+${eventsForDay.length - 3}`;
            eventList.appendChild(more);
        }
        container.appendChild(eventList);
    }

    function createDateCard(dateKey, label, options = {}) {
        const item = document.createElement("div");
        item.className = "calendar-day";
        if (options.isCompact) {
            item.classList.add("calendar-day--compact");
        }
        const header = document.createElement("div");
        header.className = "calendar-day__head";
        const dateLabel = document.createElement("strong");
        dateLabel.className = "calendar-day__date";
        dateLabel.textContent = label;
        header.appendChild(dateLabel);
        header.appendChild(createTaskLink(dateKey));
        item.appendChild(header);
        appendEvents(item, dateKey);
        return item;
    }

    function renderMonth() {
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startOffset = (firstDay.getDay() + 6) % 7;
        const totalCells = Math.ceil((startOffset + lastDay.getDate()) / 7) * 7;
        const grid = document.createElement("div");
        grid.className = "calendar-grid";
        weekdays.forEach((label) => {
            const item = document.createElement("div");
            item.className = "calendar-weekday";
            item.textContent = label;
            grid.appendChild(item);
        });
        for (let cell = 0; cell < totalCells; cell += 1) {
            const dayNumber = cell - startOffset + 1;
            if (dayNumber > 0 && dayNumber <= lastDay.getDate()) {
                const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(dayNumber).padStart(2, "0")}`;
                grid.appendChild(createDateCard(dateKey, dayNumber));
            } else {
                const item = document.createElement("div");
                item.className = "calendar-day calendar-day--empty";
                grid.appendChild(item);
            }
        }
        return grid;
    }

    function renderList(title, dateKeys) {
        const wrapper = document.createElement("div");
        wrapper.className = "calendar-list-view";
        wrapper.innerHTML = `<h3>${title}</h3>`;
        if (!dateKeys.length) {
            wrapper.innerHTML += `<div class='empty-state'>${emptyText}</div>`;
            return wrapper;
        }
        dateKeys.forEach((dateKey) => {
            wrapper.appendChild(createDateCard(dateKey, dateKey, { isCompact: true }));
        });
        return wrapper;
    }

    function renderWeek() {
        const today = new Date(selectedDate);
        const monday = new Date(today);
        monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
        const keys = [];
        for (let i = 0; i < 7; i += 1) {
            const current = new Date(monday);
            current.setDate(monday.getDate() + i);
            keys.push(`${current.getFullYear()}-${String(current.getMonth() + 1).padStart(2, "0")}-${String(current.getDate()).padStart(2, "0")}`);
        }
        return renderList(weekText, keys);
    }

    function renderDay() {
        const key = `${selectedDate.getFullYear()}-${String(selectedDate.getMonth() + 1).padStart(2, "0")}-${String(selectedDate.getDate()).padStart(2, "0")}`;
        return renderList(dayText, [key]);
    }

    function mount(view) {
        calendarRoot.innerHTML = "";
        if (view === "week") {
            calendarRoot.appendChild(renderWeek());
        } else if (view === "day") {
            calendarRoot.appendChild(renderDay());
        } else {
            calendarRoot.appendChild(renderMonth());
        }
    }

    mount("month");
    viewButtons.forEach((button) => {
        button.addEventListener("click", () => mount(button.dataset.view));
    });
});
