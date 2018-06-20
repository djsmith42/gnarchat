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
    return HttpResponse("""
    <html>
        <body>
            <h1>It's Gnarchat, log in and chat about narwhals!</h1>
            <img src="static/gnarwhal.jpg" style="width: 500px" />
            <img src="static/dgnarwhal.jpg" style="width: 500px" />
        </body>
    </html>
    """)

def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
