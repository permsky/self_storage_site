# Generated by Django 3.2.13 on 2022-06-17 16:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_use', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)], verbose_name='Бокс использован')),
                ('tariff', models.PositiveIntegerField(verbose_name='Цена аренды в месяц руб.')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
        migrations.CreateModel(
            name='BoxPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название боксангара')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('boxes_quantity', models.PositiveIntegerField(default=1, verbose_name='Общее количество боксов')),
                ('note', models.CharField(blank=True, max_length=100, verbose_name='Примечание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='boxplaces', verbose_name='Изображение')),
                ('temperature', models.IntegerField(default=18, verbose_name='Температура в боксах')),
                ('roof_height', models.FloatField(default=3.5, verbose_name='Высота ангара')),
            ],
            options={
                'verbose_name': 'Ангар для боксов',
                'verbose_name_plural': 'Ангары для боксов',
            },
        ),
        migrations.CreateModel(
            name='BoxVolume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Объем бокса в кубометрах')),
            ],
            options={
                'verbose_name': 'Объём бокса',
                'verbose_name_plural': 'Объёмы боксов',
            },
        ),
        migrations.CreateModel(
            name='CalculateCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_mail', models.EmailField(max_length=254, verbose_name='Почта заказчика расчета')),
            ],
            options={
                'verbose_name': 'Почта заказчика расчета',
                'verbose_name_plural': 'Почта заказчика расчета',
            },
        ),
        migrations.CreateModel(
            name='RentalTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_intervals', models.PositiveIntegerField(verbose_name='Время аренды в месяцах')),
            ],
            options={
                'verbose_name': 'Время аренды в месяцах',
                'verbose_name_plural': 'Время аренды в месяцах',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Фамилия')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, upload_to='', verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='заказ от')),
                ('end_date', models.DateField(verbose_name='заказ до')),
                ('access_code', models.PositiveIntegerField(default=213456789, verbose_name='код доступа к ячейке')),
                ('status', models.CharField(choices=[('active', 'active'), ('expired', 'expired'), ('closed', 'closed')], max_length=10, verbose_name='статус заказа')),
                ('box', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='box_orders', to='storage_manager.box', verbose_name='Используемый бокс')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_orders', to=settings.AUTH_USER_MODEL, verbose_name='Имя клиента')),
                ('rental_time', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storage_manager.rentaltime', verbose_name='Время аренды')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'new'), ('ready', 'ready'), ('done', 'done')], max_length=10, verbose_name='статус задачи')),
                ('date_to_run', models.DateField(verbose_name='дата запуска')),
                ('interval', models.CharField(choices=[('месяц', 'месяц'), ('2 недели', '2 недели'), ('1 неделю', '1 неделю'), ('3 дня', '3 дня'), ('6 месяцев', '6 месяцев'), ('5 месяцев', '5 месяцев'), ('4 месяца', '4 месяца'), ('3 месяца', '3 месяца'), ('2 месяца', '2 месяца'), ('1 месяц', '1 месяц')], max_length=100, verbose_name='осталось времени')),
                ('with_qrcode', models.BooleanField(default=True, verbose_name='отправлять qr-код')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='storage_manager.order')),
            ],
            options={
                'verbose_name': 'Оповещение',
                'verbose_name_plural': 'Оповещения',
            },
        ),
        migrations.AddField(
            model_name='box',
            name='box_volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='boxes', to='storage_manager.boxvolume', verbose_name='Объём бокса'),
        ),
        migrations.AddField(
            model_name='box',
            name='boxes_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='place_boxes', to='storage_manager.boxplace', verbose_name='Где находится'),
        ),
    ]
