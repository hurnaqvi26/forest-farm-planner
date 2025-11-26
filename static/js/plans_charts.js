// ============================
// Crop Distribution Pie Chart
// ============================

new Chart(document.getElementById("cropChart"), {
    type: "pie",
    data: {
        labels: analytics.crop_labels,
        datasets: [{
            data: analytics.crop_values,
            backgroundColor: [
                "#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107",
                "#FF9800", "#FF5722", "#9C27B0", "#3F51B5", "#03A9F4"
            ]
        }]
    }
});


// ============================
// Area Per Crop (Bar Chart)
// ============================

new Chart(document.getElementById("areaChart"), {
    type: "bar",
    data: {
        labels: analytics.area_labels,
        datasets: [{
            label: "Acres",
            data: analytics.area_values,
            backgroundColor: "#4CAF50"
        }]
    },
});


// ============================
// Plans Over Time (Line Chart)
// ============================

new Chart(document.getElementById("dateChart"), {
    type: "line",
    data: {
        labels: analytics.date_labels,
        datasets: [{
            label: "Plans Created",
            data: analytics.date_values,
            borderColor: "#4CAF50",
            borderWidth: 2
        }]
    }
});
