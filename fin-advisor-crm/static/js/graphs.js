let chart = null;
function loadChart(
    selectedTicker, 
    chartendPoint, 
    chartElementId,
    selectedDate,
    ticker_tag,
    date_tag,
    selectedtrendType,
    trend_type_tag
    ) 
    {
    const endPoint = chartendPoint;
    console.log("Fetching data from "+ endPoint);
    console.log("Selected ticker "+ selectedTicker + "for date " + selectedDate + "for metric " + selectedtrendType);

    const payload = {
        [ticker_tag] : selectedTicker,
        [date_tag] : selectedDate,
        [trend_type_tag] : selectedtrendType
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