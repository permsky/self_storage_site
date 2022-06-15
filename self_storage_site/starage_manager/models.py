from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class BoxPlace(models.Model):
    name = models.CharField('Название боксангара', max_length=50)
    address = models.CharField('Адрес', max_length=100)
    boxes_quantity = models.PositiveIntegerField(
        'Общее количество боксов',
        default=1)
    note = models.CharField('Пимечание', max_length=100, blank=True)


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
    boxes_place = models.ForeignKey(
        BoxPlace,
        on_delete=models.PROTECT,
        related_name='place_boxes',
        verbose_name='Где находится')
    tariff = models.PositiveIntegerField('Цена аренды в месяц')


class RentalTime(models.Model):
    time_intervals = models.PositiveIntegerField('Время аренды в месяцах')

    class Meta:
        verbose_name = 'Время аренды в месяцах'
        verbose_name_plural = 'Время аренды в месяцах'

    def __str__(self):
        return str(self.time_intervals)


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_orders')
    box = models.OneToOneField(
        Box,
        on_delete=models.PROTECT,
        related_name='box_orders',)
    rental_time = models.ForeignKey(RentalTime, on_delete=models.PROTECT, )
    start_date = models.DateTimeField('заказ от', auto_now_add=True)
    end_date = models.DateTimeField('заказ до')
    key = models.PositiveIntegerField('Ключ доступа')
