# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
import os, sys
import portfolio.models
# from common.myScript2 import own_
# common_root = '/mnt/c/final/frontend/web/common/'
# sys.path.append(common_root)
# import test as tt
# import myScript as tt
# from portfolio.models import Stock_test
class InfoDict(models.Model):
    ticker = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)
    beta = models.FloatField()
    bookvalue = models.FloatField(db_column='bookValue')  # Field name made lowercase.
    previousclose = models.FloatField(db_column='previousClose')  # Field name made lowercase.
    regularmarketopen = models.FloatField(db_column='regularMarketOpen')  # Field name made lowercase.
    marketcap = models.IntegerField(db_column='marketCap')  # Field name made lowercase.
    forwardeps = models.FloatField(db_column='forwardEps')  # Field name made lowercase.
    trailingeps = models.FloatField(db_column='trailingEps')  # Field name made lowercase.
    wk52hi = models.FloatField()
    wk52lo = models.FloatField()

    def __str__(self):
        return str(self.ticker)
    class Meta:
        managed = True
        db_table = 'info_dict_'


class Stocks(models.Model):
    ticker = models.CharField(primary_key=True, max_length=280)
    sec_code = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)
    shares_outstanding_Cr = models.IntegerField(default=1) 
    per_vol_traded_10_day = models.FloatField(blank=True, null=True)
    dividend_yield_per = models.FloatField(blank=True, null=True, help_text='incase none default is 1')
    wk52hi = models.FloatField(blank=True, null=True)
    wk52lo = models.FloatField(blank=True, null=True)
    regularopen = models.FloatField(default = 1,db_column='regularOpen', blank=True, null=True)  # Field name made lowercase.
    previousclose = models.FloatField(db_column='previousClose', blank=True, null=True)  # Field name made lowercase.
    trailingeps = models.FloatField(default = 1,db_column='trailingEps', blank=True, null=True)  # Field name made lowercase.
    forwardeps = models.FloatField(help_text= 'in case none default is 1', default=1, db_column='forwardEps', blank=True, null=True)  # Field name made lowercase.
    mvg_200_clo = models.FloatField(blank=True, null=True)
    mvg_100_clo = models.FloatField(blank=True, null=True)
    mvg_50_clo = models.FloatField(blank=True, null=True)
    mvg_20_clo = models.FloatField(blank=True, null=True)
    mvg_10_clo = models.FloatField(blank=True, null=True)
    mvg_5_clo = models.FloatField(blank=True, null=True)
    volume = models.FloatField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.
    vol_avg_10 = models.FloatField(blank=True, null=True)
    current_price = models.FloatField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    rel_100_200 = models.FloatField(blank=True, null=True)
    rel_50_100 = models.FloatField(blank=True, null=True)
    rel_20_50 = models.FloatField(blank=True, null=True)
    rel_10_20 = models.FloatField(blank=True, null=True)
    rel_52_per = models.FloatField(blank=True, null=True)
    p_upon_e = models.FloatField(blank=True, null=True)
    market_cap = models.IntegerField(blank=True, null= True)
    book_value = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    owned = models.BooleanField(default=False)
    trailingEps_rel_price_per = models.FloatField(blank=True, null=True)
    forwardEps_rel_price_per = models.FloatField(blank=True, null=True)
    price_bk_ratio = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # if self.owned ==True:
        #     return ''
            # Stock_test.objects.update_or_create(owned=True, no_of_shares=1, buy_price=self.current_price, buy_date=timezone.now(), amt_invested=1, current_val=1, gain_or_loss=1,  defaults={
            #     'current_price': self.current_price,
            #     'ticker':self.ticker
            # })         
        self.per_vol_traded = (self.volume / self.shares_outstanding_Cr)*100
        self.trailingEps_rel_price_per = (self.trailingeps/ self.current_price)*100
        self.forwardEps_rel_price_per = (self.forwardeps /  self.current_price)*100
        self.price_bk_ratio = (self.current_price / self.book_value)
        super(Stocks, self).save(*args, **kwargs)  #calls the real save method

    def __str__(self):
        return str(self.ticker)

    class Meta:
        managed = True
        db_table = 'stocks'


class Portfolio(models.Model):
    # tickers_choice = []
    # for stk in Stocks.objects.all().filter(owned=False):
    #     tickers_choice.append((stk.ticker, stk.ticker))
    # ticker = models.CharField(max_length=200, primary_key=True, choices=tickers_choice) #String
    ticker = models.ForeignKey(Stocks, on_delete=CASCADE, unique=True)
    owned =models.BooleanField()  #Bool
    no_of_shares = models.IntegerField() #integer
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(default = 1, max_digits = 10, decimal_places=2)
    buy_date = models.DateField()
    amt_invested = models.DecimalField(max_digits = 10, decimal_places=2)
    current_val = models.DecimalField(max_digits = 10, decimal_places=2)
    gain_or_loss = models.DecimalField(max_digits = 10, decimal_places=2)

    def __str__(self):   # representation in admin
        return str(self.ticker)

    def save(self, *args, **kwargs): # overiding the save
        stk_inst = Stocks.objects.all().filter(ticker=self.ticker)[0]
        stk_inst.owned = True
        stk_inst.save()
        # Stocks.objects.all().filter(ticker=self.ticker).update(owned=True)
        self.current_price = Stocks.objects.all().filter(ticker=self.ticker)[0].current_price
        self.amt_invested = float(self.buy_price) * float(self.no_of_shares)
        self.current_val = float(self.current_price) * float(self.no_of_shares)
        self.gain_or_loss = self.current_val - self.amt_invested
        # self.gain_or_loss = 0
        super(Portfolio, self).save(*args, **kwargs)  #calls the real save method

    def delete(self, *args, **kwargs):
        stk_inst = Stocks.objects.all().filter(ticker=self.ticker)[0]
        stk_inst.owned = False 
        stk_inst.save()
        super(Portfolio, self).delete()

    class Meta:
        managed = True
        db_table = 'portfolio'