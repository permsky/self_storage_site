from django.contrib import admin

from .models import (BoxPlace, Box, BoxVolume, RentalTime, Order, Job,
                     CalculateCustomer)


@admin.register(BoxPlace)
class BoxPlaceAdmin(admin.ModelAdmin):
    ...


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    ...


@admin.register(BoxVolume)
class BoxVolumeAdmin(admin.ModelAdmin):
    ...


@admin.register(RentalTime)
class RentalTimeAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
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
