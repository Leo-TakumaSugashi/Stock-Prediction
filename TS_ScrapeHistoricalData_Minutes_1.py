import re,os,sys
# base_dir = '/home/pyt/anaconda3/envs/LSTM-Stock'
# for root, dirs, files in os.walk(base_dir):
    # sys.path.append(root)
import requests
from bs4 import BeautifulSoup as BS
# import pandas as pd
from datetime import date, timedelta, datetime
from subFunctions import *
import finplot as fplt

# SaveList = "Symbol_List.txt"

def scrape_historical_data(symbol, save_dir,ex):
    file_name = os.path.join(os.getcwd(), save_dir, symbol + '_historical_data_' + ex + '.csv') ## <-- 1min
    if os.path.exists(file_name):
        check = pd.read_csv(file_name)
        check['Datetime'] = pd.to_datetime(check['Datetime'])
        
        max_datetime = check['Datetime'].max()
        Start = max_datetime.tz_convert('UTC')
        
        check = check[check['Datetime']!=Start].copy()
        End = date.today()
        Start2 = End - timedelta(days=8)
        Start2 = pd.to_datetime(Start2).tz_localize('UTC', ambiguous='NaT')
        check_dates = pd.to_datetime([Start, Start2])
        # check_datets = check_dates.dt.tz_localize('UTC', ambiguous='NaT')
        End = pd.to_datetime(End).tz_localize('UTC', ambiguous='NaT')
        Start = check_dates.max()
        print(f"{Start}  --  {End}")
        End.strftime('%Y-%m-%d')
        
        data = yf.download(symbol, start=Start, end=End, period='max', interval=ex) ## <-- 1min
        data = data.reset_index()
        data.rename(columns={'index': 'Datetime'}, inplace=True)
        data['Datetime'] = pd.to_datetime(data['Datetime'])
        catdata = pd.concat([check,data],axis=0)
        output = catdata.drop_duplicates(subset=['Datetime']).copy()
        pSTR = ' Reload:'
    else:
        data = yf.download(symbol, period='max', interval=ex) #<-- 1min
        data = data.reset_index()
        data.rename(columns={'index': 'Datetime'}, inplace=True)
        output = data
        pSTR = '   New :'
    
    output.to_csv(file_name, index=False)
    print(pSTR, file_name)
    # fplt.candlestick_ochl(output[['Open','Close','High','Low']])
    # fplt.savefig('testAAPL.png')
    # fplt.show()


Error  = ''
ex = '1m'
# scrape_historical_data('AAPL','data-'+ex, ex) #<-- 1min

with open(ListFile,'r') as f:
    ArchiveL = [l.strip() for l in f]
for Symbol in ArchiveL:
    TF = True
    c = 0
    Maxloop=100
    while TF:
        try:
            scrape_historical_data(Symbol,'data-'+ex, ex)
            TF = False
        except Exception as e:
            c += 1
            if c > Maxloop:
                TF = False
                Error += f"{Symbol}\n"
            
            print(f"Error at index {Symbol}: {e}")
            print(f"\n  loop:{str(c)}\n")

                

print("#### #### Error Symbols #### #### ####")
print(Error)
with open(f"Error-log-Scrape-{Today}.txt",'w') as f:
    f.write(Error)