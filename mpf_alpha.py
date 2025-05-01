import re,os,sys
from datetime import date, timedelta, datetime
from subFunctions import Today,output_mpf,ListFile,pd,yf

# SaveList = "Symbol_List.txt"

def mpf_figure(symbol):
    file_name = os.path.join(os.getcwd(), 'data', symbol + '_historical_data.csv')
    data = pd.read_csv(file_name)
    FigName = ''.join(['TB_logs-',Today,'/',symbol,'-last30d.png'])
    output_mpf(data, 30, symbol, FigName)


Error  = []
# mpf_figure('GOOGL')
with open(ListFile,'r') as f:
    ArchiveL = [l.strip() for l in f]
for Symbol in ArchiveL:
    try:
        mpf_figure(Symbol)
    except Exception as e:
        print(f"Error at index {Symbol}: {e}")
        Error.append(Symbol)

if not Error is None:
    print("#### #### Error Symbols #### #### ####")
    print(Error)