import pandas as pd
from moving_average.fetch_data import collect_data
from moving_average.algorithm import algo
from support_resistence.algo import sup_res
from links import create_link

data = pd.read_csv('ind_nifty500list.csv')
stock_list = []
for i in range(len(data)):
    stock_list.append(data.loc[i, "Symbol"])
stock_list.append("LALPATHLAB")

links = create_link(stock_list)
collect_data(stock_list)
algo(links)

sup_res(links)