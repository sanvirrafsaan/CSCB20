document.addEventListener("DOMContentLoaded", () => {
    const mode = document.body.dataset.mode;

    if (mode === "vote") {
        setupVoteMode();
    } else if (mode === "view") {
        setupViewMode();
    }
});

function setupVoteMode() {
    const cells = document.querySelectorAll(".slot-cell.clickable");
    const slotsInput = document.getElementById("slots-input");
    const resetBtn = document.getElementById("reset-btn");

    const selected = new Set();

    function updateHiddenInput() {
        slotsInput.value = Array.from(selected).join(",");
    }

    cells.forEach(cell => {
        cell.addEventListener("click", () => {
            const day = cell.dataset.day;
            const hour = cell.dataset.hour;
            const key = `${day}-${hour}`;

            if (selected.has(key)) {
                selected.delete(key);
                cell.classList.remove("selected");
                cell.textContent = "";
            } else {
                selected.add(key);
                cell.classList.add("selected");
                cell.textContent = "✓";
            }

            updateHiddenInput();
        });
    });

    resetBtn.addEventListener("click", () => {
        selected.clear();
        cells.forEach(cell => {
            cell.classList.remove("selected");
            cell.textContent = "";
        });
        updateHiddenInput();
    });
}

function setupViewMode() {
    const tooltip = document.getElementById("tooltip");
    const cells = document.querySelectorAll(".view-table .slot-cell");

    cells.forEach(cell => {
        cell.addEventListener("mouseenter", (event) => {
            const count = cell.dataset.count || "0";
            if (count === "0") return;

            const voters = cell.dataset.voters || "";
            const day = cell.dataset.day;
            const hour = cell.dataset.hour;

            let text = `<strong>${day} ${hour}:00 - ${Number(hour) + 1}:00</strong><br>`;
            text += `Votes: ${count}<br>`;
            text += voters ? `Users: ${voters}` : "Users: none";

            tooltip.innerHTML = text;
            tooltip.classList.remove("hidden");

            positionTooltip(event, tooltip);
        });

        cell.addEventListener("mousemove", (event) => {
            positionTooltip(event, tooltip);
        });

        cell.addEventListener("mouseleave", () => {
            tooltip.classList.add("hidden");
        });
    });
}

function positionTooltip(event, tooltip) {
    tooltip.style.left = `${event.pageX + 12}px`;
    tooltip.style.top = `${event.pageY + 12}px`;
}