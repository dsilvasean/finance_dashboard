# Main packages....
import requests, os, time, datetime, shutil, zipfile, pytz , pickle, json, base64, csv, sys
import yfinance as yf
import pandas as pd
from django.utils import timezone
from yahooquery import Ticker
from bs4 import BeautifulSoup
import concurrent.futures
from pytz import timezone as pytz_timezone

if __name__ == '__main__':
    pass
else:
    from charts.models import Update_trackers
    from charts.models import Stocks, Portfolio
# from worker.const import static_assets
static_assets = "./static/static_assets"
utc_timezone = pytz_timezone('UTC')
data = {}
emp_dict = {'zip': None, 'sector': None, 'fullTimeEmployees': None, 'longBusinessSummary': None, 'city': None, 'phone': None, 'country': None, 'companyOfficers': None, 'website': None, 'maxAge': None, 'address1': None, 'fax': None, 'industry': None, 'address2': None, 'previousClose': None, 'regularMarketOpen': None, 'twoHundredDayAverage': None, 'trailingAnnualDividendYield': None, 'payoutRatio': None, 'volume24Hr': None, 'regularMarketDayHigh': None, 'navPrice': None, 'averageDailyVolume10Day': None, 'totalAssets': None, 'regularMarketPreviousClose': None, 'fiftyDayAverage': None, 'trailingAnnualDividendRate': None, 'open': None, 'averageVolume10days': None, 'expireDate': None, 'yield': None, 'algorithm': None, 'dividendRate': None, 'exDividendDate': None, 'beta': None, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': None, 'priceHint': None, 'currency': None, 'trailingPE': None, 'regularMarketVolume': None, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': None, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': None, 'priceToSalesTrailing12Months': None, 'dayLow': None, 'ask': None, 'ytdReturn': None, 'askSize': None, 'volume': None, 'fiftyTwoWeekHigh': None, 'forwardPE': None, 'fromCurrency': None, 'fiveYearAvgDividendYield': None, 'fiftyTwoWeekLow': None, 'bid': None, 'tradeable': None, 'dividendYield': None, 'bidSize': None, 'dayHigh': None, 'exchange': None, 'shortName': None, 'longName': None, 'exchangeTimezoneName': None, 'exchangeTimezoneShortName': None, 'isEsgPopulated': None, 'gmtOffSetMilliseconds': None, 'underlyingSymbol': None, 'quoteType': None, 'symbol': None, 'underlyingExchangeSymbol': None, 'headSymbol': None, 'messageBoardId': None, 'uuid': None, 'market': None, 'annualHoldingsTurnover': None, 'enterpriseToRevenue': None, 'beta3Year': None, 'profitMargins': None, 'enterpriseToEbitda': None, '52WeekChange': None, 'morningStarRiskRating': None, 'forwardEps': None, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': None, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'bookValue': None, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 'lastFiscalYearEnd': None, 'heldPercentInstitutions': None, 'netIncomeToCommon': None, 'trailingEps': None, 'lastDividendValue': None, 'SandP52WeekChange': None, 'priceToBook': None, 'heldPercentInsiders': None, 'nextFiscalYearEnd': None, 'mostRecentQuarter': None, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': None, 'enterpriseValue': None, 'threeYearAverageReturn': None, 'lastSplitDate': None, 'lastSplitFactor': None, 'legalType': None, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': None, 'dateShortInterest': None, 'pegRatio': None, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'category': None, 'fiveYearAverageReturn': None, 'regularMarketPrice': None, 'logo_url': None}
proxies = {
  'socks5': 'socks5://127.0.0.1:9050',
  'http': 'socks5://127.0.0.1:9050',
  'https': 'socks5://127.0.0.1:9050'}

def dwnldMcapTickers():
    url = "https://static.nseindia.com//s3fs-public/inline-files/MCAP31032021_0.xlsx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    with open(f"{static_assets}/MCAP31032021_0.xlsx", 'wb') as mcap:
        mcap.write(requests.get(url, headers=headers).content)

