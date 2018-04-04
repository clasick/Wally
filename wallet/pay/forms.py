from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone_no = models.CharField(max_length=10, null=True)

    class Meta:
        model = User
        fields = ('username', 'phone_no', 'password2', )