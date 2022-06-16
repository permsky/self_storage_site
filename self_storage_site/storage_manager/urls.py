from django.shortcuts import render
from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    # path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('', views.index, name='index'),
    path('faq/', render, kwargs={'template_name': 'faq.html'}, name='faq'),
    path('register/', include('storage_manager.urls')),
    path('admin/', admin.site.urls),
]