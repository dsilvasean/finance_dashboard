from django.http import response
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import requests

import worker
from .models import Portfolio, Stocks
from django.forms.models import model_to_dict
import json, threading, queue
from django.core.serializers.json import DjangoJSONEncoder
# from finance_front.common import pieces
# Create your views here.

from charts.forms import addToPortfolio
# from charts.models import Portfolio
from portfolio.models import Stock_test

from worker import new_make_data as pieces
from worker.models import worker_tracker

worker_instance = None

def index(request):
    context = {}
    data = {}
    test_data = {'name ':' sean', 'age': 18}
    data_ = []
    stk_list = Stocks.objects.all()
    for idx, stk in enumerate(stk_list):
        data[idx] = stk
    context['data'] = data
    return render(request, "charts/charts.html", context)
    # return HttpResponse(f'Youre lookaing at question {stk_id}')

def test(request):
    return Http404()

def workers(request):
    # global worker_instance
    # worker_instance = pieces.workers_()
    resp = {}
    context = {}
    trackers = worker_tracker.objects.all()
    for idx, tracker in enumerate(trackers):
        data = {}
        data['id'] = tracker.id
        data['file_or_dir_name'] = tracker.file_or_dir_name
        data['updated_at'] = tracker.updated_at
        data['updating'] = tracker.updating
        context[tracker.file_or_dir_name] = data
    resp['data'] = context
    # return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type="application/json")
    return render(request, 'charts/workers.html', resp)

def tracker(request):
    track = request.GET['tracker']
    # print(tracker)
    data = worker_tracker.objects.get(instance=track)
    return HttpResponse(f"tracker_init {data.running_status}")


#//////////////////////////////////////////// API CALLS ////////////////////////////////////////////////////////////////////////////////////////////
# Add stock to portfolio
def addToIndex(request, pk):
    charts_instance = get_object_or_404(Stocks, ticker=pk)
    # portfolio_instance= get_object_or_404(Portfolio, ticker=pk)

    if request.method == 'POST':
        myForm = addToPortfolio(request.POST)
        if myForm.is_valid():
            ticker = request.POST.get('ticker')
            no_of_shares = request.POST.get('no_of_shares')
            buy_price = request.POST.get('buy_price')
            buy_date = request.POST.get('buy_date')
            charts_instance.owned = True
            charts_instance.save()
            inst = Portfolio(ticker = charts_instance, owned=True, no_of_shares=no_of_shares, buy_price=buy_price, buy_date=buy_date)
            inst.save()
            messages.success(request, f'{ticker} Added to Portfolio')
            return HttpResponseRedirect(reverse('charts'))
        else:
            return HttpResponse(myForm.errors)
    else:
        return HttpResponse('Get request was sent')

# Remove stock from portfolio
def rmFromIndex(request):
    inst = get_object_or_404(Portfolio, ticker=request.POST.get('ticker'))
    inst.delete()
    messages.warning(request, f"{request.POST.get('ticker')} removed from portfolio")
    response = {'status': 1, 'message':'ok', 'url':'./'}
    # return HttpResponseRedirect(reverse('index'))
    return HttpResponse(json.dumps(response), content_type='application/json')

# Download hitorical data and information from yfinance
def dwnldData(request):
    global worker_instance
    worker_instance = pieces.workers_()
    def dwnld_data():
        worker_instance.get_data('1y', '1d')
        worker_instance.get_data('1d', '1d')
        worker_instance.mk_info_pickel()
        return HttpResponse('lol')
    if worker_instance.proxy_is_alive():
        new_thrwad = threading.Thread(target=dwnld_data, args =())
        new_thrwad.name = "download_thread"
        new_thrwad.setDaemon = True
        new_thrwad.start()
        new_thrwad.join()
        if new_thrwad.is_alive:
            return HttpResponse('downloading...')
        else:
            return HttpResponse('error')
    else:
        return HttpResponse('proxy_not_set')

# Update database 
def updateDb(request):
    global worker_instance
    def update_charts():
        worker_instance.calc__('update')
        # pieces.init_tickers()
        # pieces.get_data('1y','1d')
        # pieces.calc__('update')
        return HttpResponse('hello')
    if worker_instance ==None:
        worker_instance = pieces.workers_()
    new_thread = threading.Thread(target=update_charts, args=())
    new_thread.name = 'updateThread'
    new_thread.setDaemon(True)
    new_thread.start()
    new_thread.join()
    if new_thread.is_alive:
        return HttpResponse('updating....')
    else:
        return HttpResponse('error')

# Update charts from chartink

def updateCharts(request):
    global worker_instance
    def charts():
        worker_instance.dwnld_charts()
        return HttpResponse('charts updating')
    if worker_instance == None:
        worker_instance = pieces.workers_()
    if worker_instance.proxy_is_alive():
        new_thread = threading.Thread(target=charts, args=())
        new_thread.setDaemon(True)
        new_thread.start()
        new_thread.join()
        return HttpResponse('charts updating')
    else:
        return HttpResponse('proxy_not_set')

# Progress check
def progress(request):
    if worker_instance == None:
        data = {
            'message':"workers class has not yet been initialized go to /charts/worker"
        }
    else :
        data = {
        "message":"test_msg",
        "downloading_data":True,
        "pickel_status":round(worker_instance.progress_(worker_instance.pickel_status),2),
        "charts_updated": round(worker_instance.progress_(worker_instance.charts_downloaded), 2),
        "rows_updated": round(worker_instance.progress_(worker_instance.rows_updated), 2)
        }
    return HttpResponse(json.dumps(data), content_type="application/json")