var mvtCtx = document.getElementById('marketValueTrend').getContext('2d');
var trendConfig = {
    type: 'line',
    data: {
        labels: trendDates,
        datasets: [{
            label: 'Market Value',
            data: trendValues,
            borderColor: '#4682B4',
            fill: true,
        }]
    }
};


allocCtx = document.getElementById('allocationSummary').getContext('2d');
allocConfig = {
    type: 'doughnut',
    data: {
        labels: allocationLabels,
        datasets: [
            {
                label: "Portfolio Allocation",
                backgroundColor: [
                    "rgba(255, 99, 132, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(75, 192, 192, 1)",
                    "#e8c3b9",
                ],
                data: allocationValues,
            }
        ],
    },
};

new Chart(mvtCtx, trendConfig);
new Chart(allocCtx, allocConfig);

