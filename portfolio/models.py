from django.db import models
# from charts.models import Stocks
import charts.models
# Create your models here.

class Stock_test(models.Model):
    tickers_choice = []
    # for stk in charts.models.Stocks.objects.all():
    #     tickers_choice.append((stk.ticker, stk.ticker))
    ticker = models.CharField(max_length=200, primary_key=True, choices=tickers_choice) #String
    owned =models.BooleanField()  #Bool
    no_of_shares = models.IntegerField() #integer
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits = 10, decimal_places=2)
    buy_date = models.DateField()
    amt_invested = models.DecimalField(max_digits = 10, decimal_places=2)
    current_val = models.DecimalField(max_digits = 10, decimal_places=2)
    gain_or_loss = models.DecimalField(max_digits = 10, decimal_places=2)

    def __str__(self):   # representation in admin
        return str(self.ticker)
    
    def save(self, *args, **kwargs): # overiding the save 
        self.current_price = self.current_price
        self.amt_invested = self.buy_price * self.no_of_shares
        self.current_val = self.current_price * self.no_of_shares
        self.gain_or_loss = self.current_val - self.amt_invested
        super(Stock_test, self).save(*args, **kwargs)  #calls the real save method


