# Generated by Django 3.2.13 on 2022-06-16 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_manager', '0002_boxplace_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxplace',
            name='temperature',
            field=models.IntegerField(default=18, verbose_name='Температура в боксах'),
        ),
    ]
