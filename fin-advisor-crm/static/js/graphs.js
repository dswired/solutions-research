const defaultGraphColor = "#4682B4"

new Chart(document.getElementById("marketValueTrend"), {
    type: 'line',
    data: {
        labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
        datasets: [
            { 
                data: [282,350,411,502,635,809,947,1402,3700,5267],
                label: "Market Value",
                borderColor: defaultGraphColor,
                fill: true
            }
        ]
    }
});

new Chart(document.getElementById("allocationSummary"), {
    type: 'doughnut',
    data: {
        labels: ["Alternatives", "Equities", "Fixed Income", "Other"],
        datasets: 
        [
            {
                label: "Portfolio Allocation",
                backgroundColor: [
                    "rgba(255, 99, 132, 0.5)",
                    "rgba(54, 162, 235, 0.5)",
                    "rgba(75, 192, 192, 0.5)",
                    "#e8c3b9"
                ],
                data: [1200,4500,2970,616]
            }
        ]
    }
});