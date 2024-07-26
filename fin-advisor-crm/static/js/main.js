function updateSummaryCard(selectedTicker, selectedDate) {
    const endPoint = '/equities/get_summary_card_info';
    console.log("Fetching data from " + endPoint);
    console.log("Selected ticker within updateSummaryCard " + selectedTicker);
    fetch(endPoint, {
        method: "POST",
        body: JSON.stringify(
            { 
                'equityticker': selectedTicker,
                'asOfDate' : selectedDate
            }
            ),
        headers: { 'Content-Type': 'application/json' }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error) {
            console.error("Error fetching summary card data:", data.error);
            // Display error to user
            return;
        }
        console.log("Summary card data:", data);
        // Update the summary card elements on the HTML page
        document.getElementById('marketValue').textContent = data.market_value;
        document.getElementById('closingPrice').textContent = data.closing_price;
        document.getElementById('priceChange').textContent = data.price_change;
        document.getElementById('volume').textContent = data.volume;
        document.getElementById('tickerCommentary').textContent = data.tickerCommentary;
        document.getElementById('trendCommentary').textContent = data.trendCommentary;
    })
    .catch((error) => {
        console.error("Error fetching summary card data:", error);
        // Handle error gracefully (e.g., display an error message to the user)
    });
}


const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("collapsed");
});


const navLinkEls = document.querySelectorAll('.sidebar-link');
navLinkEls.forEach(navLinkEl => {
    navLinkEl.addEventListener('click', () => {
        document.querySelector('.activated')?.classList.remove('activated');
        navLinkEl.classList.add('activated');
    });
});


// const asOfDate = document.querySelector('#AsOfDate');
// asOfDate.addEventListener("change", function () {
//     document.querySelector('#AsOfDateInputForm').submit();
// });