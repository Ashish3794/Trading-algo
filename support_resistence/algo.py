import pandas as pd
from datetime import date
from nsepy import get_history
import pandas as pd
from tqdm import tqdm
import glob
import streamlit as st
import os

def isSupport(df,i):
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
    return support
def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

def fun(path):
    # returns the final component of a url
    f_url = os.path.basename(path)
    # convert the url into link
    return "<a href='{}'>{}</a>".format(path, f_url)

def sup_res(links):
    out_text = ""
    df = {"Name": [], "Buy Price": [], "Target Price": [], "Link" : []}
    stock_list = glob.glob("moving_average/data/*")
    for stock in tqdm(stock_list):
        data = pd.read_excel(stock)
        end = len(data)-1
        ma_check_list = data["44MA"][end-10: end+1]
        check = all(i <= j for i, j in zip(ma_check_list, ma_check_list[1:]))
        if check:
            support_price = []
            resistence_price = []
            for i in range(2, len(data)-2):
                support = isSupport(data, i)
                resistence = isResistance(data, i)
                if support:
                    support_price.append(data['Low'][i])
                if resistence:
                    resistence_price.append(data['High'][i])
            levels = support_price + resistence_price
            levels.sort()
            current_price = data['Close'][len(data)-1]
            flag = 0
            for i in range(len(levels)-1, 0, -1):
                if (levels[i-1] <= current_price) and (current_price<levels[i]):
                    buy_price = levels[i-1]
                    sell_price = levels[i]
                    if ((current_price-buy_price)/buy_price)*100<=2 and ((current_price-buy_price)/buy_price)*100>=0  and ((sell_price-buy_price)/buy_price)*100 >= 5:
                        flag = 1
                    break
            if flag:  
                stock_name = stock.split(".")[0].split("\\")[-1]
                out_text += stock_name + '\n' + "Buy Price: " + str(buy_price) + '\n' + "Sell Price: " + str(sell_price) + '\n' + "----"*10 + '\n'  
                df["Name"].append(stock_name)
                df["Buy Price"].append(buy_price)
                df["Target Price"].append(sell_price)
                df["Link"].append(links[stock_name])
    output = pd.DataFrame(df)
    print(output)
    # final_output = output.style.format({'Link' : fun})
    # html_output = output.to_html(escape = False)
    st.title("Support and Resistence Level Results")
    # st.table(final_output)
    # print(html_output)
    st.dataframe(output)
#     import streamlit.components.v1 as components  # Import Streamlit

# # Render the h1 block, contained in a frame of size 200x200.
#     components.html(html_output)
    with open('support_resistence/Calls/'+str(date.today())+'.txt', 'w') as f:
        f.write(out_text)
    