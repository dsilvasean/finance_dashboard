from django.http import response
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import requests

from .models import Portfolio, Stocks
from django.forms.models import model_to_dict
import json, threading, queue
from django.core.serializers.json import DjangoJSONEncoder
# from finance_front.common import pieces
# Create your views here.

from charts.forms import addToPortfolio
# from charts.models import Portfolio

from charts.models import Update_trackers
from utils import fetch_data 

worker_instance = None

def login_(request):
    global worker_instance
    if request.method =='GET':
        return render(request, "registration/login.html")
    username = request.POST['username']
    print(username)
    password = request.POST['password']
    user  = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        request.session['username'] = user.get_username()
        worker_instance = fetch_data.workers_()
        if request.POST['next'] == '' or None:
            print('lolll')
            return HttpResponseRedirect('/charts')
        else:
            return HttpResponseRedirect(request.POST['next'])
    else:
        return HttpResponse('asas')

def logout_(request):
    logout(request)
    return HttpResponseRedirect('login')

def loginForm(request):
    return render(request, "registration/login.html") 

@login_required(login_url='login_')
def index(request):
    context = {}
    data = {}
    test_data = {'name ':' sean', 'age': 18}
    data_ = []
    stk_list = Stocks.objects.all()
    for idx, stk in enumerate(stk_list):
        data[idx] = stk
    context['data'] = data
    print(request.session['username'])
    return render(request, "charts/charts.html", context)

def test(request):
    return HttpResponse(request.session['id'])

@login_required(login_url='login_')
def workers(request):
    # global worker_instance
    # worker_instance = pieces.workers_()
    resp = {}
    context = {}
    trackers = Update_trackers.objects.all()
    for idx, tracker in enumerate(trackers):
        data = {}
        data['id'] = tracker.id
        data['file_or_dir_name'] = tracker.file_or_dir_name
        data['updated_at'] = tracker.updated_at
        data['updating'] = tracker.updating
        context[tracker.file_or_dir_name] = data
    resp['data'] = context
    return render(request, 'charts/workers.html', resp)

#//////////////////////////////////////////// API CALLS ////////////////////////////////////////////////////////////////////////////////////////////
# API V1
# Add stock to portfolio
# Remove stock from portfolio
# Download hitorical data and information from yfinance
# Update database 
# Update charts from chartink
# Progress check
# ////////////////////////////// API V2 CALLS////////////////////////////////////////////////////////////////////
@login_required
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

@login_required
def rmFromIndex(request):
    inst = get_object_or_404(Portfolio, ticker=request.POST.get('ticker'))
    inst.delete()
    messages.warning(request, f"{request.POST.get('ticker')} removed from portfolio")
    response = {'status': 1, 'message':'ok', 'url':'./'}
    # return HttpResponseRedirect(reverse('index'))
    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def updateHistoricalData(request):
    _reso_ = None
    global worker_instance
    try:
        worker_instance = fetch_data.workers_()
        _resp_ = worker_instance.update_max_data()
        resp_ = {
            'message':_resp_
        }
        return HttpResponse(json.dumps(resp_, content_type="application/json"))
    except Exception as e:
        resp_ = {
            'message':_resp_
        }
        return HttpResponse(json.dumps(resp_), content_type="application/json")
@login_required
def statsUpdate(request):
    global worker_instance
    resp_ = {'message':1}
    try:
        inst = worker_instance
        _resp_ = inst.yquery()
        resp_['message'] = _resp_
    except Exception as e:
        # resp_['message'] = e
        print(e)
    return HttpResponse(json.dumps(resp_), content_type="application/json")

@login_required
def updateRowsInDb(request):
    global worker_instance
    try:
        inst = worker_instance
        _resp_ = inst.update_rows('update')
        resp_ = {
            'message':_resp_
        }
        return HttpResponse(json.dumps(resp_), content_type="application/json")
    except Exception as e:
        resp_ = {
            'message':e
        }
        return HttpResponse(json.dumps(resp_), content_type="application/json")

@login_required
def updateCharts_(request):
    global worker_instance
    try:
        inst = worker_instance
        _resp_ = inst.dwnld_charts()
        resp_ = {
            'message':_resp_
        }
        return HttpResponse(json.dumps(resp_), content_type="application/json")
    except Exception as e:
        resp_ = {
            'message': e
        }
        return HttpResponse(json.dumps(resp_), content_type='application/json')
@login_required(login_url='login_')
def progress_(request):
    global worker_instance
    resp = worker_instance.progress_debug()
    data_ = {
        'username': request.session['username'],
        'data':{
            'message': "hello world",
            'debug':resp
        }
    }
    return HttpResponse(json.dumps(data_), content_type='application/json')

def bhavCopy(request):
    inst = fetch_data.workers_()
    ret = inst.update_max_data()
    return HttpResponse(ret)

def debugUpdate(request):
    inst = fetch_data.workers_()
    # inst.update_max_data()
    inst.yquery()
    # return HttpResponse("helllo debug")

@login_required
def yquery(request):
    global worker_instance
    # inst.dwnld_charts()
    worker_instance.update_rows('update')