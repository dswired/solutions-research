// document.addEventListener('DOMContentLoaded', () => {

const selectElement = document.getElementById('mySelect');
const endPoint = '/equities/get_dropdown_data';
const graphendPoint = '/equities/equity_trend';
const chartElementId = 'equityPriceTrend';
const dateInputElement = document.getElementById('asOfDate'); 
const tag_name = 'equityticker';


async function equityAjaxEngine(
    selectElement, 
    endPoint, 
    graphendPoint,
    chartElementId,
    dateInputElement,
    // tag_name
) {
    console.log("Fetching data from", endPoint);

    try {
        const response = await fetch(endPoint);
        const optionsData = await response.json();
        const tickerData = optionsData.unique_tickers;
        const chartendPoint = graphendPoint;

        console.log(tickerData);

        // Use the fetched data to create options
        tickerData.forEach(optionText => {
            const option = document.createElement('option');
            option.text = optionText;
            option.value = optionText.toLowerCase();  // Adjust value setting as needed
            selectElement.appendChild(option);
        });

        const updateData = () => {
            const selectedTicker = selectElement.value;
            const selectedDate = dateInputElement.value;
            if (selectedTicker) {
                loadChart(
                    selectedTicker, 
                    chartendPoint, 
                    chartElementId, 
                    selectedDate
                );
                updateSummaryCard(
                    selectedTicker, 
                    selectedDate
                );
            }
        };


        selectElement.addEventListener('change', updateData);
        dateInputElement.addEventListener('change', updateData);

        //trigger initial data load
        if (selectElement.options.length > 0) {
            selectElement.value = selectElement.options[0].value;
            if (!dateInputElement.value) {
                dateInputElement.value = '2020-01-02';
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
    graphendPoint, 
    chartElementId,
    dateInputElement,
    // tag_name
);


// });