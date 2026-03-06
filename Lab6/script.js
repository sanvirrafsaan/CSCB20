const container_id = document.getElementById("container");
const button_flex = document.getElementById("button-flex");
const button_grid = document.getElementById("button-grid");

function switchtoFlex() {
    container_id.classList.add("layout-flex");
    container_id.classList.remove("layout-grid");
    button_flex.disabled = true;
    button_grid.disabled = false;
}

function switchtoGrid() {
    container_id.classList.add("layout-grid");
    container_id.classList.remove("layout-flex");
    button_flex.disabled = false;
    button_grid.disabled = true;


}

button_flex.addEventListener("click", switchtoFlex);
button_grid.addEventListener("click", switchtoGrid);