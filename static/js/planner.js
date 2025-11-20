console.log("planner.js loaded");

let plots = [];

// ----------------------------
// ADD PLOT
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
    const addBtn = document.getElementById("addPlot");
    const genBtn = document.getElementById("generatePlan");

    addBtn.addEventListener("click", () => {
        const plotId = document.getElementById("plotId").value.trim();
        const area = document.getElementById("area").value.trim();
        const soil = document.getElementById("soilType").value.trim();
        const crop = document.getElementById("currentCrop").value.trim();

        if (!plotId || !area || !soil) {
            alert("Plot ID, Area, and Soil are required!");
            return;
        }

        plots.push({ plotId, area: Number(area), soil, crop });

        renderTable();
        updateCharts();

        document.getElementById("plotId").value = "";
        document.getElementById("area").value = "";
        document.getElementById("currentCrop").value = "";
    });

    genBtn.addEventListener("click", () => {
        if (plots.length === 0) {
            alert("Add at least one plot first!");
            return;
        }

        document.getElementById("plots_json").value = JSON.stringify(plots);
        document.getElementById("plannerForm").submit();
    });
});

function renderTable() {
    const tbody = document.getElementById("plotTable");
    tbody.innerHTML = "";

    plots.forEach((p, i) => {
        tbody.innerHTML += `
            <tr>
                <td>${i + 1}</td>
                <td>${p.plotId}</td>
                <td>${p.area}</td>
                <td>${p.soil}</td>
                <td>${p.crop || "-"}</td>
            </tr>
        `;
    });
}


// ----------------------------
// CHARTS
// ----------------------------
let cropChart, soilChart, areaChart;

function updateCharts() {
    const cropCounts = {};
    const soilCounts = {};
    let totalArea = 0;

    plots.forEach(p => {
        cropCounts[p.crop || "Unknown"] = (cropCounts[p.crop || "Unknown"] || 0) + 1;
        soilCounts[p.soil] = (soilCounts[p.soil] || 0) + 1;
        totalArea += p.area;
    });

    if (cropChart) cropChart.destroy();
    if (soilChart) soilChart.destroy();
    if (areaChart) areaChart.destroy();

    const cropCtx = document.getElementById("cropChart");
    const soilCtx = document.getElementById("soilChart");
    const areaCtx = document.getElementById("areaChart");

    cropChart = new Chart(cropCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(cropCounts),
            datasets: [{
                data: Object.values(cropCounts),
                backgroundColor: ['#8eff9e', '#6fe88c', '#5dd47a', '#4ac060']
            }]
        }
    });

    soilChart = new Chart(soilCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(soilCounts),
            datasets: [{
                label: 'Soil Types',
                data: Object.values(soilCounts),
                backgroundColor: '#7ee27a'
            }]
        }
    });

    areaChart = new Chart(areaCtx, {
        type: 'doughnut',
        data: {
            labels: ["Total Area (acres)"],
            datasets: [{
                data: [totalArea],
                backgroundColor: ['#72db68']
            }]
        }
    });
}
