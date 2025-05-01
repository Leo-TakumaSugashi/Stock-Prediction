import re,os,sys
# base_dir = '/home/pyt/anaconda3/envs/LSTM-Stock'
# for root, dirs, files in os.walk(base_dir):
    # sys.path.append(root)
import requests
from bs4 import BeautifulSoup as BS
# import pandas as pd
from datetime import date, timedelta, datetime
# import yfinance as yf
sys.path.append("/home/pyt/Python")
import leo_function as leo
from subFunctions import *

# SaveList = "Symbol_List.txt"

def scrape_historical_data(symbol, save_dir):
    file_name = os.path.join(os.getcwd(), save_dir, symbol + '_historical_data.csv')
    if os.path.exists(file_name):
        check = pd.read_csv(file_name)
        check['Date'] = pd.to_datetime(check['Date'])
        Start = check['Date'].max()
        check = check[check['Date']!=Start].copy()
        End = date.today() + timedelta(2)
        End.strftime('%Y-%m-%d')
        data = yf.download(symbol, start=Start, end=End)
        data = data.reset_index()
        data.rename(columns={'index': 'Date'}, inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        catdata = pd.concat([check,data],axis=0)
        output = catdata.drop_duplicates(subset=['Date']).copy()
        pSTR = ' Reload:'
    else:
        data = yf.download(symbol)
        data = data.reset_index()
        data.rename(columns={'index': 'Date'}, inplace=True)
        output = data
        pSTR = '   New :'
    
    output.to_csv(file_name, index=False)

    FigName = ''.join(['logs/TB_logs-',Today,'/',symbol,'-last30d.png'])
    output_mpf(output, 30, symbol, FigName)
    print(pSTR, file_name)


Error  = []
with open(ListFile,'r') as f:
    ArchiveL = [l.strip() for l in f]
for Symbol in ArchiveL:
    try:
        scrape_historical_data(Symbol,'data')
    except Exception as e:
        print(f"Error at index {Symbol}: {e}")
        Error.append(Symbol)

print("#### #### Error Symbols #### #### ####")
print(Error)