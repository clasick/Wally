from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return HttpResponse("this is the index page")

def dashboard(request):
    return render(request, 'pay/index.html')

def account(request):
    if request.GET.get('addmoney'):
        u = User.objects.get(username=request.user.username)
        u.profile.money += int(request.GET.get('addmoney'))
        u.save()
    return render(request, 'pay/account.html')

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
