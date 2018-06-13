from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
#def index(request):
#    # return HttpResponse('Hello from Python!')
#    return render(request, 'index.html')

import requests

def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>do you love narwhals? well we do so come look something up about narwhals and tell people about it. welcome to ngarchat (and yes it is supposed to be spelled like that short for gnarly narwhals)</pre>')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

