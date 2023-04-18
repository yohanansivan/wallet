from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world.")

def testing(request, coin):
    response = "Testing coin %s"
    return HttpResponse(response % coin)
