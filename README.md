# scaling-octo-disco
install - requirements.txt

btc data explorer.py prompts the user for a date and timeframe in a specific format. It then returns:
  - a table/list of timestamped information (such as open, close, high. low and volume),
  - a separate table/list - where it only lists the timestamp and average price of each candle based on its high and low (avg b/highlow)
  - a candlestick chart with 2 lines
      the moving average for the past 7 candles
      the avg b/highlow plotted into a line
