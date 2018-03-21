from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'pay'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('login', auth_views.login, {'template_name':'pay/login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
]
