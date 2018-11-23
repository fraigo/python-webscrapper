from django.http import HttpResponse
from . import scrapper

import os


def home(request):
    filename = os.path.join("templates","index.html")
    content = open(filename, "r")
    return HttpResponse(content)

def data(request):
    content = ''
    if 'q' in request.GET:
        search = request.GET['q']
        filename = os.path.join("data",search+".json")
        content = open(filename, "r")
    return HttpResponse(content)

def search(request):
    content = ''
    if 'q' in request.GET:
        search = request.GET['q']
        LOCATION = "Vancouver, BC"
        url = scrapper.get_url(search, LOCATION)
        scrapper.scrappe(search,url)
        return data(request)
    return HttpResponse(content)
