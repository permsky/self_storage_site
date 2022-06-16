from django.shortcuts import render
from django.http import JsonResponse


def register(request):
    return JsonResponse({'success': 'successfully!'})


def index(request):
    #print(request.__dict__)
    return render(request, 'index.html')
