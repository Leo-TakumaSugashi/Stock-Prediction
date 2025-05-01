import yfinance as yf
import os,sys
import pandas as pd
from datetime import date,timedelta,datetime
import mplfinance as mpf

ListInfoFile = "Symbol_List_Info.csv"
ListFile = 'Symbol_List.txt'
Today = date.today().strftime('%Y-%m-%d')
def get_options(symbol):
    yfTicker = yf.Ticker(symbol)

    # 取得する項目のリスト
    attributes = [
        ("actions", "actions"),
        ("dividends", "dividends"),
        ("splits", "splits"),
        ("financials", "financials"),
        ("quarterly_financials", "quarterly_financials"),
        ("major_holders", "major_holders"),
        ("institutional_holders", "institutional_holders"),
        ("balance_sheet", "balance_sheet"),
        ("quarterly_balance_sheet", "quarterly_balance_sheet"),
        ("cashflow", "cashflow"),
        ("quarterly_cashflow", "quarterly_cashflow"),
        ("earnings", "earnings"),
        ("quarterly_earnings", "quarterly_earnings"),
        ("sustainability", "sustainability"),
        ("recommendations", "recommendations"),
        ("calendar", "calendar"),
        ("isin", "isin"),
        ("options", "options")
    ]

    # 結果を格納する辞書
    Dict = {}
    for key, attr in attributes:
        try:
            Dict[key] = getattr(yfTicker, attr)  # 動的に属性を取得
        except Exception as e:
            Dict[key] = f"Error: {e}"

    try:
        Dict[f"option_chain({Today})"] = yfTicker.option_chain(Today)
    except Exception as e:
        Dict[f"option_chain({Today})"] = f"Error: {e}"

    return Dict

def print_options_memo():
    STR = ["\
    #株式情報を取得する yfTicker.info\
    # 過去の市場データを取得する hist = yfTicker.history(period = 'max') \
    # アクション(配当、分割)を表示 \
    yfTicker.actions \
    '\n'\
    # 配当を表示\
    yfTicker.dividends\
    '\n'\
    # 分割を表示\
    yfTicker.splits\
    '\n'\
    # 財務情報を表示\
    yfTicker.financials\
    yfTicker.quarterly_financials\
    '\n'\
    # 主要な所有者を表示\
    yfTicker.major_holders\
    '\n'\
    # 機関保有者を表示\
    yfTicker.institutional_holders\
    '\n'\
    # バランスシートを表示\
    yfTicker.balance_sheet\
    yfTicker.quarterly_balance_sheet\
    '\n'\
    # キャッシュフローを表示\
    yfTicker.cashflow\
    yfTicker.quarterly_cashflow\
    '\n'\
    # 収益を表示\
    yfTicker.earnings\
    yfTicker.quarterly_earnings\
    '\n'\
    # 持続可能性を示す\
    yfTicker.sustainability\
    '\n'\
    # アナリストの推奨事項を表示\
    yfTicker.recommendations\
    '\n'\
    # 次のイベント(収益など)を表示\
    yfTicker.calendar\
    '\n'\
    # ISINコードを表示-*実験的*\
    # ISIN =国際証券識別番号\
    yfTicker.isin\
    '\n'\
    # オプションの有効期限を表示\
    yfTicker.options\
    '\n'\
    特定の有効期限のオプションチェーンを取得\
    opt = yfTicker.option_chain( 'YYYY-MM-DD')\
    # データは次の方法で入手できます:opt.calls、opt.puts "]
    print(STR)
    return STR
    
def get_name(symbol):
    try:
        df = pd.read_csv(ListInfoFile)
        ind = df['Symbol']==symbol
        x = df[ind].copy()
        output_Dict = { "Symbol": f"{symbol}",
                        "Name": x["Name"].values[0],
                        "LongName": x["FullName"].values[0],
                        "Market" :x["Market"].values[0],
                        "Sector" : x["Sector"].values[0]}
        return output_Dict
    except Exception as e:
        print(f" No Symbol in ${ListInfoFile} ${symbol} : ${e}")
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            output_Dict = {"Symbol": f"{symbol}",
                           "Name": f"{info.get('shortName', 'N/A')}",
                           "LongName": f"{info.get('longName', 'N/A')}",
                           "Market" :f"{info.get('market', 'N/A')}",
                           "Sector" : f"{info.get('sector', 'N/A')}"}
            return output_Dict
        except Exception as e:
            print(f" Error in get_name(yf.Ticker) ${symbol} : ${e}")
            return None

