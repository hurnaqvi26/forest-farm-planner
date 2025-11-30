console.log("planner.js loaded!");

let plots = [];

// ADD PLOT
document.getElementById("addPlot").addEventListener("click", () => {
    const plotId = document.getElementById("plotId").value;
    const area = document.getElementById("area").value;
    const soil = document.getElementById("soilType").value;
    const crop = document.getElementById("currentCrop").value;

    if (!plotId || !area || !soil) {
        alert("Please fill all required fields");
        return;
    }

    plots.push({
        plotId: plotId,
        area: parseFloat(area),
        soil: soil,
        crop: crop || "",
        date: new Date().toISOString()
    });

    updateTable();

    // reset
    document.getElementById("plotId").value = "";
    document.getElementById("area").value = "";
    document.getElementById("currentCrop").value = "";
});

// UPDATE TABLE
function updateTable() {
    const tbody = document.querySelector("#plotTable tbody");
    tbody.innerHTML = "";

    plots.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.plotId}</td>
                <td>${p.area}</td>
                <td>${p.soil}</td>
                <td>${p.crop}</td>
                <td>${new Date(p.date).toLocaleString()}</td>
            </tr>
        `;
    });
}

// SUBMIT FOR GENERATION
document.getElementById("generatePlan").addEventListener("click", () => {
    if (plots.length === 0) {
        alert("Add at least one plot!");
        return;
    }

    document.getElementById("plots_json").value = JSON.stringify(plots);
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
