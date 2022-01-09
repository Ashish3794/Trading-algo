from datetime import date
from nsepy import get_history
import os
import streamlit as st


def fetch_data(data, name):
    data.drop(['Series', 'Last', 'VWAP', 'Volume', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble', 'Prev Close'], inplace = True, axis = 1)
    data["44MA"] = [0]*len(data)
    data_ma = [0]*len(data)
    data.reset_index(inplace = True)
    for i in range(43, len(data)):
        data_ma[i] = sum(data["Close"][i-43 : i+1])/44 
    data["44MA"] = data_ma
    data.to_excel('moving_average/data/'+name+'.xlsx')

def collect_data(stock_list):
    path = 'moving_average/data/'
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    for stock in stock_list:
        st.markdown("Collecting data for: "+stock)
        data = get_history(symbol = stock, start = date(2021, 1, 1), end = date.today())
        data.reset_index(inplace = True)
        
        if len(data)>0:
            #Use fetch_data() for first time use
            fetch_data(data, stock)
