from django.urls import path, reverse
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('create-market/', views.create_market, name='create_market'),
    path('check-market-repeat/', views.check_market_repeat, name='check_market_repeat'),
]