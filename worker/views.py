from django.shortcuts import render
from django.http import HttpResponse
from worker import make_data as pieces
import json
# Create your views here.
def test(request):
    return HttpResponse('test at status')

def get_progress(request):
    response_data = {}
    data = []
    response_data['mk_pickel_status'] = pieces.pick_progress(len(pieces.ticker_list))
    response_data['update_progress'] = pieces.progress(len(pieces.ticker_list))
    response_data['downloading_data'] = pieces.dwn_status()
    response_data['charts_progress'] = pieces.charts_progress(len(pieces.ticker_list))
    return HttpResponse(json.dumps(response_data), content_type="application/json")
