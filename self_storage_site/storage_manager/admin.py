from dateutil.relativedelta import *
from datetime import timedelta

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    BoxPlace,
    Box,
    BoxVolume,
    RentalTime,
    Order,
    Job,
    CalculateCustomer,
    Profile
)


@admin.register(BoxPlace)
class BoxPlaceAdmin(admin.ModelAdmin):
    ...


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_filter = ['in_use']
    list_display = [
        'box_volume',
        'boxes_place',
        'tariff',
        'in_use',
    ]


@admin.register(BoxVolume)
class BoxVolumeAdmin(admin.ModelAdmin):
    ...


@admin.register(RentalTime)
class RentalTimeAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    readonly_fields = ['end_date']
    list_display = [
        'customer',
        'box',
        'rental_time',
        'start_date',
        'end_date',
        'status',
    ]

    def save_model(self, request, obj, form, change):
        time_interval = obj.rental_time.time_intervals
        time_delta = relativedelta(months=+time_interval)
        obj.end_date = obj.start_date+time_delta
        super().save_model(request, obj, form, change)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = [
        'status',
        'date_to_run',
        'interval',
        'with_qrcode',
        'order'
    ]


@admin.register(CalculateCustomer)
class OrderCalculateCustomer(admin.ModelAdmin):
    ...


class ProfileFilter(admin.SimpleListFilter):
    title = 'Статус клиента'
    parameter_name = 'get_status_profile'

    def lookups(self, request, model_admin):
        return [
            ['current', 'Боксы в аренде'],
            ['not_current', 'Нет боксов в аренде'],
            ['expired', 'Аренда просрочена'],
        ]

    def queryset(self, request, queryset):
        if self.value() == 'current':
            return queryset.filter(
                user__orders__status='active'
            ).distinct()
        elif self.value() == 'not_current':
            return queryset.exclude(
                user__orders__gte=0
            ).distinct()
        elif self.value() == 'expired':
            return queryset.filter(
                user__orders__status='expired'
            ).distinct()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'phone_number',
        'avatar',
        'get_status_profile',
    ]
    list_filter = (ProfileFilter,)

    def get_status_profile(self, obj):
        states_colors = {
            'боксы в аренде': 'green',
            'нет боксов в аренде': 'gray',
            'аренда просрочена': 'red'
        }
        is_expired = False
        for order in obj.user.orders.all():
            if order.status == 'expired':
                is_expired = True
                break
        if not obj.user.orders.all():
            state = 'нет боксов в аренде'
        elif is_expired:
            state = 'аренда просрочена'
        else:
            state = 'боксы в аренде'
        return mark_safe(f'<span style="color:{states_colors[state]};font-weight:bold">{state}</span>')
    get_status_profile.short_description = 'Статус клиента'
