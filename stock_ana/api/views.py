from django.shortcuts import render
from django.http import HttpResponse
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ../../stock_ana_proj import DBFunctions as dbf

# Create your views here.
def index(request):
    return render(request,'./api/index.html')

def search(request,ticker):
    rst=dbf.get_single_result_ticker(ticker.upper())
    return HttpResponse(str(rst[0][6]))