# Checks if the proxy server is alive 
def proxy_is_alive():
        try:
            re = requests.get('https://www.google.com', proxies=proxies)
            return True
        except:
            return False

def convert_to_localtime(utctime):
    fmt = '%d/%m/%Y %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

def lookup(key_,module_,field_):
    try:
        data_ = data[key_][module_][field_]
        return data_
    except :
        return None

def lookup_(dict_, field_):
    try:
        data_ = dict_[field_]
        if data_ == None or data_ == 'null':
            data_ = 0
    except KeyError:
        data_ = 0
    return data_

def update_stocks(data):
    data = data
    inst = Stocks.objects.update_or_create(
        ticker= data['ticker'],
        defaults={ 'sec_code':data['isin_code'],'sector': data['sector'] , 'shares_outstanding_Cr' : data['sharesOutstanding'], 'per_vol_traded_10_day': data['per_vol_traded_10_day'] , 'dividend_yield_per':data['dividendYield'] , 'wk52hi':data['wk52hi'] , 'wk52lo':data['wk52lo'] , 'regularopen':data['regularMarketOpen'] , 'previousclose': data['previousClose'] , 'trailingeps': data['trailingEps'] , 'forwardeps':data['forwardEps'] , 'mvg_200_clo':data['mvg_200_clo'] , 'mvg_100_clo': data['mvg_100_clo'] ,'mvg_50_clo': data['mvg_50_clo'] , 'mvg_20_clo':  data['mvg_20_clo'], 'mvg_10_clo': data['mvg_10_clo'] , 'mvg_5_clo':data['mvg_5_clo'] , 'volume':data['Volume'] , 'vol_avg_10':data['vol_avg_10'] , 'current_price': data['current_price'], 'last_updated': '2021-05-22', 'rel_100_200':data['rel_100_200'] , 'rel_50_100': data['rel_50_100'], 'rel_20_50': data['rel_20_50'], 'rel_10_20': data['rel_10_20'], 'rel_52_per': data['rel_52_per'], 'p_upon_e':data['p_upon_e'] , 'market_cap':data['marketCap'] , 'book_value': data['bookValue'] , 'beta': data['beta'] ,'trailingEps_rel_price_per': data['trailingEps_rel_price_per'], 'forwardEps_rel_price_per': data['forwardEps_rel_price_per']})
    if Portfolio.objects.all().filter(ticker=data['ticker']).exists():
        p_inst = Portfolio.objects.get(ticker=data['ticker'])
        p_inst.current_price = data['current_price']
        p_inst.save()
        print('updatd Portfolio')
    else:
        print('Not present in portfolio...')
