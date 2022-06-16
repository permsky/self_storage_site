from django.shortcuts import render
from django.http import JsonResponse
from storage_manager.models import Box, BoxPlace
from django.db.models import Min

from .utils import randomise_from_range


def register(request):
    return JsonResponse({'success': 'successfully!'})


def index(request):
    #print(request.__dict__)
    all_box_spaces = list(BoxPlace.objects.all().get_free_boxes().get_min_price())
    space_count = len(all_box_spaces)
    random_box_space_index = randomise_from_range(space_count)
    random_box_space = all_box_spaces[random_box_space_index]
    #q = BoxPlace.objects.all().get_free_boxes()
    #print(random_box_space.min_price)

    min_box_price = Box.objects.all().aggregate(Min('tariff'))['tariff__min']
    context = {
        'min_box_price': min_box_price,
        'box_space': random_box_space,
        'free_space': random_box_space.free_boxes,
        'min_price': random_box_space.min_price,
    }
    return render(request, 'index.html', context)
