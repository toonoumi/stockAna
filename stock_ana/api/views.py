from django.shortcuts import render
from django.http import HttpResponse
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__+ "/../../"))))

from stock_ana_proj import DBFunctions as dbf


# Create your views here.
def index(request):
    return render(request,'./api/index.html')

def search(request,ticker):
    rst=dbf.get_single_result_ticker(ticker.upper())
    if len(rst) == 0:
        #not found, try to retrive live data
        rst=dbf.record_new_ticker(ticker.upper())
        return HttpResponse('Record Not Found for: %s.' % ticker.upper())
    return HttpResponse(str(rst[0][6]))