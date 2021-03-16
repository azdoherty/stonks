import yfinance as yf

amd = yf.Ticker('amd')
hist = amd.history(period='max')

print(hist)