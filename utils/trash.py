import yfinance as yf
import requests
session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
stk = yf.Ticker('RELIANCE.NS TCS.NS', session=session)
df = stk.get_calendar()
print(df)
