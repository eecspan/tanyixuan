from django.urls import path, re_path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('create-market/', views.create_market, name='create_market'),
    path('my-market/', views.my_market, name='my_market'),
    path('check-market-repeat/', views.check_market_repeat, name='check_market_repeat'),
    path('delete-market/', views.delete_market, name='delete_market'),
    # 在摊主首页中展示摆摊地点详情
    re_path(r'^booth-detail/(?P<booth_id>\d+)/$', views.booth_detail, name="booth_detail")
]