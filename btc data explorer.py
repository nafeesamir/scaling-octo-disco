import ccxt
import pandas as pd
import mplfinance as mpf

print('this is the list of different exchanges you could access:\n')
print(ccxt.exchanges)
    
exchange = input('Enter the ccxt exchange you would like to use: ')

while exchange not in ccxt.exchanges:
    exchange = input(f'{exchange} not a ccxt exchange\ntry again: ')

print(f'here are the symbols in {exchange}')
exchange = getattr(ccxt,exchange)()
exchange.load_markets()
print(exchange.symbols)
symbol = input('Enter the symbol you would like to view:')

start = input("Enter the date you would like the data points to start from: ") 
end = input("Enter the date you would like the data points to end at (or enter T for today's date): ")
timeframe = input('Enter the timeframe you would like each candle to be: ')

if 'T' in end:
    end = exchange.milliseconds()
else:
    end = exchange.parse8601(end+'T00:00:00Z')
start_ms = exchange.parse8601(start+"T00:00:00Z")
timeframe_ms = exchange.parse_timeframe(timeframe)*1000
limit = (end - start_ms)//timeframe_ms

date_start = pd.to_datetime((start_ms), unit = 'ms')
date_end = pd.to_datetime((end), unit = 'ms')
print(f'from {date_start} to {date_end}:')
all_bars=[]
while start_ms<end:
    bars = exchange.fetch_ohlcv(symbol,timeframe = timeframe,since =start_ms, limit =limit)
    if not bars:
        break
    all_bars+=[b for b in bars if b[0]<end]
    start_ms = bars[-1][0]+1
    
    


df =pd.DataFrame(all_bars, columns =['timestamp','open','high','low','close','volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'],unit = 'ms') 
df = df.set_index('timestamp')

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)

print(df)

df['avg b/highlow'] = (df['high']+df['low'])/2
additional_plots = mpf.make_addplot(df['avg b/highlow'], color = 'black')

mpf.plot(df,type='candle',volume = True, mav=(7),title = 'BTCUSDT', style = 'tradingview',addplot=additional_plots)
mpf.show()
