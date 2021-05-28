from django.contrib import admin
from portfolio.models import Stock_test
# Register your models here.

# Register modesl so that they can be mdoified using admin panel
class Stock_testAdmin(admin.ModelAdmin):
    readonly_fields = ('amt_invested', 'current_val', 'gain_or_loss')
    exclude = ('amt_invested','current_val', 'gain_or_loss')

admin.site.register(Stock_test, Stock_testAdmin)
