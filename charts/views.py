from django.http import response
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import Portfolio, Stocks
from django.forms.models import model_to_dict
import json, threading, queue
from django.core.serializers.json import DjangoJSONEncoder
# from finance_front.common import pieces
# Create your views here.

from charts.forms import addToPortfolio
# from charts.models import Portfolio
from portfolio.models import Stock_test

from worker import make_data as pieces
from worker.models import worker_tracker

# def index(request):
#     data = {}
#     test_data = {'name ':' sean', 'age': 18}
#     data_ = []
#     stk_list = Stocks.objects.all()
#     for stk in stk_list:
#         data[f'{stk.ticker}'] = 'hello'
#         # data_.append(stk.ticker)
#     # return HttpResponse(stk_list[1].volume)
#     return HttpResponse(test_data)

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

def workers(request):
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

def rmFromIndex(request):
    inst = get_object_or_404(Portfolio, ticker=request.POST.get('ticker'))
    inst.delete()
    messages.warning(request, f"{request.POST.get('ticker')} removed from portfolio")
    response = {'status': 1, 'message':'ok', 'url':'./'}
    # return HttpResponseRedirect(reverse('index'))
    return HttpResponse(json.dumps(response), content_type='application/json')

def updateDb(request):
    def update_charts():
        pieces.init_tickers()
        # pieces.get_data('1y','1d')
        pieces.calc__('update')
        return HttpResponse('hello')
    new_thread = threading.Thread(target=update_charts, args=())
    new_thread.name = 'updateThread'
    new_thread.setDaemon(True)
    new_thread.start()
    new_thread.join()
    if new_thread.is_alive:
        return HttpResponse('updating....')
    else:
        return HttpResponse('error')

def dwnldData(request):
    def dwnld_data():
        pieces.init_tickers()
        pieces.get_data('1y', '1d')
        pieces.get_data('1d', '1d')
        pieces.mk_info_pickel()
        return HttpResponse('lol')
    if pieces.proxy_is_alive():
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

def dwnldCharts(request):
    pieces.init_tickers()
    pieces.dwnld_charts()
    return HttpResponse('downloaded')

def tracker(request):
    track = request.GET['tracker']
    # print(tracker)
    data = worker_tracker.objects.get(instance=track)
    return HttpResponse(f"tracker_init {data.running_status}")


def updateProgress(request):
    response_data = {}
    data = []
    threads = threading.enumerate()
    for i in range(0, len(threads)):
        if threads[i].name == 'updateThread':
            if threads[i].is_alive:
                p = pieces.progress(len(pieces.ticker_list)-1)
                response_data['progress'] = p
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            break
        data.append(threads[i].name)
    response_data['progress'] = 'updated'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def pickel_progress(request):
    response_data = {}
    data = []
    response_data['pk_stat'] = pieces.pick_progress(len(pieces.ticker_list))
    # response_data['progress'] = 'updated'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def updateCharts(request):
    def charts():
        pieces.init_tickers()
        pieces.dwnld_charts()
        return HttpResponse('charts updating')
    if pieces.proxy_is_alive():
        new_thread = threading.Thread(target=charts, args=())
        new_thread.setDaemon(True)
        new_thread.start()
        new_thread.join()
        return HttpResponse('charts updating')
    else:
        return HttpResponse('proxy_not_set')