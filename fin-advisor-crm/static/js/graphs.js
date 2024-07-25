let chart = null;
function loadChart(
    selectedTicker, 
    chartendPoint, 
    chartElementId,
    selectedDate
    // tag_name
    ) 
    {
    const endPoint = chartendPoint
    console.log("Fetching data from "+ endPoint);
    console.log("Selected ticker "+ selectedTicker + "for date" + selectedDate);
    fetch(endPoint, {
        method: "POST",
        body: JSON.stringify(
            {
                'equityticker' : selectedTicker,
                'asOfDate' : selectedDate
            }
        ),
        headers: { 'Content-Type': 'application/json' }        
    })
        .then((response) => response.json())
        .then((config) => {
            console.log("results", config)
            const ctx = document.getElementById(chartElementId);

            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, config)
        })
}