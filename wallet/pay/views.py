from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, CreditCardForm, AddMoneyForm
from .models import CreditCard

def index(request):
    return HttpResponse("this is the index page")

def dashboard(request):
    return render(request, 'pay/index.html')

def account(request):
    u  = User.objects.get(pk=request.user.id)
    
    linked = 0

    if CreditCard.objects.filter(user=u).count():
        linked = 1
        
    form = AddMoneyForm()
    context = {'user' : u, 'linked': linked, 'form': form}
    return render(request, 'pay/account.html', context)

def transfer(request):
    if request.GET.get('send_user'):
        u = User.objects.get(username=request.user.username)
        s = User.objects.get(pk=request.GET.get('send_user'))
        u.profile.money -= int(request.GET.get('amount'))
        s.profile.money += int(request.GET.get('amount'))
        u.save()
        s.save()
    user_list = User.objects.all()
    context = {'users': user_list}
    return render(request, 'pay/transfer.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_no = form.cleaned_data.get('phone_no')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return render(request, 'pay/index.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def link_card(request, u_id):
    u = get_object_or_404(User, pk=u_id)
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            creditcard = form.save()
            creditcard.refresh_from_db()
            creditcard.user = user
            creditcard.save()
            return render(request, 'pay/index.html')
    else:
        form = CreditCardForm()
    return render(request, 'pay/credit.html', {'form': form})