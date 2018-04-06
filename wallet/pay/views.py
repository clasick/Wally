from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, CreditCardForm, AddMoneyForm, SendMoneyForm
from .models import CreditCard, Profile
from django.core.exceptions import ValidationError


def index(request):
    return HttpResponse("this is the index page")


def dashboard(request):
    return render(request, 'pay/index.html')


def account(request):
    u = User.objects.get(pk=request.user.id)

    linked = 0

    if CreditCard.objects.filter(user=u).count():
        linked = 1

    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            u.profile.money += float(form.cleaned_data.get('amt'))
            u.save()

    form = AddMoneyForm()
    context = {'user': u, 'linked': linked, 'form': form}
    return render(request, 'pay/account.html', context)


def transfer(request):
    u = User.objects.get(pk=request.user.id)

    errors = []

    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            if Profile.objects.filter(phone_no=form.cleaned_data.get('receiver_phone')).count():
                if u.profile.money > float(form.cleaned_data.get('amt')):
                    u.profile.money -= float(form.cleaned_data.get('amt'))
                    r = Profile.objects.filter(
                        phone_no=form.cleaned_data.get('receiver_phone')).first()
                    r.money += float(form.cleaned_data.get('amt'))
                    u.save()
                    r.save()
                else:
                    errors.append(
                        "You don't have enough money in your account. Please add more balance.")
            else:
                errors.append(
                    "User with specified phone number does not exist.")

    form = SendMoneyForm()
    context = {'user': u, 'form': form, 'errors': errors}

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
        print("\n\n\n this is the form")
        print(form)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = u
            c.save()
            return render(request, 'pay/index.html')
    else:
        form = CreditCardForm()
    return render(request, 'pay/credit.html', {'form': form})
