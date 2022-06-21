from django.shortcuts import render
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', render, kwargs={'template_name': 'faq.html'}, name='faq'),
    path('boxes/', views.boxes, name='boxes'),
    path('profile/change/', views.change_user_profile, name='profile_change'),
    path('profile/', views.personal_account, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.send_qrcode, name='send_qrcode'),
    path('createorder/', views.make_order, name='create_order'),
    path('orderpay/<int:order_id>/', views.pay_order, name='payment'),
    path('order/<int:pk>/', views.prolong, name='prolong'),
    ]
