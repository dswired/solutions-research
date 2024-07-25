function generateUpdatedGraph() {
    console.log("Running generateUpdatedGraph!")
    const formEl = document.getElementById('AsOfDateInputForm');
    formEl.submit()
    const formData = new FormData(formEl);
    const data = new URLSearchParams(formData);

    fetch('/main/entity_trend', {
        method: 'POST',
        body: data
    })
    .then(res => res.json())
    .then(config => {
        console.log('generateUpdatedGraph(POST)', config)
        let chartStatus = Chart.getChart('marketValueTrend');
        if (chartStatus != undefined) {
            chartStatus.destroy();
        };
        ctx = document.getElementById('marketValueTrend')
        new Chart(ctx, config)
    })
    .catch(error => console.log(error));

};


function loadChart(elementId, endPoint) {
    console.log("Fetching data from "+ endPoint);
    fetch(endPoint)
        .then((response) => response.json())
        .then((config) => {
            console.log("loadChart(GET)", config)
            ctx = document.getElementById(elementId)
            new Chart(ctx, config)
        })
        .catch((error) => {
            console.error("Error:", error);
        })
};

// loadChart('marketValueTrend', '/main/entity_trend')
// loadChart('allocationSummary', '/main/entity_allocation')
// loadChart('equityPriceTrend', '/equities/equity_trend')