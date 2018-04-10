from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CreditCard, Profile

from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Username')
    firstname = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='First Name')
    lastname = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Last Name')
    phone_no = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Phone Number')
    password1 = forms.CharField(max_length=10, widget=forms.PasswordInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Password')
    password2 = forms.CharField(max_length=10, widget=forms.PasswordInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Password Confirmation')

    def clean_phone_no(self):
        if Profile.objects.filter(phone_no=self.cleaned_data.get('phone_no', '')):
            raise ValidationError(
                'Given phone number already exists in database.')

        return self.cleaned_data.get('phone_no', '')

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'phone_no', 'password1', 'password2', )


class CreditCardForm(forms.ModelForm):
    owner = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Owner')
    number = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Card Number')
    exp_date = forms.CharField(max_length=6, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Expiry Date')
    cvv = forms.CharField(max_length=3, widget=forms.PasswordInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='CVV')

    def clean_owner(self):
        if not all(char.isalpha() or char == ' ' for char in self.cleaned_data.get('owner', '')):
            raise ValidationError('Owner name should only contain alphabets.')

        return self.cleaned_data.get('owner', '')

    def clean_number(self):
        if len(self.cleaned_data.get('number', '')) != 16:
            raise ValidationError("Credit card number needs to be 16 digits.")
        if not all(char.isdigit() for char in self.cleaned_data.get('number', '')):
            raise ValidationError("Credit card contains special characters.")

        return self.cleaned_data.get('number', '')

    def clean_exp_date(self):
        if len(self.cleaned_data.get('exp_date', '')) != 6:
            raise ValidationError(
                "Exp date number needs to be 6 digits. (MMYYYY) ")
        if not all(char.isdigit() for char in self.cleaned_data.get('exp_date', '')):
            raise ValidationError("Exp date contains special characters")

        return self.cleaned_data.get('exp_date', '')

    def clean_cvv(self):
        if len(self.cleaned_data.get('cvv', '')) != 3:
            print(len(self.cleaned_data.get('cvv', '')))
            raise ValidationError("CVV number needs to be 3 digits.")
        if not all(char.isdigit() for char in self.cleaned_data.get('cvv', '')):
            raise ValidationError("CVV contains special characters")

        return self.cleaned_data.get('cvv', '')

    class Meta:
        model = CreditCard
        exclude = ('user',)


class AddMoneyForm(forms.Form):
    amt = forms.FloatField(min_value=0.0, max_value=100000.0, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Amount (Limit: Rs. 100,000)')

    def clean_amt(self):
        if self.cleaned_data.get('amt', '') <= 0:
            raise ValidationError("Amount cannot be zero or negative")

        return self.cleaned_data.get('amt', '')
    # exp_date = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'form-control'}), label = 'Expiry Date' )


class SendMoneyForm(forms.Form):
    receiver_phone = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Beneficiary Phone no.')
    amt = forms.FloatField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': 'form-control'}), label='Amount')

    def clean_amt(self):
        print(self.cleaned_data.get('amt', ''), ' is the amt ')
        if self.cleaned_data.get('amt', '') <= 0:
            print("INSIDE THE NEGATIVE")
            raise ValidationError(
                "Cannot send negative or zero amount of money.")

        return self.cleaned_data.get('amt', '')

    def clean_receiver_phone(self):
        if not all(char.isdigit() for char in self.cleaned_data.get('receiver_phone', '')):
            raise ValidationError("Receiver phone contains special characters")

        return self.cleaned_data.get('receiver_phone', '')
