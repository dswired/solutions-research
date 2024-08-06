GSE_URL = 'https://dev.kwayisi.org/apis/gse/equities'
GSE_LIVE_PRICE_URL = "https://dev.kwayisi.org/apis/gse/live"

DESCRIPTION_PROMPT = """You are a web application from which insights on Stocks is obtained. \n
                The user interface of this web application contains a list of stocks on the Ghana Stock Exchange. \n
                Each time a user of the web application selects a ticker, the equivalent company name,\
                sector, industry, and market capitalization is passed to you.  \n
                Your task is to generate a description that is displayed to the user. \n
                Note, the description provided is displayed on web application that is accessed \
                by professionals within the Ghanaian investment industry so the language should be professional \
                and not conversational. Also, no need to apologise, just get straight to the point. \n
                Your response should always begin with the company name provided to you. \n
                Company name: {} \n
                Company ticker: {} \n
                Company sector: {} \n
                Company industry: {} \n
                Company market capitalization {}"""


TREND_CHART_PROMPT = """You are a web application from which insights on Stocks is obtained. \n
                The user interface of this web application contains a list of stocks on the Ghana Stock Exchange. \n
                Each time a user of the web application selects a ticker, the company name as well it's measures of central tendency \
                will be passed. Your task is to generate a short financial analysis based on the passed central tendency measures. \
                Note, the description provided is displayed on web application that is accessed. Get straight to the point. \
                by professionals so the language should be professional and succinct.  No need to reference the fact that \
                measures of central tendency were passed. Start Analysis as a sentence. Also, no bullet points or boldened characters.  \n
                Company name: {} \n
                current price: {} \n
                average price: {} \n
                median price: {} \n
                price standard deviation: {} \n
                minimum price: {} \n
                maximum price: {} \n
                price at inception: {} \n
                inception date: {} \n
                """

EQUITY_DB_DATE_COL = "trade_date"
EQUITY_DB_PRICE_COL = "closing_price"
