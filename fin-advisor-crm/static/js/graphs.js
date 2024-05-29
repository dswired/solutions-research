function loadChart(elementId, endPoint) {
    console.log("Fetching data from "+ endPoint);
    fetch(endPoint)
        .then((response) => response.json())
        .then((config) => {
            console.log("results", config)
            ctx = document.getElementById(elementId)
            new Chart(ctx, config)
        })
}

loadChart('marketValueTrend', '/main/entity_trend')
loadChart('allocationSummary','/main/entity_allocation')
