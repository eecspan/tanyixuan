from django.urls import path, re_path
from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('get-market/', views.get_market, name="get_market"),
    path('my-booth/', views.my_booth, name="my_booth"),
    path('get-my-booth/', views.get_my_booth, name="get_my_booth"),
    path('start-business/', views.start_business, name="start_business"),
    path('close-booth/', views.close_booth, name="close_booth"),
    path('open-booth/', views.open_booth, name="open_booth"),
    path('create-booth/', views.create_booth, name="create_booth"),
    path('delete-booth/', views.delete_booth, name="delete_booth"),
    path('check-booth-reapeat/', views.check_booth_repeat, name="check_booth_repeat"),
    # 在摊主首页中展示摆摊地点详情
    re_path(r'^market-detail/(?P<market_id>\d+)/$', views.market_detail, name="market_detail")
]