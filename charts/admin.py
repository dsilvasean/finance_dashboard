from django.contrib import admin
from charts.models import Stocks
from charts.models import Portfolio
from charts.models import InfoDict 
from django.db import models
from django.forms import TextInput, Textarea


# Register your models here.

class StcoskAdmin(admin.ModelAdmin):
    readonly_fields = ('last_updated',)
    formfield_overrides = {
       models.IntegerField: {'widget': TextInput(attrs={'size':'200'})},
        models.IntegerField: {'widget': Textarea(attrs={'rows':1, 'cols':20})},
    }
admin.site.register(Portfolio)
admin.site.register(Stocks, StcoskAdmin)
admin.site.register(InfoDict)

