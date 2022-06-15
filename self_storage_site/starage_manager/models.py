from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class BoxVolume(models.Model):
    volume = models.FloatField(
        'Объем бокса',
        validators=[MinValueValidator(0.0)])


class Box(models.Model):
    box_volume = models.ForeignKey(
        BoxVolume,
        on_delete=models.PROTECT,
        related_name='boxes',)
    in_use = models.BooleanField()


class Tariff(models.Model):
    time_intervals = models.PositiveIntegerField('Тариф в месяцах')


class Order(models.Model):
    number = models.BigAutoField('Номер заказа')
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_orders')
    box = models.OneToOneField(
        Box,
        on_delete=models.PROTECT,
        related_name='box_orders',)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT,)
    start_date = models.DateTimeField('заказ от', auto_now_add=True)
    key = models.PositiveIntegerField('Ключ доступа')
