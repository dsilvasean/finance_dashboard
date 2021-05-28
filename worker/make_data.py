#python script to get data
import enum
import time, requests, csv, shutil, os, pickle, json, concurrent.futures
import yfinance as yf
import base64
from bs4 import BeautifulSoup
from yfinance.utils import empty_df

if __name__ == "__main__":
    from stock_base import Stock
    import db_tools as dbtools
    from .const import static_assets
else:
    from worker.stock_base import Stock
    import worker.db_tools as dbtools
    from worker.const import static_assets
# Global variables
time_started = time.time()
c =0
ticker_list =[]
isin_code = []
dict_info ={}
string_tickers = ''
update_count = 0
pickel_status = 0
downloading_data = False
charts_got = 0
proxies = {
  'socks5': 'socks5://127.0.0.1:9050',
  'http': 'socks5://127.0.0.1:9050',
  'https': 'socks5://127.0.0.1:9050'
}

# static_assets
# static_assets = "/mnt/c/final/frontend/web/static/static_assets"

# m_time = int(os.stat(f'{static_assets}/500.csv').st_mtime)
# print(time.strftime('%Y-%m-%d', time.localtime(m_time)))

# def proxy_status():

def dwnld_500csv():
    global c, limit, ticker_list
    ticker_list.clear()
    isin_code.clear()
    data = requests.get('https://www1.nseindia.com/content/indices/ind_nifty500list.csv').text.strip('\n')
    data_ = ''
    splitted = data.split('\r')
    for split in splitted:
        data_ += split 
    with open(f'{static_assets}/500.csv', 'w+') as f:
        f.write(data_)
    #------ append to gloabl variables
    with open(f'{static_assets}/500.csv', 'r+') as f:
        spamreader = csv.reader(f)
        for row in spamreader:
            ticker_list.append(f'{row[2]}.NS')
            isin_code.append(f'{row[4]}')
    ticker_list.remove('Symbol.NS')
    isin_code.remove('ISIN Code')
    ticker_list = sorted(ticker_list)
    # del ticker_list[1:490]
    # del isin_code[1:490]
    # del ticker_list[5:40]
    print('got...')
    # print(len(ticker_list))
    # print(ticker_list)
    # print(len(ticker_list))
    time.sleep(5)

# Downloading data....
def get_data(period, interval):
    global downloading_data
    downloading_data = True
    dir_name = f'{static_assets}/{period}_{interval}'
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    data = yf.download(
        tickers = ticker_list,
        period=period,
        interval=interval,
        group_by='ticker',
        auto_adjust=False, 
        prepost=False,
        threads= 4, 
        # proxy='socks5://127.0.0.1:9050',
        proxy=None
    )
    data =data.T
    print(data)
    for ticker in ticker_list:
        data.loc[(ticker,),].T.to_csv(f'{static_assets}/{period}_{interval}/{ticker}.csv', sep=',', encoding='utf-8')
    downloading_data = False
    # time.sleep(1.5)

