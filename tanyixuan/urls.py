"""tanyixuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from registerLogin import views
# 以下用于显示静态资源
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('register/', views.register),
    path('logout/', views.logout),
    path('consumer/', include('consumer.urls')),
    path('seller/', include('seller.urls')),
    path('manager/', include('manager.urls')),
    path('admin/', admin.site.urls),
]

# 以下用于显示静态资源
urlpatterns += [
    re_path('favicon.ico', serve, {'document_root': 'static/', 'path': 'images/favicon.ico'}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': 'static/images/'}),  # 为了存储静态图片数据库中只需要存图片名字
    # re_path(r'^static/images/(?P<path>.*)$', serve, {'document_root': 'static/images/'})  # 为了存储静态图片数据库中只需要存图片名字
]
