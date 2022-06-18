from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from django.http import JsonResponse
from storage_manager.models import Box, BoxPlace, CalculateCustomer, Order
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timezone

from .utils import randomise_from_range, get_email


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse(form.errors)
    return JsonResponse({})


def sign_in(request):
    if request.method == "POST":
        context = {}
        email = request.POST['email']
        password = request.POST['password']

        account = authenticate(request, username=email, password=password)
        if account is None:
            context['message'] = 'Неверный логин или пароль'
            context['success'] = False
            return JsonResponse(context)

        elif account:
            login(request, account)
            context['message'] = 'Вы вошли в аккаунт!'
            context['success'] = True
            return JsonResponse(context)

        else:
            context['message'] = 'Неверный логин или пароль'
            context['success'] = False
            return JsonResponse(context)

    return JsonResponse({})


def index(request):
    if request.GET.get('EMAIL1'):
        get_email(request)
        return redirect('index')

    all_box_spaces = list(BoxPlace.objects.all().prefetch_related(
        'place_boxes').get_free_boxes().get_min_price())
    space_count = len(all_box_spaces)
    random_box_space_index = randomise_from_range(space_count)
    random_box_space = all_box_spaces[random_box_space_index]
    free_space = random_box_space.boxes_quantity - random_box_space.free_boxes

    min_box_price = Box.objects.all().aggregate(Min('tariff'))['tariff__min']
    context = {
        'min_box_price': min_box_price,
        'box_space': random_box_space,
        'free_space': free_space,
        'min_price': random_box_space.min_price,
    }
    return render(request, 'index.html', context)


@login_required
def personal_account(request):
    user_orders = Order.objects.filter(customer=request.user).select_related('box__boxes_place')
    for order in user_orders:
        order.expires_soon = (order.end_date - date.today()).days < 14

    context = {
        'orders': user_orders
    }
    return render(request, 'personal_account.html', context)


def boxes(request):
    if request.GET.get('EMAIL1'):
        get_email(request)
        return redirect('boxes')

    all_places = BoxPlace.objects.all().prefetch_related(
        'place_boxes').get_free_boxes().get_min_price()

    context = {
        'all_places': all_places
    }
    return render(request, 'boxes.html', context)
