from django.http import HttpResponse
from django.template.loader import render_to_string

from . import scrapper

import os


def home(request):
    content = render_to_string('index.html', {'foo': 'bar'})
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
        res = scrapper.scrappe(url)
        scrapper.save(search, res)
        return data(request)
    return HttpResponse(content)
