console.log("planner.js loaded!");

let plots = [];

// ADD PLOT
document.getElementById("addPlot").addEventListener("click", function () {
    const plotId = document.getElementById("plotId").value;
    const area = document.getElementById("area").value;
    const soil = document.getElementById("soilType").value;
    const crop = document.getElementById("currentCrop").value;

    if (!plotId || !area) {
        alert("Please fill all required fields");
        return;
    }

    plots.push({ plotId, area, soil, crop });

    updateTable();
    updateAnalytics();
});

// UPDATE TABLE
function updateTable() {
    const tbody = document.querySelector("#plotTable tbody");
    tbody.innerHTML = "";

    plots.forEach((p, idx) => {
        tbody.innerHTML += `
            <tr>
                <td>${idx + 1}</td>
                <td>${p.plotId}</td>
                <td>${p.area}</td>
                <td>${p.soil}</td>
                <td>${p.crop}</td>
            </tr>`;
    });

    document.getElementById("plotCount").innerText = plots.length;
    document.getElementById("noPlotsMsg").style.display =
        plots.length === 0 ? "block" : "none";
}

// QUICK ANALYTICS
function updateAnalytics() {
    document.getElementById("metricTotalPlots").innerText = plots.length;

    const totalArea = plots.reduce((sum, p) => sum + parseFloat(p.area), 0);
    document.getElementById("metricTotalArea").innerText = totalArea.toFixed(1);

    const uniqueCrops = new Set(plots.map(p => (p.crop || "").toLowerCase()));
    document.getElementById("metricUniqueCrops").innerText = uniqueCrops.size;
}

// SAVE PLAN
document.getElementById("generatePlan").addEventListener("click", function () {
    if (plots.length === 0) {
        alert("Add at least one plot!");
        return;
    }

    document.getElementById("plots_json").value = JSON.stringify(plots);
    document.getElementById("plannerForm").action = "/dashboard/";
    document.getElementById("plannerForm").submit();
});

// EXPORT PDF
document.getElementById("exportPDF").addEventListener("click", function () {
    if (plots.length === 0) {
        alert("Add at least one plot before exporting PDF!");
        return;
    }

    document.getElementById("plots_json").value = JSON.stringify(plots);

    const form = document.getElementById("plannerForm");
    form.action = "/export-pdf/";
    form.submit();
});