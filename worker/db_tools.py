import os, sys, sqlite3
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'finance_front.settings'
# pro_root_dir = '/mnt/c/final/frontend/web'
pro_root_dir = "/home/sean/repos/finance_dashboard"
# db_root_dir = '/mnt/c/final/frontend/web'
db_root_dir = "/home/sean/repos/finance_dashboard"
sys.path.append(pro_root_dir)
django.setup()
from charts.models import Stocks, Portfolio
from worker.const import static_assets

# static_assets
# static_assets = "/mnt/c/final/frontend/web/static_assets"

def update_stocks(data):
    data =data
    inst = Stocks.objects.update_or_create(
        ticker= data['ticker'],
        defaults={ 'sec_code':data['isin_code'],'sector': data['sector'] , 'shares_outstanding_Cr' : data['sharesOutstanding'], 'per_vol_traded_10_day': data['per_vol_traded_10_day'] , 'dividend_yield_per':data['dividendYield'] , 'wk52hi':data['wk52hi'] , 'wk52lo':data['wk52lo'] , 'regularopen':data['regularMarketOpen'] , 'previousclose': data['previousClose'] , 'trailingeps': data['trailingEps'] , 'forwardeps':data['forwardEps'] , 'mvg_200_clo':data['mvg_200_clo'] , 'mvg_100_clo': data['mvg_100_clo'] ,'mvg_50_clo': data['mvg_50_clo'] , 'mvg_20_clo':  data['mvg_20_clo'], 'mvg_10_clo': data['mvg_10_clo'] , 'mvg_5_clo':data['mvg_5_clo'] , 'volume':data['Volume'] , 'vol_avg_10':data['vol_avg_10'] , 'current_price': data['current_price'], 'last_updated': '2021-05-22', 'rel_100_200':data['rel_100_200'] , 'rel_50_100': data['rel_50_100'], 'rel_20_50': data['rel_20_50'], 'rel_10_20': data['rel_10_20'], 'rel_52_per': data['rel_52_per'], 'p_upon_e':data['p_upon_e'] , 'market_cap':data['marketCap'] , 'book_value': data['bookValue'] , 'beta': data['beta'] ,'trailingEps_rel_price_per': data['trailingEps_rel_price_per'], 'forwardEps_rel_price_per': data['forwardEps_rel_price_per']})
    if Portfolio.objects.all().filter(ticker= data['ticker']).exists():
       p_inst = Portfolio.objects.get(ticker= data['ticker'])
       p_inst.current_price = data['current_price']
       p_inst.save()
       print('updated portfolio')
    else:
        print('not present in portflio')
    # Portfolio.objects.all().filter(ticker= data['ticker']).update(current_price=data['current_price'])
    # inst.save()
    # stk_inst = Stocks.objects.all().filter(ticker = data['ticker'])[0]
    # stk_inst.up