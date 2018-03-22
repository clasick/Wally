from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("this is the index page")

def dashboard(request):
    return render(request, 'pay/index.html')

def account(request):
    return render(request, 'pay/account.html')

def transfer(request):
    return render(request, 'pay/transfer.html')
