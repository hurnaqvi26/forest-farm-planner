document.addEventListener("DOMContentLoaded", () => {
    console.log("planner.js LOADED ✅");

    let plots = [];

    const plotIdInput = document.getElementById("plotId");
    const areaInput = document.getElementById("area");
    const soilSelect = document.getElementById("soilType");
    const cropInput = document.getElementById("currentCrop");

    const addPlotBtn = document.getElementById("addPlot");
    const generatePlanBtn = document.getElementById("generatePlan");

    const plotsJsonInput = document.getElementById("plots_json");
    const plannerForm = document.getElementById("plannerForm");
    const tableBody = document.querySelector("#plotTable tbody");
    const noPlotsMsg = document.getElementById("noPlotsMsg");

    const plotCountSpan = document.getElementById("plotCount");
    const metricTotalPlots = document.getElementById("metricTotalPlots");
    const metricTotalArea = document.getElementById("metricTotalArea");
    const metricUniqueCrops = document.getElementById("metricUniqueCrops");

    // Add plot
    addPlotBtn.addEventListener("click", () => {
        const id = (plotIdInput.value || "").trim();
        const area = (areaInput.value || "").trim();
        const soil = soilSelect.value;
        const crop = (cropInput.value || "").trim();

        if (!id || !area) {
            alert("Plot ID and Area are required.");
            return;
        }

        plots.push({
            plotId: id,
            area: area,
            soil: soil,
            crop: crop
        });

        plotIdInput.value = "";
        areaInput.value = "";
        cropInput.value = "";

        renderTable();
        updateMetrics();
    });

    function renderTable() {
        tableBody.innerHTML = "";

        plots.forEach((p, index) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${p.plotId}</td>
                <td>${p.area}</td>
                <td>${p.soil}</td>
                <td>${p.crop || "-"}</td>
                <td style="text-align:right;">
                    <button type="button" class="btn btn-outline btn-sm remove-btn" data-index="${index}">
                        ✕
                    </button>
                </td>
            `;

            tableBody.appendChild(row);
        });

        // Remove handlers
        document.querySelectorAll(".remove-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const idx = parseInt(e.target.getAttribute("data-index"));
                plots.splice(idx, 1);
                renderTable();
                updateMetrics();
            });
        });

        if (plots.length === 0) {
            noPlotsMsg.style.display = "block";
        } else {
            noPlotsMsg.style.display = "none";
        }

        plotCountSpan.textContent = plots.length.toString();
    }

    function updateMetrics() {
        // total plots
        metricTotalPlots.textContent = plots.length.toString();

        // total area
        let totalArea = 0;
        plots.forEach(p => {
            const n = parseFloat(p.area);
            if (!isNaN(n)) totalArea += n;
        });
        metricTotalArea.textContent = totalArea.toString();

        // unique crops
        const crops = new Set();
        plots.forEach(p => {
            if (p.crop && p.crop.trim() !== "") {
                crops.add(p.crop.trim().toLowerCase());
            }
        });
        metricUniqueCrops.textContent = crops.size.toString();
    }

    // Generate plan → submit form
    generatePlanBtn.addEventListener("click", () => {
        if (plots.length === 0) {
            alert("Please add at least one plot before generating a plan.");
            return;
        }

        plotsJsonInput.value = JSON.stringify(plots);
        plannerForm.submit();
    });
});
