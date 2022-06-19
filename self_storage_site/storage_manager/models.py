from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


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
    note = models.CharField('Примечание', max_length=100, blank=True)
    image = models.ImageField(
        'Изображение', upload_to='boxplaces', null=True, blank=True)
    temperature = models.IntegerField('Температура в боксах', default=18)
    roof_height = models.FloatField('Высота ангара', default=3.5)
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
    in_use = models.BooleanField(
        'Бокс в аренде',
        default=False,
    )
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
        ('active', 'active'),
        ('expired', 'expired'),
        ('closed', 'closed')
    ]
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
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
    start_date = models.DateField('заказ от')
    end_date = models.DateField('заказ до')
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        intervals = [
            'месяц',
            '2 недели',
            'неделю',
            '3 дня',
        ]
        deltas = {
            'месяц': timedelta(days=30),
            '2 недели': timedelta(days=14),
            'неделю': timedelta(days=7),
            '3 дня': timedelta(days=3),
        }
        for interval in intervals:
            date_to_run = self.end_date - deltas[interval]
            Job.objects.create(
                status='new',
                interval=interval,
                with_qrcode=True,
                date_to_run=date_to_run,
                order=self
            )
        self.box.in_use = True
        self.box.save()


class Job(models.Model):
    STATUSES = [
        ('new', 'new'),
        ('ready', 'ready'),
        ('done', 'done')
    ]
    INTERVALS=[
        ('месяц', 'месяц'),
        ('2 недели', '2 недели'),
        ('1 неделю', '1 неделю'),
        ('3 дня', '3 дня'),
        ('6 месяцев', '6 месяцев'),
        ('5 месяцев', '5 месяцев'),
        ('4 месяца', '4 месяца'),
        ('3 месяца', '3 месяца'),
        ('2 месяца', '2 месяца'),
        ('1 месяц', '1 месяц'),
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
    
    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'
    
    def __str__(self):
        return f'Задача на отправку оповещения по заказу с id: {self.order.id}'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        'Имя',
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=30,
        blank=True
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        blank=True)
    avatar = models.ImageField(
        'Аватар',
        blank=True)

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user} {self.first_name} {self.last_name}'


class CalculateCustomer(models.Model):
    customer_mail = models.EmailField('Почта заказчика расчета', max_length=254)

    class Meta:
        verbose_name = 'Почта заказчика расчета'
        verbose_name_plural = 'Почта заказчика расчета'

    def __str__(self):
        return self.customer_mail
