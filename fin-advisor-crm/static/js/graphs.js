let chart = null;
function loadChart(
    selectedTicker, 
    chartendPoint, 
    chartElementId,
    selectedDate,
    ticker_tag,
    date_tag,
    ) 
    {
    const endPoint = chartendPoint;
    console.log("Fetching data from "+ endPoint);
    console.log("Selected ticker "+ selectedTicker + "for date" + selectedDate);

    const payload = {
        // 'equityticker' : selectedTicker,
        [ticker_tag] : selectedTicker,
        [date_tag] : selectedDate
    }

    fetch(endPoint, {
        method: "POST",
        body: JSON.stringify(payload),
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