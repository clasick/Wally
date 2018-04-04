from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Username' )
    phone_no = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Phone Number' )
    password1 = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Password')
    password2 = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Password Confirmation')
    
    class Meta:
        model = User
        fields = ('username', 'phone_no', 'password1', 'password2', )

class CreditCardForm(forms.Form):
    owner = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Owner' )
    number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Card Number' )
    exp_date = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Expiry Date' )
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'CVV' )

class AddMoneyForm(forms.Form):
    amt = forms.FloatField(min_value=0.0, max_value=100000.0, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Amount' )
    # exp_date = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Expiry Date' )