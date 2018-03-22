from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = 'pay'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
#   path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('account', views.account, name='account'),
    path('transfer', views.transfer, name='transfer')
]
