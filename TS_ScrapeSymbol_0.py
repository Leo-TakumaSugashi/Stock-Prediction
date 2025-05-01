import re,os,sys,math
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
# import webbrowser
# import yfinance as yf
from datetime import date
from subFunctions import Symbol2Names


urlA = "https://finance.yahoo.com/markets/stocks/most-active/?start="
urlB = "&count=25"
url_trending = "https://finance.yahoo.com/markets/stocks/trending/"
url_gainersA = "https://finance.yahoo.com/markets/stocks/gainers/?start="
# url_gainersB = "&count=25"
url_52WgainersA = "https://finance.yahoo.com/markets/stocks/52-week-gainers/?start=" #1775
# url_52WgainersB = "&count=25"

SaveList = "Symbol_List.txt"
Today = date.today().strftime('%Y-%m-%d')

def get_Symbols(url,L):
    red = requests.get(url)
    soup = BS(red.text,'lxml')
    # divs = soup.find_all('div',class_=re.compile('tableContainer'))
    divs = soup.find_all('span',class_=re.compile('symbol'))
    for div in divs:
        L.add(div.get_text())
        print(div.get_text()+',',end='')
    print('')
    return L

def loop(urlA,urlB,End,Step,Name='Most Active',L = set()):
    for n in range(0,End+1): ## most Active
        inURL = ''.join([urlA,str(n*Step+1),urlB])
        L = get_Symbols(inURL,L)
        print(''.join([Name, " : ",str(n+1).zfill(3),'/',str(End).zfill(3),' ',inURL])) 
    return L

def scrape_fun():
    L = loop(urlA, urlB, 20, 25, 'Most Active', set())
    print('Trending... ')
    L = get_Symbols(url_trending,L) ## trending

    L = loop(url_gainersA, urlB,3, 25, 'Gainers', L)
    L = loop(url_52WgainersA, urlB,71, 25, '52week Gainers', L)

    with open(SaveList,'r') as f:
        ArchiveL = [l.strip() for l in f]
    
    for n in ArchiveL:
        L.add(n)

    LL = print_symbols_main(L)
    print("Current Number of Symbol List is " + str(len(ArchiveL)))
    print("New Number of Symbol List is " + str(len(LL)))
    return LL

def append_list(LL):
    Prompt = f"mv {SaveList} Archive/{Today}-{SaveList}"
    print(Prompt)
    os.system(Prompt)

    with open(SaveList,'w') as f:
        for n in LL:
            f.write(n + '\n')

    Symbol2Names()

def print_symbols(Short,row,strNum):
    c = 1
    for i,l in enumerate(Short):
        l = f"{l}," + " " *(strNum-len(l))
        if c >= row:
            print(l)
            c = 1
        else:
            print(l, end='')
            c +=1
        if (i == len(Short) -1 and  c != row):
            print("")

def print_symbols_main(LL):
    print("New List is ... \n" + "-"*(128))
    LL = sorted(list(LL))
    Long = []
    Llen = []
    Short = set()
    LongSymbol = set()
    for l in LL:
        if len(l) >=6:
            LongSymbol.add(l)
            Long.append(l.replace(' ','_'))
            Llen.append(len(l))
        else:
            Short.add(l.replace(' ',''))
    NewList = Short
    for l in list(LongSymbol):
        NewList.add(l)

    Lmax = pd.DataFrame(Llen).max()[0] if Llen else None
    print_symbols(Short,17,5)
    print_symbols(Long,math.floor(17*5/Lmax),Lmax)
    print("\n" + "_"*128)
    return NewList

if __name__ == "__main__":
    LL = scrape_fun()
    while True:
        user_input = input("Update Symbol list?? (yes/no): ").strip().lower()
        if user_input == "yes":
            # LL = print_symbols_main(LL)
            append_list(LL)
            break  # プログラムが実行されたのでループを終了
        elif user_input == "no":
            # print_symbols_main(LL):
            print('>>> Return ...\n\n')
            break  # プログラムは実行されなかったのでループを終了
        else:
            print("無効な入力です。'yes' または 'no' を入力してください。")
