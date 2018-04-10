from django.shortcuts import render, redirect, reverse, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, CreditCardForm, AddMoneyForm, SendMoneyForm, ChangeProfileDetails
from .models import CreditCard, Profile, Transcation, Product
from django.core.exceptions import ValidationError
from datetime import datetime
import pytz
from django.utils.timezone import make_aware

from cart.cart import Cart


def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)


def edit_profile(request):
    if request.method == 'POST':
        form = ChangeProfileDetails(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.profile.phone_no = form.cleaned_data['phone_no']
            request.user.profile.ssn = form.cleaned_data['ssn']
            request.user.save()
            return redirect('pay:account')
    else:
        # u = User.objects.filter(pk=request.user.id)
        # print(u)
        form = ChangeProfileDetails()
        form.fields['username'].initial = request.user.username
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['phone_no'].initial = request.user.profile.phone_no
        form.fields['ssn'].initial = request.user.profile.ssn

    return render(request, 'signup.html', {'form': form, 'signup': 0})


def shopping_cart(request):

    u = User.objects.get(pk=request.user.id)

    amount = 0
    errors = []

    for item in Cart(request):
        amount = amount + item.product.price

    if request.GET.get('make-payment'):
        if amount <= u.profile.money:
            for item in Cart(request):
                remove_from_cart(request, item.product.id)
                u.profile.money -= item.product.price
            u.save()
            return redirect('pay:dashboard')
        else:
            errors.append(
                "You don't have enough money in your account. Please add more balance.")

    if request.GET.get('remove'):
        try:
            remove_from_cart(request, request.GET.get('remove'))
            errors.append("Removed item from cart.")
        except:
            errors.append("Error removing item from cart.")

    context = {'cart': list(Cart(request)), 'user': u,
               'amount': amount, 'errors': errors}
    return render_to_response('pay/cart.html', context)


def index(request):
    return HttpResponse("this is the index page")


def dashboard(request):

    product_list = Product.objects.all()

    if request.GET.get('add-prod'):
        add_to_cart(request, request.GET.get('add-prod'), 1)
        print("added to cart")

    context = {'product_list': product_list}
    return render(request, 'pay/index.html', context)


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
    else:
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
                    t = Transcation()
                    t.sender = u
                    t.receiver = r.user
                    t.amt = float(form.cleaned_data.get('amt'))
                    t.timestamp = datetime.now()
                    u.save()
                    r.save()
                    t.save()
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


def transcations(request):
    receive_list = Transcation.objects.filter(receiver=request.user).order_by('-timestamp')
    send_list = Transcation.objects.filter(sender=request.user).order_by('-timestamp')

    context = {'receive_list': receive_list, 'send_list': send_list}
    return render(request, 'pay/transcations.html', context)
