from django.contrib import admin

from .models import (
    BoxPlace,
    Box,
    BoxVolume,
    RentalTime,
    Order,
    Job,
    CalculateCustomer
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
    list_display = [
        'customer',
        'box',
        'rental_time',
        'start_date',
        'end_date',
        'status',
    ]


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