def mk_info_pickel():
    global pickel_status
    emp_dict = {'zip': '0', 'sector': '0', 'fullTimeEmployees': '0', 'longBusinessSummary': '0', 'city': '0', 'phone': '0', 'country': '0', 'companyOfficers': '0', 'website': '0', 'maxAge': '0', 'address1': '0', 'fax': '0', 'industry': '0', 'address2': '0', 'previousClose': '0', 'regularMarketOpen': '0', 'twoHundredDayAverage': '0', 'trailingAnnualDividendYield': '0', 'payoutRatio': '0', 'volume24Hr': '0', 'regularMarketDayHigh': '0', 'navPrice': '0', 'averageDailyVolume10Day': '0', 'totalAssets': '0', 'regularMarketPreviousClose': '0', 'fiftyDayAverage': '0', 'trailingAnnualDividendRate': '0', 'open': '0', 'averageVolume10days': '0', 'expireDate': '0', 'yield': '0', 'algorithm': '0', 'dividendRate': '0', 'exDividendDate': '0', 'beta': '0', 'circulatingSupply': '0', 'startDate': '0', 'regularMarketDayLow': '0', 'priceHint': '0', 'currency': '0', 'trailingPE': '0', 'regularMarketVolume': '0', 'lastMarket': '0', 'maxSupply': '0', 'openInterest': '0', 'marketCap': '0', 'volumeAllCurrencies': '0', 'strikePrice': '0', 'averageVolume': '0', 'priceToSalesTrailing12Months': '0', 'dayLow': '0', 'ask': '0', 'ytdReturn': '0', 'askSize': '0', 'volume': '0', 'fiftyTwoWeekHigh': '0', 'forwardPE': '0', 'fromCurrency': '0', 'fiveYearAvgDividendYield': '0', 'fiftyTwoWeekLow': '0', 'bid': '0', 'tradeable': '0', 'dividendYield': '0', 'bidSize': '0', 'dayHigh': '0', 'exchange': '0', 'shortName': '0', 'longName': '0', 'exchangeTimezoneName': '0', 'exchangeTimezoneShortName': '0', 'isEsgPopulated': '0', 'gmtOffSetMilliseconds': '0', 'underlyingSymbol': '0', 'quoteType': '0', 'symbol': '0', 'underlyingExchangeSymbol': '0', 'headSymbol': '0', 'messageBoardId': '0', 'uuid': '0', 'market': '0', 'annualHoldingsTurnover': '0', 'enterpriseToRevenue': '0', 'beta3Year': '0', 'profitMargins': '0', 'enterpriseToEbitda': '0', '52WeekChange': '0', 'morningStarRiskRating': '0', 'forwardEps': '0', 'revenueQuarterlyGrowth': '0', 'sharesOutstanding': '0', 'fundInceptionDate': '0', 'annualReportExpenseRatio': '0', 'bookValue': '0', 'sharesShort': '0', 'sharesPercentSharesOut': '0', 'fundFamily': '0', 'lastFiscalYearEnd': '0', 'heldPercentInstitutions': '0', 'netIncomeToCommon': '0', 'trailingEps': '0', 'lastDividendValue': '0', 'SandP52WeekChange': '0', 'priceToBook': '0', 'heldPercentInsiders': '0', 'nextFiscalYearEnd': '0', 'mostRecentQuarter': '0', 'shortRatio': '0', 'sharesShortPreviousMonthDate': '0', 'floatShares': '0', 'enterpriseValue': '0', 'threeYearAverageReturn': '0', 'lastSplitDate': '0', 'lastSplitFactor': '0', 'legalType': '0', 'morningStarOverallRating': '0', 'earningsQuarterlyGrowth': '0', 'dateShortInterest': '0', 'pegRatio': '0', 'lastCapGain': '0', 'shortPercentOfFloat': '0', 'sharesShortPriorMonth': '0', 'category': '0', 'fiveYearAverageReturn': '0', 'regularMarketPrice': '0', 'logo_url': '0'}
    def exec(ticker):
        stk = yf.Ticker(ticker)
        print(ticker)
        data = stk.get_info(proxy="socks5://127.0.0.1:9050")
        data_ = {"ticker": ticker, "info_dict": data}
        return data_
    with concurrent.futures.ThreadPoolExecutor(max_workers=210) as executor:
        futures = (executor.submit(exec, ticker) for ticker in ticker_list)
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                data =future.result()
            except Exception as ex:
                print(ex)
            pickel_status = pickel_status +1
            print(idx)
            dict_info[f"{data['ticker']}"] = data['info_dict']
    dict_info['NONE.NS'] = emp_dict
    with open(f'{static_assets}/data.p', 'wb') as fp:
        pickle.dump(dict_info, fp, protocol=pickle.HIGHEST_PROTOCOL)
    with open(f'{static_assets}/data.json', 'w') as js:
        json.dump(dict_info, js)
    print(f"{(time.time() - time_started)/ 60}")