class Stock():
    def __init__(self, ticker, isin_code):
        self.ticker = ticker
        self.isin_code = isin_code
        with open(f"{static_assets}/query_1.json", 'r') as json_file:
            data_ = json.load(json_file)
            # print(data_)
        try:
            data = data_[self.ticker]
            # print(data)
        except KeyError:
            print(ticker)
            print('exception......')
            data = emp_dict
        self.sector = lookup_(data,'sector')
        self.dividendYield = lookup_(data, 'dividendYield')
        self.beta = lookup_(data,'beta')
        self.bookValue = lookup_(data,'bookValue')
        self.forwardEps = lookup_(data,'forwardEps')
        self.trailingEps = lookup_(data,'trailingEps')
        self.sharesOutstanding = lookup_(data, 'sharesOutstanding')
        self.regularMarketPrice = lookup_(data, 'regularMarketPrice')
        self.previousClose  = lookup_(data,'previousClose')
        self.regularMarketOpen = lookup_(data, "regularMarketOpen")
        self.marketCap = lookup_(data, 'marketCap')
        self.wk52hi = lookup_(data,'wk52hi')
        self.wk52lo = lookup_(data,'wk52lo')
        # print(data)
    def current_price(self):
        try:
            with open(f'{static_assets}/max_1d/{self.ticker}.csv', 'r+') as csvfile:
                data = csv.reader(csvfile)
                data = list((data))
                if float(data[-1][4]) == 0.0:
                    return 1
                else:
                    return float(data[-1][4])
        except:
            return 1
    def volume(self):
        try:
            with open(f'{static_assets}/max_1d/{self.ticker}.csv', 'r+') as csvfile:
                data = csv.reader(csvfile)
                data = list((data))
                return float(data[-1][6])
        except:
            return 1
    def vol_avg(self, period_):
        lst = []
        try:
            with open(f'{static_assets}/max_1d/{self.ticker}.csv') as f:
                data_ = csv.reader(f)
                data_ = list(data_)
                for i in range(1,period_+1):
                    if data_[-i][-1] =='':
                        lst = [0]
                    else:
                        # print(self.ticker)
                        lst.append(int(float(data_[-i][-1])))
            return sum(lst)/int(len(lst))
        except:
            return 1
    def mvg(self,range_):
        # print(f"**************{self.ticker}")
        lst = []
        with open(f'{static_assets}/max_1d/{self.ticker}.csv', 'r+') as csvfile:
            data_ = csv.reader(csvfile)
            data_ = list(data_)
        for i in range(1, range_+1):
            try:
                # print(lst)
                lst.append(float(data_[-i][4]))
            except (ValueError, IndexError):
                # lst.append(0)
                return 0
        return sum(lst)/len(lst)


