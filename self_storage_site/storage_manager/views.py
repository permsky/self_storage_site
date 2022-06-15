from django.shortcuts import render
from django.http import JsonResponse


def register(request):
    return JsonResponse({'success': 'successfully!'})
