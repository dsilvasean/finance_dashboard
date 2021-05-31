import requests, pandas, os, shutil, pickle, json, time, threading, base64
import yfinance as yf
import concurrent.futures
from bs4 import BeautifulSoup
from worker.stock_base import Stock
import worker.db_tools as dbtools
from worker.models import worker_tracker
from worker.const import static_assets

file_name = "500_mk_cap_class"
# # static_assets = "../static/static_assets/migrate_class"
# # static_assets = "/home/sean/Desktop/repos/finance_dashboard/static/static_assets/migrate_class"
# static_assets = "/mnt/c/repos/finance_dashboard/static/static_assets/migrate_class"

class workers_():
    def __init__(self):
        worker_tracker.objects.update_or_create(
            file_or_dir_name="500_mk_cap.xlsx",
            defaults={"updating": True}
        )
        self.time_started = time.time()
        self.pickel_status = 0
        self.charts_downloaded = 0
        self.rows_updated =0
        self.proxies = proxies = {
  'socks5': 'socks5://127.0.0.1:9050',
  'http': 'socks5://127.0.0.1:9050',
  'https': 'socks5://127.0.0.1:9050'}
        self.dict_info = {}
        self.tickers_list = []
        self.isin_code = []
        self.emp_dict = {'zip': None, 'sector': None, 'fullTimeEmployees': None, 'longBusinessSummary': None, 'city': None, 'phone': None, 'country': None, 'companyOfficers': None, 'website': None, 'maxAge': None, 'address1': None, 'fax': None, 'industry': None, 'address2': None, 'previousClose': None, 'regularMarketOpen': None, 'twoHundredDayAverage': None, 'trailingAnnualDividendYield': None, 'payoutRatio': None, 'volume24Hr': None, 'regularMarketDayHigh': None, 'navPrice': None, 'averageDailyVolume10Day': None, 'totalAssets': None, 'regularMarketPreviousClose': None, 'fiftyDayAverage': None, 'trailingAnnualDividendRate': None, 'open': None, 'averageVolume10days': None, 'expireDate': None, 'yield': None, 'algorithm': None, 'dividendRate': None, 'exDividendDate': None, 'beta': None, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': None, 'priceHint': None, 'currency': None, 'trailingPE': None, 'regularMarketVolume': None, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': None, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': None, 'priceToSalesTrailing12Months': None, 'dayLow': None, 'ask': None, 'ytdReturn': None, 'askSize': None, 'volume': None, 'fiftyTwoWeekHigh': None, 'forwardPE': None, 'fromCurrency': None, 'fiveYearAvgDividendYield': None, 'fiftyTwoWeekLow': None, 'bid': None, 'tradeable': None, 'dividendYield': None, 'bidSize': None, 'dayHigh': None, 'exchange': None, 'shortName': None, 'longName': None, 'exchangeTimezoneName': None, 'exchangeTimezoneShortName': None, 'isEsgPopulated': None, 'gmtOffSetMilliseconds': None, 'underlyingSymbol': None, 'quoteType': None, 'symbol': None, 'underlyingExchangeSymbol': None, 'headSymbol': None, 'messageBoardId': None, 'uuid': None, 'market': None, 'annualHoldingsTurnover': None, 'enterpriseToRevenue': None, 'beta3Year': None, 'profitMargins': None, 'enterpriseToEbitda': None, '52WeekChange': None, 'morningStarRiskRating': None, 'forwardEps': None, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': None, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'bookValue': None, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 'lastFiscalYearEnd': None, 'heldPercentInstitutions': None, 'netIncomeToCommon': None, 'trailingEps': None, 'lastDividendValue': None, 'SandP52WeekChange': None, 'priceToBook': None, 'heldPercentInsiders': None, 'nextFiscalYearEnd': None, 'mostRecentQuarter': None, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': None, 'enterpriseValue': None, 'threeYearAverageReturn': None, 'lastSplitDate': None, 'lastSplitFactor': None, 'legalType': None, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': None, 'dateShortInterest': None, 'pegRatio': None, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'category': None, 'fiveYearAverageReturn': None, 'regularMarketPrice': None, 'logo_url': None}
        self.url = "https://static.nseindia.com//s3fs-public/inline-files/MCAP31032021_0.xlsx"
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        self.data = requests.get(self.url, headers=self.headers).content
        with open(f"{static_assets}/{file_name}.xlsx", 'wb') as xls:
            xls.write(self.data)
        xl = pandas.read_excel(f"{static_assets}/{file_name}.xlsx", header=None)
        for i in range(1,501):
            self.tickers_list.append(f"{xl[1][i]}.NS")
            self.isin_code.append(f'ISIN{i}')
        worker_tracker.objects.update_or_create(
            file_or_dir_name="500_mk_cap.xlsx",
            defaults={"updating": False}
        )
        
    def progress_(self, done):
        try:
            per = (done/len(self.tickers_list))*100
            return per
        except:
            return 'update_not_yet_started'
        # return (f"{done} out of {len(self.tickers_list)}")
    
    def proxy_is_alive(self):
        try:
            re = requests.get('https://www.google.com', proxies=self.proxies)
            return True
        except:
            return False
            
    def get_data(self, period, interval):
        dir_name = f'{static_assets}/{period}_{interval}'
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"{period}_{interval}/",
            defaults={"updating": True}
        )
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
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"{period}_{interval}/",
            defaults={"updating": False}
        )

    def mk_info_pickel(self):
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"data.json",
            defaults={"updating": True}
        )
        def exec(ticker):
            stk = yf.Ticker(ticker)
            print(ticker)
            data = stk.get_info(proxy=self.proxies['socks5'])
            data_ = {"ticker":ticker, "info_dict": data}
            return data_
        with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
            futures = (executor.submit(exec, ticker) for ticker in self.tickers_list)
            for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    data =future.result()
                except Exception as ex:
                    print(ex)
                self.pickel_status = self.pickel_status +1
                print(idx)
                self.dict_info[f"{data['ticker']}"] = data['info_dict']
        self.dict_info['NONE.NS'] = self.emp_dict
        with open(f'{static_assets}/data.p', 'wb') as fp:
            pickle.dump(self.dict_info, fp, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'{static_assets}/data.json', 'w') as js:
            json.dump(self.dict_info, js)
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"data.json",
            defaults={"updating": False}
        )
        print(f"{(time.time() - self.time_started)/ 60}")
    
    def dwnld_charts(self):
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"charts/",
            defaults={"updating": True}
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
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"charts/",
            defaults={"updating": False}
        )
    # 
    def calc__(self,d): 
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"db_update",
            defaults={"updating": True}
        )
        for i in range(0, len(self.tickers_list)):
            # if (i%40 ==0 or i%80 == 0 or i % 100 ==0 or i%150==0 or i % 200 ==0 or i % 250 ==0 or i%300 ==0 or i%350 ==0 or i%400 ==0 or i%450 ==0 or i%500 ==0):
            #     time.sleep(1)
            stk = Stock(self.tickers_list[i], self.isin_code[i])
            curr_price = stk.curr_price()
            volume = stk.volume()
            vol_10_avg = stk.vol_avg(10)
        # 
            mvg_200 = round(stk.mvg('1y','1d',200))
            mvg_100 = round(stk.mvg('1y', '1d', 100))
            mvg_50 = round(stk.mvg('1y', '1d', 50))
            mvg_20 = round(stk.mvg('1y', '1d', 20))
            mvg_10 = round(stk.mvg('1y', '1d', 10))
            mvg_5 = round(stk.mvg('1y', '1d', 5))
        # 
            # p_b_ratio = curr_price / stk.bookValue
            per_trail_eps_pri = round((stk.trailingEps/stk.regularMarketPrice)*100,2)
            per_for_eps_pri = round((stk.forwardEps/stk.regularMarketPrice)*100,2)
            per_vol_traded_10_day = round((vol_10_avg/ stk.sharesOutstanding)*100, 2)
            try:
                rel_52_p = (curr_price -  stk.wk52lo) / (stk.wk52hi - stk.wk52lo) * 100
                rel_52_p = (curr_price / stk.wk52hi) *100
                pe_ratio = stk.trailingEps/ curr_price
            except (ZeroDivisionError, TypeError):
                rel_52_p = 0
                pe_ratio = 0
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
            print(stk.__dict__)

            print(self.tickers_list[i])
            print(stk.sector)
            print(stk.mvg('1y','1d',100))
            print(f'Volume:{volume}')
            print(f'curr_price:{curr_price}')
            print(stk.__dict__)
            if d =='update':
                dbtools.update_stocks(stk.__dict__)
                self.rows_updated = self.rows_updated + 1
                # ++update_count
            else:
                dbtools.add_to_db(stk.__dict__)
            print(f'{len(self.tickers_list)- 1}')
            print(self.tickers_list)
        worker_tracker.objects.update_or_create(
            file_or_dir_name=f"db_update",
            defaults={"updating": False}
        )
        
