from django.shortcuts import render
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', render, kwargs={'template_name': 'faq.html'}, name='faq'),
    path('boxes/', render, kwargs={'template_name': 'boxes.html'}, name='boxes'),
    path('users_prof/', render, kwargs={'template_name': 'my-rent.html'}, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
