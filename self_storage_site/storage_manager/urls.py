from django.shortcuts import render
from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', render, kwargs={'template_name': 'faq.html'}, name='faq'),
    path('boxes/', render, kwargs={'template_name': 'boxes.html'}, name='boxes'),
    path('users_prof/', render, kwargs={'template_name': 'my-rent.html'}, name='profile'),
]