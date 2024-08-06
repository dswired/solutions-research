// document.addEventListener('DOMContentLoaded', () => {

const selectElement = document.getElementById('mySelect');
const endPoint = '/equities/get_dropdown_data';
const graphendPoint = '/equities/equity_trend';
const toogleendPoint = '/equities/trend_view_toggle';
const chartElementId = 'equityPriceTrend';
const dateInputElement = document.getElementById('asOfDate'); 
const ticker_tag = 'equityticker';
const date_tag = 'asOfDate';
const trendToggleElement = document.getElementById('trendSelect');
const trend_type_tag = 'trendtoggle';


async function equityAjaxEngine(
    selectElement, 
    endPoint, 
    trendToggleElement,
    graphendPoint,
    toogleendPoint,
    chartElementId,
    dateInputElement,
    // tag_name
) {
    console.log("Fetching data from", endPoint);

    try {
        const response = await fetch(endPoint);
        const optionsData = await response.json();
        const tickerData = optionsData.unique_tickers;

        const toogle_response = await fetch(toogleendPoint);
        const toogleData = await toogle_response.json();
        const trendTypeData = toogleData.trend_toggle;

        const chartendPoint = graphendPoint;

        console.log("Ticker data", tickerData);
        console.log("Trend data", trendTypeData);

        // Use the fetched data to create options
        tickerData.forEach(optionText => {
            const option = document.createElement('option');
            option.text = optionText;
            option.value = optionText.toLowerCase();  // Adjust value setting as needed
            selectElement.appendChild(option);
        });

        trendTypeData.forEach(optionText => {
            const option = document.createElement('option');
            option.text = optionText;
            option.value = optionText.toLowerCase();  // Adjust value setting as needed
            trendToggleElement.appendChild(option);
        });

        const updateData = () => {
            const selectedTicker = selectElement.value;
            const selectedDate = dateInputElement.value;
            const selectedtrendType = trendToggleElement.value;
            if (selectedTicker) {
                loadChart(
                    selectedTicker, 
                    chartendPoint, 
                    chartElementId, 
                    selectedDate,
                    ticker_tag,
                    date_tag,
                    selectedtrendType,
                    trend_type_tag,
                );
                updateSummaryCard(
                    selectedTicker, 
                    selectedDate,
                );
            }
        };


        selectElement.addEventListener('change', updateData);
        dateInputElement.addEventListener('change', updateData);
        trendToggleElement.addEventListener('change', updateData);

        //trigger initial data load
        if (selectElement.options.length > 0) {
            selectElement.value = selectElement.options[0].value;
            if (!dateInputElement.value) {
                dateInputElement.value = '2020-01-02';
            }
            if (trendToggleElement.options.length > 0) {
                trendToggleElement.value = trendToggleElement.options[0].value;  // Set default to the first option
                        }
            updateData();
        }

    } catch (error) {
        console.log("Error fetching data:", error);
        // Handle errors gracefully (e.g., display an error message to the user)
    }
}



equityAjaxEngine(
    selectElement, 
    endPoint, 
    trendToggleElement,
    graphendPoint, 
    toogleendPoint,
    chartElementId,
    dateInputElement,
    // tag_name
);


// });