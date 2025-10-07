from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Це другий застосунок Django!")