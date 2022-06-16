from django.shortcuts import render
from django.http import JsonResponse
from storage_manager.models import Box
from django.db.models import Min


def register(request):
    return JsonResponse({'success': 'successfully!'})


def index(request):
    #print(request.__dict__)
    min_box_price = Box.objects.all().aggregate(Min('tariff'))['tariff__min']
    context = {
        'min_box_price': min_box_price,
    }
    return render(request, 'index.html', context)
