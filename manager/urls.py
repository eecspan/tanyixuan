from django.urls import path, reverse
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
]