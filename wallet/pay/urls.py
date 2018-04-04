from django.urls import path
from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views

from . import views

app_name = 'pay'

urlpatterns = [
    # ex: /polls/
    path('', auth_views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('account', views.account, name='account'),
    path('transfer', views.transfer, name='transfer'),
    path('signup', views.signup, name='signup')

]
