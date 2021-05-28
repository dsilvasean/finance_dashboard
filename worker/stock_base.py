import csv, json, os, sys, ast, math
import pickle
import pandas as pd
import yfinance as yf
# from worker.const import static_assets
# from const import static_assets
from .const import static_assets
# static_assets = "/mnt/c/final/frontend/web/static_assets"
emp_dict = {'zip': '', 'sector': '', 'fullTimeEmployees': '', 'longBusinessSummary': '', 'city': '', 'phone': '', 'state': '', 'country': '', 'companyOfficers': '', 'website': '', 'maxAge': '', 'address1': '', 'fax': '', 'industry': '', 'previousClose': 0, 'regularMarketOpen': 0, 'twoHundredDayAverage': '', 'trailingAnnualDividendYield': '', 'payoutRatio': '', 'volume24Hr': '', 'regularMarketDayHigh': '', 'navPrice': '', 'averageDailyVolume10Day': '', 'totalAssets': '', 'regularMarketPreviousClose': '', 'fiftyDayAverage': '', 'trailingAnnualDividendRate': '', 'open': '', 'toCurrency': '', 'averageVolume10days': '', 'expireDate': '', 'yield': '', 'algorithm': '', 'dividendRate': '', 'exDividendDate': '', 'beta': 0, 'circulatingSupply': '', 'startDate': '', 'regularMarketDayLow': '', 'priceHint': '', 'currency': '', 'trailingPE': '', 'regularMarketVolume': '', 'lastMarket': '', 'maxSupply': '', 'openInterest': '', 'marketCap': 0, 'volumeAllCurrencies': '', 'strikePrice': '', 'averageVolume': '', 'priceToSalesTrailing12Months': '', 'dayLow': '', 'ask': '', 'ytdReturn': '', 'askSize': '', 'volume': '', 'fiftyTwoWeekHigh': 0, 'forwardPE': '', 'fromCurrency': '', 'fiveYearAvgDividendYield': '', 'fiftyTwoWeekLow': 0, 'bid': '', 'tradeable': '', 'dividendYield': 0, 'bidSize': '', 'dayHigh': '', 'exchange': '', 'shortName': '', 'longName': '', 'exchangeTimezoneName': '', 'exchangeTimezoneShortName': '', 'isEsgPopulated': '', 'gmtOffSetMilliseconds': '', 'quoteType': '', 'symbol': '', 'messageBoardId': '', 'market': '', 'annualHoldingsTurnover': '', 'enterpriseToRevenue': '', 'beta3Year': '', 'profitMargins': '', 'enterpriseToEbitda': '', '52WeekChange': '', 'morningStarRiskRating': '', 'forwardEps': 0, 'revenueQuarterlyGrowth': '', 'sharesOutstanding': 1, 'fundInceptionDate': '', 'annualReportExpenseRatio': '', 'bookValue': '', 'sharesShort': '', 'sharesPercentSharesOut': '', 'fundFamily': '', 'lastFiscalYearEnd': '', 'heldPercentInstitutions': '', 'netIncomeToCommon': '', 'trailingEps': 0, 'lastDividendValue': '', 'SandP52WeekChange': '', 'priceToBook': '', 'heldPercentInsiders': '', 'nextFiscalYearEnd': '', 'mostRecentQuarter': '', 'shortRatio': '', 'sharesShortPreviousMonthDate': '', 'floatShares': '', 'enterpriseValue': '', 'threeYearAverageReturn': '', 'lastSplitDate': '', 'lastSplitFactor': '', 'legalType': '', 'morningStarOverallRating': '', 'earningsQuarterlyGrowth': '', 'dateShortInterest': '', 'pegRatio': '', 'lastCapGain': '', 'shortPercentOfFloat': '', 'sharesShortPriorMonth': '', 'category': '', 'fiveYearAverageReturn': '', 'regularMarketPrice': 1, 'logo_url': ''}

class Stock():
    def __init__(self, ticker, isin_code):
        self.stk = yf.Ticker(ticker)
        self.ticker = ticker
        self.isin_code = isin_code
        with open(f"{static_assets}/data.p", 'rb') as pk:
            data_ = pickle.load(pk)
        try:
            data = ast.literal_eval(f"{data_[ticker]}")
        except:
            data = ast.literal_eval('NONE.NS')
        try:
            self.sector = data['sector']
        except:
            data = emp_dict
        if data['dividendYield'] == None:
            data['dividendYield'] = 0
        if data['beta'] == None:
            data['beta'] == 0
        if data['bookValue'] == "" or data['bookValue'] == None:
            data['bookValue'] = 1
        if data['forwardEps'] ==None:
            data['forwardEps'] = 1
        if data['trailingEps'] ==None:
            data['trailingEps'] = 1
        self.sector = data['sector'] 
        self.dividendYield = data['dividendYield'] * 100
        self.sharesOutstanding = data['sharesOutstanding']
        print(data['regularMarketPrice'])
        print(type(data['regularMarketPrice']))
        self.regularMarketPrice = float(data['regularMarketPrice'])
        self.previousClose = data['previousClose']
        self.regularMarketOpen = data['regularMarketOpen']
        self.beta = data['beta']
        self.bookValue = data['bookValue']
        self.marketCap = data['marketCap']
        self.forwardEps = data['forwardEps']
        self.trailingEps = data['trailingEps']
        self.wk52hi = data['fiftyTwoWeekHigh']
        self.wk52lo = data['fiftyTwoWeekLow']
    def curr_price(self):
        # history = self.stk.history(period='1d', interval='1m', proxy='socks5://127.0.0.1:9050')
        # try:
        #     price = pd.Series(list(history.get('Close'))).values[-1].item()
        # except IndexError:
        #     price = 0
        # return price
        try:
            with open(f'{static_assets}/1d_1d/{self.ticker}.csv', 'r+') as csvfile:
                data = csv.reader(csvfile)
                data = list((data))
                return float(data[-1][4])
        except:
            return 1
    def volume(self):
        # history_ = self.stk.history(period='1d', interval='1d')
        # volume = pd.Series(list(history_.get('Volume'))).values
        # try:
        #     volume_numpy  =volume[0]
        #     volume_py = volume_numpy.item()
        # except IndexError:
        #     volume_py = 0
        # if math.isnan(volume_py):
        #     return 0
        # else:
        #     return volume_py
        try:
            with open(f'{static_assets}/1d_1d/{self.ticker}.csv', 'r+') as csvfile:
                data = csv.reader(csvfile)
                data = list((data))
                return float(data[-1][6])
        except:
            return 1
    def vol_avg(self, period_):
        lst = []
        with open(f'{static_assets}/1y_1d/{self.ticker}.csv') as f:
            data_ = csv.reader(f)
            data_ = list(data_)
            for i in range(1,period_+1):
                if data_[-i][-1] =='':
                    lst = [0]
                else:
                    # print(self.ticker)
                    lst.append(int(float(data_[-i][-1])))
        return sum(lst)/int(len(lst))
    def mvg(self, period,interval,range_):
        lst = []
        with open(f'{static_assets}/{period}_{interval}/{self.ticker}.csv', 'r+') as csvfile:
            data_ = csv.reader(csvfile)
            data_ = list(data_)
        for i in range(1, range_+1):
            try:
                lst.append(float(data_[-i][4]))
            except ValueError:
                lst.append(0)
        return sum(lst)/len(lst)
    
