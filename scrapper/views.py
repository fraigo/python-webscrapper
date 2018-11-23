from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from scrapper import scrapper

import os


def home(request):
    return render(request, 'index.html')

def data(request):
    content = ''
    if 'q' in request.GET:
        search = request.GET['q']
        name = scrapper.get_name(search)
        filename = os.path.join("data",name+".json")
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
