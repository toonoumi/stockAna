from django.shortcuts import render
from django.http import HttpResponse 
from django.template import loader
import urllib
from .models import Question

# Create your views here.
last_token=''

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def px(request, token):
    page=urllib.request.urlopen('https://%s' % token)
    #print(page.read())
    global last_token
    last_token=token
    return HttpResponse(page.read())
    #return HttpResponse("test. Token: %s" % token)
    
def link_click(request,content):
    link='https://%s/%s' % (last_token, content)
    print(link)
    page=urllib.request.urlopen(link)
    return HttpResponse(page.read())