class workers_():
    def __init__(self):
        self.max_update_running = None
        self.max_update_now = None
        self.total_entries = 600
        self.total_no_ = 0
        self.done__ = 0
        self.time_started = time.time()
        self.pickel_status = 0
        self.charts_downloaded = 0
        self.rows_updated =0
        self.days_to_fetch = []
        # self.time_now =timezone.now()
        self.time_now = datetime.datetime.now()
        self.proxies = proxies = {
  'socks5': 'socks5://127.0.0.1:9050',
  'http': 'socks5://127.0.0.1:9050',
  'https': 'socks5://127.0.0.1:9050'}
        self.dict_info = {}
        self.tickers_list = []
        self.isin_code = []
        self.emp_dict = {'zip': None, 'sector': None, 'fullTimeEmployees': None, 'longBusinessSummary': None, 'city': None, 'phone': None, 'country': None, 'companyOfficers': None, 'website': None, 'maxAge': None, 'address1': None, 'fax': None, 'industry': None, 'address2': None, 'previousClose': None, 'regularMarketOpen': None, 'twoHundredDayAverage': None, 'trailingAnnualDividendYield': None, 'payoutRatio': None, 'volume24Hr': None, 'regularMarketDayHigh': None, 'navPrice': None, 'averageDailyVolume10Day': None, 'totalAssets': None, 'regularMarketPreviousClose': None, 'fiftyDayAverage': None, 'trailingAnnualDividendRate': None, 'open': None, 'averageVolume10days': None, 'expireDate': None, 'yield': None, 'algorithm': None, 'dividendRate': None, 'exDividendDate': None, 'beta': None, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': None, 'priceHint': None, 'currency': None, 'trailingPE': None, 'regularMarketVolume': None, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': None, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': None, 'priceToSalesTrailing12Months': None, 'dayLow': None, 'ask': None, 'ytdReturn': None, 'askSize': None, 'volume': None, 'fiftyTwoWeekHigh': None, 'forwardPE': None, 'fromCurrency': None, 'fiveYearAvgDividendYield': None, 'fiftyTwoWeekLow': None, 'bid': None, 'tradeable': None, 'dividendYield': None, 'bidSize': None, 'dayHigh': None, 'exchange': None, 'shortName': None, 'longName': None, 'exchangeTimezoneName': None, 'exchangeTimezoneShortName': None, 'isEsgPopulated': None, 'gmtOffSetMilliseconds': None, 'underlyingSymbol': None, 'quoteType': None, 'symbol': None, 'underlyingExchangeSymbol': None, 'headSymbol': None, 'messageBoardId': None, 'uuid': None, 'market': None, 'annualHoldingsTurnover': None, 'enterpriseToRevenue': None, 'beta3Year': None, 'profitMargins': None, 'enterpriseToEbitda': None, '52WeekChange': None, 'morningStarRiskRating': None, 'forwardEps': None, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': None, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'bookValue': None, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 'lastFiscalYearEnd': None, 'heldPercentInstitutions': None, 'netIncomeToCommon': None, 'trailingEps': None, 'lastDividendValue': None, 'SandP52WeekChange': None, 'priceToBook': None, 'heldPercentInsiders': None, 'nextFiscalYearEnd': None, 'mostRecentQuarter': None, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': None, 'enterpriseValue': None, 'threeYearAverageReturn': None, 'lastSplitDate': None, 'lastSplitFactor': None, 'legalType': None, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': None, 'dateShortInterest': None, 'pegRatio': None, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'category': None, 'fiveYearAverageReturn': None, 'regularMarketPrice': None, 'logo_url': None}
        xl = pd.read_excel(f"{static_assets}/MCAP31032021_0.xlsx", header=None)
        for i in range(1,self.total_entries):
            self.tickers_list.append(f"{xl[1][i]}.NS")
            self.isin_code.append(f'ISIN{i}')
        print(self.tickers_list)

    # For downloading historical data....
    def get_data(self, period, interval):
        dir_name = f'{static_assets}/{period}_{interval}'
        # Update_trackers.objects.update_or_create(
        #     file_or_dir_name=f"{period}_{interval}/",
        #     defaults={"updating": True, "updated_at": datetime.datetime.now()}
        # )
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        data = yf.download(
        tickers = self.tickers_list,
        period=period,
        interval=interval,
        group_by='ticker',
        auto_adjust=False, 
        prepost=False,
        threads= 4, 
        proxy='socks5://127.0.0.1:9050',
        # proxy=None
    )
        data =data.T
        for ticker in self.tickers_list:
            data.loc[(ticker,),].T.to_csv(f'{static_assets}/{period}_{interval}/{ticker}.csv', sep=',', encoding='utf-8')
        # Update_trackers.objects.update_or_create(
        #     file_or_dir_name=f"{period}_{interval}/",
        #     defaults={"updating": False}
        # )
    def progress_debug(self):
        data_to_return = {
            'total_entries' : self.total_entries,
            'historical': {
                'historical_now_updating': self.max_update_now,
                'max_update_running': self.max_update_running
            },
            'statsUpdate':{
                'msg':'coming soon..'
            },
            'chartsUpdate':{
                'msg': 'coming soon..'
            },
            'updateRows': 'coming soon..'
        }
        return data_to_return
    # Updating max_1d using bhavcopy....  its a mess but works 
    def update_max_data(self):
        self.max_update_running = True
        with open(f"{static_assets}/max_1d/RELIANCE.NS.csv", 'r') as f:
            data_ = csv.reader(f)
            rows_ = [row for row in data_]
            last_updated_on = rows_[-1][0]
        try:
            last_updated_on = datetime.datetime.strptime(last_updated_on,"%d-%b-%Y")
        except:
            last_updated_on = datetime.datetime.strptime(last_updated_on,"%Y-%m-%d")
        # last_updated_on = Update_trackers.objects.get(file_or_dir_name='max_1d/')
        # last_updated_on = getattr(last_updated_on, 'updated_at')
        print(last_updated_on)
        # last_updated_on = last_updated_on.replace(tzinfo=None)
        # print(self.time_now.hour)
        if int(convert_to_localtime(timezone.now())[11:13]) >= 18:     
            days_to_fetch = pd.date_range(last_updated_on + datetime.timedelta(days=1), self.time_now, freq='B')
        else:
            days_to_fetch = pd.date_range(last_updated_on + datetime.timedelta(days=1), self.time_now - datetime.timedelta(days=1), freq='B')
            print('asas')
        print(len(days_to_fetch))
        if len(days_to_fetch) == 0:
            print(f'{last_updated_on}assdfrgrgrtgktk')
            self.max_update_now = last_updated_on.strftime('%d, %m, %y')
        if len(days_to_fetch) == 0:
            self.max_update_running = False
            return 'already up to date'
        self.total_no_ = len(days_to_fetch) * len(self.tickers_list)
        print(f'sasasadsdfggjghjfg{len(days_to_fetch)}')
        for date in days_to_fetch:
            month_ = date.strftime("%b").upper()
            day_ = date.strftime("%d")
            year_ = date.year
            self.max_update_now = f"{day_}/{month_}/{year_}"
            file_name = f"bhavcopy{day_}{month_}{year_}"
            # print(day_)
            url =  f"https://archives.nseindia.com/content/historical/EQUITIES/{year_}/{month_}/cm{day_}{month_}{year_}bhav.csv.zip"
            print(f"updating for {day_} using {url}")
            # print(time_now.hour)
            data = requests.get(url).content
            with open(f"{static_assets}/bhavcopy/temp/{file_name}.csv.zip", 'wb') as f:
                f.write(data)
            with zipfile.ZipFile(f'{static_assets}/bhavcopy/temp/{file_name}.csv.zip', "r") as zip:
                zip.extractall(f"{static_assets}/bhavcopy")
                os.remove(f'{static_assets}/bhavcopy/temp/{file_name}.csv.zip')
            for ticker in self.tickers_list:
                print(f"now appending to {ticker}")
                cols_to_get = ['TIMESTAMP','OPEN', 'HIGH', 'LOW', 'CLOSE', 'PREVCLOSE', 'TOTTRDQTY']
                to_append = f""
                with open(f"{static_assets}/bhavcopy/cm{day_}{month_}{year_}bhav.csv", 'r') as bhavcopy:
                    df = pd.read_csv(bhavcopy)
                    for col in cols_to_get:
                        try:
                            dat_ = df.loc[df['SYMBOL'] == ticker.replace('.NS', '')][col].iloc[0]
                        except IndexError:
                            dat_ = 0
                        if col == "TOTTRDQTY":
                            to_append = to_append + str(dat_) + "\n"
                        else:
                            to_append = to_append + str(dat_) + ','
                # print(to_append)
                with open(f'{static_assets}/max_1d/{ticker}.csv', 'a') as f:
                    f.write(to_append)
                self.done__ = self.done__ + (len(days_to_fetch) * 1)
        Update_trackers.objects.update_or_create(
            file_or_dir_name=f"max_1d/",
            defaults={"updating": False, "updated_at": timezone.now()}
        )
        self.max_update_running = False
        return 'updated......'
    # 
    def yquery(self):
        with open(f'{static_assets}/query_1.json', 'r+') as f:
            last_updated = json.load(f)['RELIANCE.NS']['last_updated']
        if last_updated == datetime.datetime.now().strftime('%d-%m-%y'):
            print('already up to date')
            return 'already up to date'
        else:
            print(last_updated)
            print(f'sdasd{self.tickers_list}')
            global data
            data_to_json ={}
            tickers = Ticker(self.tickers_list, asynchronous=True, progress=True, proxies={"http":"socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"})
            data = tickers.get_modules(['assetProfile', 'summaryDetail', 'defaultKeyStatistics', 'price'])
            time.sleep(2)
            for key in data.keys():
                data_ = {
                    'sector':lookup(key, 'assetProfile', 'sector'),
                    'dividendYield':lookup(key, 'summaryDetail', 'dividendYield'),
                    'beta':lookup(key, 'defaultKeyStatistics', 'beta'),
                    'bookValue':lookup(key,'defaultKeyStatistics','bookValue'), 
                    'forwardEps': lookup(key, 'defaultKeyStatistics', 'forwardEps'),
                    'trailingEps':lookup(key,'defaultKeyStatistics', 'trailingEps'),
                    'sharesOutstanding':lookup(key, 'defaultKeyStatistics', 'sharesOutstanding'),
                    'regularMarketPrice':lookup(key,'price', 'regularMarketPrice'),
                    'previousClose':lookup(key,'summaryDetail', 'previousClose'),
                    'regularMarketOpen':lookup(key,'summaryDetail','regularMarketOpen'),
                    'marketCap':lookup(key,'summaryDetail', 'marketCap'),
                    'wk52hi':lookup(key,'summaryDetail','fiftyTwoWeekHigh'),
                    'wk52lo':lookup(key,'summaryDetail','fiftyTwoWeekLow'),
                    'last_updated':datetime.datetime.now().strftime('%d-%m-%y')
                }
                data_to_json[key] = data_
                # print(key, data_)
            with open(f'{static_assets}/query_1.json', 'w') as f:
                json.dump(data_to_json, f)
            return 'updated....'
            print('updated...')

    def dwnld_charts(self):
        utc_timezone = pytz_timezone('UTC')
        utc_time = datetime.datetime.now(utc_timezone)
        print(f"{utc_time},--{Update_trackers.objects.get(file_or_dir_name='charts/').updated_at.day}")
        if utc_time.day == Update_trackers.objects.get(file_or_dir_name="charts/").updated_at.day:
            print('updated_today')
            return 'last updated: today'
        else:
            Update_trackers.objects.update_or_create(
                file_or_dir_name=f"charts/",
                defaults={"updating": True, 'updated_at': datetime.datetime.now()}
            )
            def make_req(ticker):
                print(ticker)
                ticker =ticker[:-3]
                url = f"https://chartink.com/raw/chartdisplay.php?v=o&t=d&E=1&E2=1&h=1&l=0&vg=1&y=1&s=0&w=0&c1=RSI%7EOBV%7ECOscillator%7E&c2=14%7En/a%7En/a%7E&a1=1&a1t=c&a1v=SMA&a1l=50&a2=1&a2t=c&a2v=SMA&a2l=100&a3l=15&a4l=20&a5l=28&ti=5000&d=d&c=s&A={ticker}&width=1127&is_premium=false&user_id=0"
                resp = requests.get(url, proxies=self.proxies).text
                soup_ = BeautifulSoup(resp, 'lxml')
                encoded_img_ = soup_.find('img')['src'][23:]
                _data ={'ticker':f'{ticker}.NS',
                'b64d':encoded_img_}
                return _data
            with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
                futures = (executor.submit(make_req, ticker) for ticker in self.tickers_list)
                print('teee')
                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(f"exc_here {exc}")
                    print(idx)
                    self.charts_downloaded = self.charts_downloaded + 1
                    with open(f'{static_assets}/charts/{data["ticker"]}.png', 'wb') as f:
                        f.write(base64.b64decode(data['b64d']))
            Update_trackers.objects.update_or_create(
                file_or_dir_name=f"charts/",
                defaults={"updating": False}
            )
            return 'Downloaded all'
    def update_rows(self, d):
        utc_timezone = pytz_timezone('UTC')
        utc_time = datetime.datetime.now(utc_timezone)
        if utc_time.day == Update_trackers.objects.get(file_or_dir_name="db_update").updated_at.day:
            return 'database was already updated today'
        else:
            Update_trackers.objects.update_or_create(
                file_or_dir_name=f"db_update",
                defaults={"updating": True, "updated_at": datetime.datetime.now()}
            )
            for i in range(0, len(self.tickers_list)):
                stk = Stock(self.tickers_list[i], 'ISIN001')
                if self.tickers_list[i] == "ICICIBANK.NS":
                    print(stk)
                curr_price = stk.current_price()
                volume = stk.volume()
                vol_10_avg = stk.vol_avg(10)
                # 
                mvg_200 = round(stk.mvg(200))
                mvg_100 = round(stk.mvg(100))
                mvg_50 = round(stk.mvg(50))
                mvg_20 = round(stk.mvg(20))
                mvg_10 = round(stk.mvg(10))
                mvg_5 = round(stk.mvg(5))
                # 
                # p_b_ratio = curr_price / stk.bookValue
                per_trail_eps_pri = round((stk.trailingEps/stk.regularMarketPrice)*100,2)
                per_for_eps_pri = round((stk.forwardEps/stk.regularMarketPrice)*100,2)
                per_vol_traded_10_day = round((vol_10_avg/ stk.sharesOutstanding)*100, 2)
                # 
                try:
                    rel_52_p = (curr_price -  stk.wk52lo) / (stk.wk52hi - stk.wk52lo) * 100
                    rel_52_p = (curr_price / stk.wk52hi) *100
                    pe_ratio = stk.trailingEps/ curr_price
                except (ZeroDivisionError, TypeError):
                    rel_52_p = 0
                    pe_ratio = 0
                # 
                stk.__dict__['mvg_200_clo'] = str(mvg_200)
                stk.__dict__['mvg_100_clo'] = str(mvg_100)
                stk.__dict__['mvg_50_clo'] = str(mvg_50)
                stk.__dict__['mvg_20_clo'] = str(mvg_20)
                stk.__dict__['mvg_10_clo'] = str(mvg_10) 
                stk.__dict__['mvg_5_clo'] = str(mvg_5)
                stk.__dict__['Volume'] = volume
                stk.__dict__['vol_avg_10'] = vol_10_avg
                stk.__dict__['current_price'] = curr_price
                stk.__dict__['last_updated'] = time.ctime()
                stk.__dict__['trailingEps_rel_price_per'] = per_trail_eps_pri
                stk.__dict__['forwardEps_rel_price_per'] = per_for_eps_pri
                stk.__dict__['per_vol_traded_10_day'] = per_vol_traded_10_day
                stk.__dict__['sharesOutstanding'] = stk.sharesOutstanding
                try:
                    stk.__dict__['rel_100_200'] = str(round(((mvg_100 / mvg_200) - 1)*100, 2))
                    stk.__dict__['rel_50_100'] = str(round(((mvg_50 / mvg_100) - 1)*100, 2))
                    stk.__dict__['rel_20_50'] = str(round(((mvg_20 / mvg_50) - 1)*100, 2))
                    stk.__dict__['rel_10_20'] = str(round(((mvg_10 / mvg_20) - 1)*100, 2))
                    print(f"rel_10_20{str(round(((mvg_10 / mvg_20) - 1)*100, 2))}")
                except ZeroDivisionError:
                    stk.__dict__['rel_100_200'] =  0
                    stk.__dict__['rel_50_100'] = 0
                    stk.__dict__['rel_20_50'] = 0
                    stk.__dict__['rel_10_20'] = 0
                stk.__dict__['rel_52_per'] = rel_52_p
                stk.__dict__['p_upon_e'] = pe_ratio
                # stk.__dict__.pop('stk')
                # print(stk.__dict__)

                print(self.tickers_list[i])
                print(stk.sector)
                print(stk.mvg(100))
                print(f'Volume:{volume}')
                print(f'curr_price:{curr_price}')
                # print(stk.__dict__)
                if d =='update':
                    update_stocks(stk.__dict__)
                    self.rows_updated = self.rows_updated + 1
                    # ++update_count
                else:
                    pass
                print(f'{len(self.tickers_list)- 1}')
                # print(self.tickers_list)
            Update_trackers.objects.update_or_create(
                file_or_dir_name=f"db_update",
                defaults={"updating": False}
            )
            return 'Updated rows.....'
        # /////
# inst = workers_()
# inst.yquery()
# inst.update_max_data()
# stk = Stock('ICICIBANK.NS', 'ADDFG')
# inst =  workers_()
