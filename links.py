def create_link(stock_list):
    links = {}
    for stock in stock_list:
        path = "https://in.tradingview.com/chart/?symbol=NSE%3A"+stock
        links[stock] = path
    return links
