import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from arch import arch_model

exchange = ccxt.binance()
symbol = 'BTCUSDT'
#input date, turn it into parse
since = exchange.parse8601(input("input start date\nlike this: 2025-01-01\n")+"T00:00:00Z")
#input timeframe, keep it as str
timeframe = input('timeframe: 1s,1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M\n')
#today's date, turn it parse
today = exchange.parse8601('2026-11-10T00:00:00Z')

#convert timeframe into parse/ms
time_parse ={
    '1s':1000,
    '1m':60*1000,
    '3m':3*60*1000,
    '5m':5*60*1000,
    '15m':15*60*1000,
    '30m':30*60*1000,
    '1h':60*60*1000,
    '2h':2*60*60*1000,
    '4h':4*60*60*1000,
    '6h':6*60*60*1000,
    '8h':8*60*60*1000,
    '12h':12*60*60*1000,
    '1d':24*60*60*1000,
    '3d':3*24*60*60*1000,
    '1w':7*24*60*60*1000,
    '1M':30*24*60*60*1000
    } 

end = since + time_parse[timeframe]*1000
date_since = pd.to_datetime(since,unit ='ms')
date_end = pd.to_datetime(end,unit ='ms')
print(f'From {date_since} to {date_end}')
#num of candles they want to request
limit = (today-since)//time_parse[timeframe]


all_bars=[]
while True:
    bars=exchange.fetch_ohlcv(symbol,timeframe=timeframe,since=since,limit=limit)
    if not bars:
        break
    all_bars += [b for b in bars if b[0] < end]
    since = bars[-1][0] + 1


df =pd.DataFrame(all_bars, columns =['timestamp','open','high','low','close','volume'])
#df = df.drop('open',axis=1).drop('high',axis=1).drop('low',axis=1)
df['timestamp'] = pd.to_datetime(df['timestamp'],unit = 'ms') 
df = df.set_index('timestamp')
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)
print(df)
df['avg b/highlow'] = (df['high']+df['low'])//2
additional_plots = mpf.make_addplot(df['avg b/highlow'], color = 'black')

mpf.plot(df,type='candle',volume = True, mav=(7),title = 'BTCUSDT', style = 'tradingview',addplot=additional_plots)
mpf.show()



