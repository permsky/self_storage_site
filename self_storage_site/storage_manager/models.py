from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, Min


User = get_user_model()


class BoxPlaceQuerySet(models.QuerySet):
    def get_free_boxes(self):
        free_boxes = self.annotate(free_boxes=Sum('place_boxes__in_use'))
        return free_boxes

    def get_min_price(self):
        min_price = self.annotate(min_price=Min('place_boxes__tariff'))
        return min_price


class BoxPlace(models.Model):
    name = models.CharField('Название боксангара', max_length=50)
    address = models.CharField('Адрес', max_length=100)
    boxes_quantity = models.PositiveIntegerField(
        'Общее количество боксов',
        default=1)
    note = models.CharField('Пимечание', max_length=100, blank=True)
    image = models.ImageField(
        'Изображение', upload_to='boxplaces', null=True, blank=True)
    temperature = models.IntegerField('Температура в боксах', default=18)
    objects = BoxPlaceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Ангар для боксов'
        verbose_name_plural = 'Ангары для боксов'

    def __str__(self):
        return self.name


class BoxVolume(models.Model):
    volume = models.FloatField(
        'Объем бокса в кубометрах',
        validators=[MinValueValidator(0.0)])

    class Meta:
        verbose_name = 'Объём бокса'
        verbose_name_plural = 'Объёмы боксов'

    def __str__(self):
        return str(self.volume)


class Box(models.Model):
    box_volume = models.ForeignKey(
        BoxVolume,
        on_delete=models.PROTECT,
        related_name='boxes',
        verbose_name='Объём бокса')
    in_use = models.PositiveSmallIntegerField(
        'Бокс использован',
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ])
    boxes_place = models.ForeignKey(
        BoxPlace,
        on_delete=models.PROTECT,
        related_name='place_boxes',
        verbose_name='Где находится')
    tariff = models.PositiveIntegerField('Цена аренды в месяц руб.')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'Бокс {self.pk} объёмом {self.box_volume} по адресу {self.boxes_place}'


class RentalTime(models.Model):
    time_intervals = models.PositiveIntegerField('Время аренды в месяцах')

    class Meta:
        verbose_name = 'Время аренды в месяцах'
        verbose_name_plural = 'Время аренды в месяцах'

    def __str__(self):
        return str(self.time_intervals)


class Order(models.Model):
    STATUSES = [
        (1, 'active'),
        (2, 'expired'),
        (3, 'closed')
    ]
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_orders',
        verbose_name='Имя клиента')
    box = models.OneToOneField(
        Box,
        on_delete=models.PROTECT,
        related_name='box_orders',
        verbose_name='Используемый бокс')
    rental_time = models.ForeignKey(
        RentalTime,
        on_delete=models.PROTECT,
        verbose_name='Время аренды')
    start_date = models.DateTimeField('заказ от', auto_now_add=True)
    end_date = models.DateTimeField('заказ до')
    access_code = models.PositiveIntegerField('код доступа к ячейке', default=213456789)
    status = models.CharField(
        'статус заказа',
        choices=STATUSES,
        max_length=10
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.pk} клиента {self.customer.first_name} от {str(self.start_date)}'


class Job(models.Model):
    STATUSES = [
        (1, 'new'),
        (2, 'ready'),
        (3, 'done')
    ]
    INTERVALS=[
        (1, 'месяц'),
        (2, '2 недели'),
        (3, '1 неделю'),
        (4, '3 дня'),
        (5, '6 месяцев'),
        (6, '5 месяцев'),
        (7, '4 месяца'),
        (8, '3 месяца'),
        (9, '2 месяца'),
        (10, '1 месяц'),
    ]
    status = models.CharField(
        'статус задачи',
        choices=STATUSES,
        max_length=10
    )
    date_to_run = models.DateField('дата запуска')
    interval = models.CharField(
        'осталось времени',
        choices=INTERVALS,
        max_length=100
    )
    with_qrcode = models.BooleanField('отправлять qr-код', default=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    
    def __str__(self):
        return f'Задача на отправку почты по заказу с id: {self.order.id}'
