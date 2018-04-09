from django.urls import path
from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views

from . import views

app_name = 'pay'

urlpatterns = [
    path('', auth_views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('account', views.account, name='account'),
    path('transfer', views.transfer, name='transfer'),
    path('link-card/<int:u_id>', views.link_card, name='link_card'),
    path('transcations', views.transcations, name='transcations' ),
    path('signup', views.signup, name='signup'),
    path('shopping-cart', views.shopping_cart, name='shopping_cart'),
]