def pick_progress(out_of):
    global pickel_status
    try:
        completed_percent = (pickel_status/ out_of) *100
    except:
        return "mk_pickel_not_yet_started"
    return completed_percent

def progress(out_of):
    global update_count
    try:
        completed_percent = (update_count/ out_of) *100
    except:
        return 'update_not_yet_started'
    return completed_percent

def progress_(item_, out_of):
    global pickel_status
    global update_count
    global charts_got
    try:
        completed_percent = (item_/ out_of) *100
    except:
       return 'update_not_yet_started'

def charts_progress(out_of):
    global charts_got
    try:
        completed_percent = (charts_got/ out_of) *100
    except:
       return 'update_not_yet_started'
    return completed_percent



def dwn_status():
    return downloading_data

def proxy_is_alive():
    try:
        data = requests.get('http://icanhazip.com', proxies=proxies).text
        return True
    except Exception as e:
        print(e)
        return False

def dwnld_charts():
    global charts_got
    print('charts init')
    def make_req(ticker):
        global charts_got
        print(ticker)
        ticker =ticker[:-3]
        url = f"https://chartink.com/raw/chartdisplay.php?v=o&t=d&E=1&E2=1&h=1&l=0&vg=1&y=1&s=0&w=0&c1=RSI%7EOBV%7ECOscillator%7E&c2=14%7En/a%7En/a%7E&a1=1&a1t=c&a1v=SMA&a1l=50&a2=1&a2t=c&a2v=SMA&a2l=100&a3l=15&a4l=20&a5l=28&ti=5000&d=d&c=s&A={ticker}&width=1127&is_premium=false&user_id=0"
        resp = requests.get(url, proxies=proxies).text
        soup_ = BeautifulSoup(resp, 'lxml')
        encoded_img_ = soup_.find('img')['src'][23:]
        _data ={'ticker':f'{ticker}.NS',
        'b64d':encoded_img_}
        charts_got = charts_got +1
        return _data
        # Uses threadding 
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        print('some')
        futures = (executor.submit(make_req, ticker) for ticker in ticker_list)
        print('teee')
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                data = future.result()
            except Exception as exc:
                print(exc)
            print(idx)
            with open(f'{static_assets}/charts/{data["ticker"]}.png', 'wb') as f:
                f.write(base64.b64decode(data['b64d']))

def calc__(d):
    # get_data('1y', '1d')
    # get_data('1d', '1d')
    # mk_info_pickel()
    # get_data('1y','1d')
    global update_count 
    for i in range(0, len(ticker_list)):
        # if (i%40 ==0 or i%80 == 0 or i % 100 ==0 or i%150==0 or i % 200 ==0 or i % 250 ==0 or i%300 ==0 or i%350 ==0 or i%400 ==0 or i%450 ==0 or i%500 ==0):
        #     time.sleep(1)
        stk = Stock(ticker_list[i], isin_code[i])
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
        stk.__dict__.pop('stk')
        print(stk.__dict__)

        print(ticker_list[i])
        print(stk.sector)
        print(stk.mvg('1y','1d',100))
        print(f'Volume:{volume}')
        print(f'curr_price:{curr_price}')
        print(stk.__dict__)
        if d =='update':
            dbtools.update_stocks(stk.__dict__)
            ++update_count
        else:
            dbtools.add_to_db(stk.__dict__)
        print(f'{len(ticker_list)- 1}')
        print(ticker_list)
        # print(f'update_count: {i}')
        update_count = i
        # print(progress(len(ticker_list)-1))

            # print((time.time() - time_stated))

# dwnld_500csv()
# get_data('1y', '1d')
# get_data('1d', '1d')
# mk_info_pickel()
# for i in range(0, 20):
#     print(pickel_status(len(ticker_list)))
#     time.sleep(5)
# calc__('update')
# dwnld_charts()
# proxy_is_alive()