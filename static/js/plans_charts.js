// ================================
// GLOBAL CHART STYLE (applies to all charts)
// ================================
Chart.defaults.font.family = "Poppins, Arial, sans-serif";
Chart.defaults.font.size = 14;
Chart.defaults.color = "#444";
Chart.defaults.plugins.legend.labels.boxWidth = 20;


// ================================
// GRADIENT GENERATOR
// ================================
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}


// ================================
// 1️⃣ CROP DISTRIBUTION – PIE CHART
// ================================
(() => {
    const ctx = document.getElementById("cropChart");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: analytics.crop_labels,
            datasets: [{
                data: analytics.crop_values,
                backgroundColor: [
                    "#4CAF50", "#66BB6A", "#81C784", "#A5D6A7",
                    "#FFB74D", "#FFD54F", "#FF8A65", "#E57373",
                    "#7986CB", "#64B5F6"
                ],
                borderColor: "#fff",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Crop Distribution",
                    font: { size: 20, weight: "bold" }
                }
            }
        }
    });
})();


// ================================
// 2️⃣ AREA PER CROP – BAR CHART
// ================================
(() => {
    const ctx = document.getElementById("areaChart").getContext("2d");

    const gradient = createGradient(ctx, "#4CAF50", "#A5D6A7");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: analytics.area_labels,
            datasets: [{
                label: "Acres",
                data: analytics.area_values,
                backgroundColor: gradient,
                borderColor: "#2E7D32",
                borderWidth: 0,
                borderRadius: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Area per Crop (Acres)",
                    font: { size: 20, weight: "bold" }
                }
            },
            scales: {
                y: {
                    grid: { color: "#e0e0e0" },
                    ticks: { beginAtZero: true }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
})();


// ================================
// 3️⃣ PLANS OVER TIME – LINE CHART
// ================================
(() => {
    const ctx = document.getElementById("dateChart").getContext("2d");

    const gradient = createGradient(ctx, "rgba(76, 175, 80, 0.5)", "rgba(165, 214, 167, 0)");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: analytics.date_labels,
            datasets: [{
                label: "Plans Created",
                data: analytics.date_values,
                fill: true,
                backgroundColor: gradient,
                borderColor: "#4CAF50",
                borderWidth: 3,
                pointBackgroundColor: "#2E7D32",
                pointRadius: 5,
                tension: 0.4   // smooth curved line
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Plans Created Over Time",
                    font: { size: 20, weight: "bold" }
                }
            },
            scales: {
                y: { grid: { color: "#ddd" } },
                x: {
                    grid: { display: false },
                    ticks: { autoSkip: true, maxTicksLimit: 10 }
                }
            }
        }
    });
})();
