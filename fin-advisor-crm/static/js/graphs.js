function loadChart(elementId, endPoint) {
    console.log("Fetching data from "+ endPoint);
    fetch(endPoint)
        .then((response) => response.json())
        .then((config) => {
            console.log("results", config)
            ctx = document.getElementById(elementId)
            new Chart(ctx, config)
        })
        .catch((error) => {
            console.error("Error:", error);
        })
}

loadChart('marketValueTrend', '/main/entity_trend')
loadChart('allocationSummary', '/main/entity_allocation')
loadChart('equityPriceTrend', '/equities/equity_trend')

var dateform = document.getElementById('AsOfDateInputForm')
dateform.addEventListener('submit', function(e){
    // prevent autosubmit
    e.preventDefault();

    var asOf = document.getElementById('AsOfDate').value;
    fetch('/main/entity_trend', {
        method: 'POST',
        body: JSON.stringify({
            title: 'AsOf',
            body: asOf,
            id:id
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        }
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data);
    })
})