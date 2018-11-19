"""AwsIotWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from . import views

app_lable = 'awsiot'
urlpatterns = [
    path('users/', views.UserViewSet.as_view()),
    # 用户登录
    path('register/', views.UserRegister.as_view()),
    path('login/', views.UserRegister.as_view()),
    path('test/', views.TestView.as_view(), name='test'),
    path('test1/', views.TestView.as_view(), name='test'),
]
