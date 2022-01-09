import pandas as pd
from datetime import date
import os
import glob
import streamlit as st

def calculate(data, name, df, links):
    
    end = len(data)-1
    ma_check_list = data["44MA"][end-10: end+1]
    check = all(i <= j for i, j in zip(ma_check_list, ma_check_list[1:]))    #to check if the 44MA graph is strictly increasing
    
    open_price = data.loc[end, "Open"]
    close_price = data.loc[end, "Close"]
    high_price = data.loc[end, "High"]
    low_price = data.loc[end, "Low"]
    ma_price = data.loc[end, "44MA"]
    text = ''
    if open_price < close_price and check:            #Check for reen candle and increasing 44MA graph
        
        diff = (abs(low_price - ma_price)/low_price)*100       #Diff between 44MA graph and low of the candle
        mid = (close_price + open_price)/2
        
        if  (diff <= 2 and ma_price <= mid) or (ma_price <= mid and ma_price >= low_price) :
            if (data.loc[end-1, "Open"] >= data.loc[end-1, "Close"]):
                if close_price >= data.loc[end-1, "Open"]:

                    text += "Call available for " + str(name.split('.')[0]) + '\n'

                    buy = round(data.loc[end, "High"])+1
                    text += "Buy Price: "+ str(buy) +'\n'

                    stoploss = min(round(data.loc[end, "Low"])-1, round(data.loc[end-1, "Low"])-1)
                    text += "Stoploss: " + str(stoploss) + '\n'

                    target = round((2*(buy-stoploss))+buy)
                    text += "Target price: " + str(round((2*(buy-stoploss))+buy)) + '\n'

                    
                    gain_percent = str(round(((target-buy)/buy)*100))
                    text += "Gain: "+gain_percent+"%\n"

                    loss_percent = str(round(((buy-stoploss)/buy)*100))
                    text += "Loss: "+loss_percent+"%\n"

                    text += "-----------------------------------\n"

                    df["Name"].append(name)
                    df["Buy Price"].append(buy)
                    df["Stoploss"].append(stoploss)
                    df["Target Price"].append(target)
                    df["Gain %"].append(gain_percent)
                    df["Loss %"].append(loss_percent)
                    df["Link"].append(links[name])

                    return text
            else:
                text += "Call available for " + str(name.split('.')[0]) + '\n'

                buy = round(data.loc[end, "High"])+1
                text += "Buy Price: "+ str(buy) +'\n'

                stoploss = min(round(data.loc[end, "Low"])-1, round(data.loc[end-1, "Low"])-1)
                text += "Stoploss: " + str(stoploss) + '\n'
                
                target = round((2*(buy-stoploss))+buy)
                text += "Target price: " + str(target) + '\n'
                
                gain_percent = str(round(((target-buy)/buy)*100))
                text += "Gain: " + gain_percent + "%\n"

                loss_percent = str(round(((buy-stoploss)/buy)*100))
                text += "Loss: " + loss_percent + "%\n"

                text += "-----------------------------------\n"
            
                df["Name"].append(name)
                df["Buy Price"].append(buy)
                df["Stoploss"].append(stoploss)
                df["Target Price"].append(target)
                df["Gain %"].append(gain_percent)
                df["Loss %"].append(loss_percent)
                df["Link"].append(links[name])

                return text

def fun(path):
    # returns the final component of a url
    f_url = os.path.basename(path)
    # convert the url into link
    return '<a href="{}">{}</a>'.format(path, f_url)

def algo(links):
    text = ''
    files = glob.glob("moving_average/data/*")
    df = {"Name": [], "Buy Price": [], "Target Price": [], "Stoploss": [], "Gain %": [], "Loss %": [], "Link" : []}
    for name in files:
        data = pd.read_excel(name)
        data = data.iloc[: , 1:]            #To remove the first unnamed column
        name = name.split('.')[0].split('\\')[1]
        out = calculate(data, name, df, links)

        if out != None:
            text += out
    output = pd.DataFrame(df)
    # output = output.to_html(escape=False)
    output = output.style.format({'Link' : fun})
    st.title("44 Moving Average Results")
    st.dataframe(output)
    with open('moving_average/Calls/'+str(date.today())+'.txt', 'w') as f:
        f.write(text)