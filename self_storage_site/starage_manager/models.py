from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Order (models.Model):
    number = models.BigAutoField('Номер заказа')
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders')
    box = ...
    tariff = ...
    start_date = models.DateTimeField('заказ от', auto_now_add=True)
    key = models.PositiveIntegerField('Ключ доступа')
