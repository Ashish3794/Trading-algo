def create_link(stock_list):
    links = {}
    for stock in stock_list:
        path = "https://in.tradingview.com/chart/?symbol=NSE%3A"+stock
        # f_url = stock
        # val = "<a href='{}'>{}</a>".format(path, f_url)
        # val = "https://in.tradingview.com/chart/?symbol=NSE%3A"+stock
        # links[stock] = "[{}]({})".format(stock, path)
        links[stock] = path
    return links