def Symbol2Names():
    with open(ListFile,'r') as f:
        Symbols = [L.strip() for L in f]

    Sy = []
    Na = []
    lNa = []
    Ma = []
    Se = []
    Co = []
    c = 0
    for Symbol in Symbols:
        D = get_name(Symbol)
        if not D is None:
            Sy.append(D["Symbol"])
            Na.append(D["Name"])
            lNa.append(D["LongName"])
            Ma.append(D["Market"])
            Se.append(D["Sector"])
            Co.append(str(c))
            c = c + 1

    data = pd.DataFrame({"Index":Co,"Symbol":Sy, "Name":Na, "Market":Ma, "Sector":Se, "FullName":lNa})
    os.system(f"mv {ListInfoFile} Archive/{Today}-{ListInfoFile}")
    data.to_csv(ListInfoFile, index=False)

def get_ListInfoFile():
    return pd.read_csv(ListInfoFile, index_col=0)

def output_mpf(data, Days, TitleSTR, figname):
    if data.index.name is not None and \
        ('Date' in data.index.name or 'Datetime' in data.index.name):
        data.index = pd.to_datetime(data.index, utc=True)
    else:
        if 'Date' in data.columns and not 'Datetime' in data.columns:
            data.rename(columns={'Date': 'Datetime'}, inplace=True)
        data['Datetime'] = pd.to_datetime(data['Datetime'], utc=True)
        data.set_index('Datetime', inplace=True)
    End = data.index.max()
    Start = End - timedelta(days=Days)
    ind = data.index >= Start
    x = data[ind].copy()
    mpf.plot(x,type='candle',mav=(3,6,9),volume=True,\
        title=TitleSTR, savefig=figname)



def make_table():
    outputFilename = f"login/tables/Summary{Today}.csv"
    data = get_ListInfoFile()
    Symbols = data['Symbol']
    SymbolsList = Symbols.tolist()
    Table = pd.DataFrame(columns=['Symbol', 'FullName', 'Sector','startDate', 'endDate', 'Duration',\
         'LatestClose', 'Prediction1wA', 'Prediction1mA', 'Gaps1wA', 'Gaps1mA','1wA%','1mA%','Validation', 'Accuracy1wB' ])
    Table['Symbol'] = SymbolsList
    print(data.head)
    print("###########################################################################")
    c = 0
    for n in range(0,len(SymbolsList)):
        symbol = SymbolsList[n]
        print(symbol)
        try:
            fname = symbol + '_historical_data.csv'
            ind = SymbolsList.index(symbol)
            Name = data.loc[ind,'FullName']
            Sector = data.loc[ind, 'Sector']
            hdata = pd.read_csv('data/' + fname)
            minD = hdata['Date'].min()
            maxD = hdata['Date'].max()
            Duration = pd.to_datetime(maxD) - pd.to_datetime(minD)
            Latest = hdata[hdata['Date']==maxD].copy()
            lc = Latest['Close'].values
            fdata = pd.read_csv(f"logs/TB_logs-{Today}/{symbol}_tmp.csv")
            After1w = pd.to_datetime(maxD) + pd.Timedelta(days=7)
            After1m = pd.to_datetime(maxD) + pd.Timedelta(days=28)
            After1w_str = After1w.strftime('%Y-%m-%d')
            After1m_str = After1m.strftime('%Y-%m-%d')
            a1w = fdata[fdata['date']==After1w_str]['future'].values
            a1m = fdata[fdata['date']==After1m_str]['future'].values
            # print(f"{After1w.strftime('%Y-%m-%d')}")
            # print(Latest['Close'].values)
            Table.loc[n, 'Symbol'] = symbol
            Table.loc[n, 'FullName'] = Name
            Table.loc[n, 'Sector'] = Sector
            Table.loc[n, 'startDate'] = minD
            Table.loc[n, 'endDate'] = maxD
            Table.loc[n, 'Duration'] = Duration.days
            Table.loc[n, 'LatestClose'] = lc
            Table.loc[n, 'Prediction1wA'] = a1w
            Table.loc[n, 'Prediction1mA'] = a1m
            Table.loc[n, 'Gaps1wA'] = a1w - lc
            Table.loc[n, 'Gaps1mA'] = a1m - lc
            Table.loc[n, '1wA%'] = a1w / lc
            Table.loc[n, '1mA%'] = a1m / lc
            Table.loc[n, 'Validation'] = 'V'
            Table.loc[n, 'Accuracy1wB'] = 'HELLp'
            # Table.loc[n, 'Symbol'] = symbol
            # print(type(Duration.days))
            # print(f"{symbol},   startDate : {minD} ,   endDate : {maxD},  Duration: {Duration.days} ")
            
        except Exception as e:
            print(f"Error read csv. : {e}")
    print("###########################################################################")
    Table.to_csv(outputFilename, index=False)