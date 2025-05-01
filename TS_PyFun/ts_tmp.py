#! /usr/bin/env python3
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from matplotlib import pyplot as plt
import sys,os,json

def get_close(ticker):
    Asset = pd.DataFrame(yf.download(ticker, start=Start, end=End)['Adj Close'])
    return Asset

def get_name(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    output_Dict = {'Symbol': f"{symbol}",
                   "Name": f"{info.get('shortName', 'N/A')}",
                   "Market" :f"{info.get('market', 'N/A')}",
                   "Sector" : f"{info.get('sector', 'N/A')}",
                   "start-Date" : [],
                   "end-Date": [],
                   "create-Date" : []}
    return output_Dict

symbols = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'TSM']
Start = date.today() - timedelta(365)
Start.strftime('%Y-%m-%d')

End = date.today() + timedelta(2)
End.strftime('%Y-%m-%d')

List = []
for s in symbols:
    List.append(get_name(s))

with open('symbols_list.json', 'w') as json_file:
    json.dump(List, json_file, indent=4)  # 
    
sys.exit(1)

TSMC = get_close('TSM')

fgh = plt.figure(figsize = (5,5), facecolor='white')
plt.plot(TSMC)
plt.show(block=True)
fgh.savefig('TSM.png')
