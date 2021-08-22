from django import forms

class addToPortfolio(forms.Form):
    ticker = forms.CharField()
    no_of_shares = forms.IntegerField()
    buy_price = forms.DecimalField(decimal_places=2)
    buy_date = forms.DateField()