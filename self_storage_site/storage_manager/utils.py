import json
import os
import random
import qrcode
from datetime import datetime
from pathlib import Path

import self_storage_site.settings
from storage_manager.models import (
    BoxPlace,
    BoxVolume,
    Box,
    RentalTime,
    CalculateCustomer
)


def read_from_json(filepath):
            with open(filepath, encoding='UTF-8', mode='r') as f:
                return json.loads(f.read())


def fill_database(filepath):
    storages = read_from_json(filepath)
    for item in storages:
        if item['type'] == 'box_volumes':
            for volume in item['box_volumes']:
                BoxVolume.objects.get_or_create(volume=volume)
        if item['type'] == 'rental_time':
            for time in item['rental_time']:
                RentalTime.objects.get_or_create(time_intervals=time)
        if item['type'] == 'box_places':
            for storage in item['box_places']:
                box_place = BoxPlace.objects.get_or_create(
                    name=storage['name'],
                    address=storage['address'],
                    boxes_quantity=storage['boxes_quantity'],
                    note=storage['note'],
                )
                box_sizes = storage['box_sizes']
                for box_size in box_sizes:
                    count_and_price = box_sizes[box_size]
                    for box in range(count_and_price[0]):
                        box_volume = BoxVolume.objects.get(volume=int(box_size))
                        Box.objects.create(
                            box_volume=box_volume,
                            boxes_place=box_place[0],
                            tariff=count_and_price[1]
                        )


def create_qrcode(code):
    qrcode_image = qrcode.make(code)
    qrcodes_path = os.path.join(
        self_storage_site.settings.BASE_DIR / 'qrcodes'
    )
    filename = f'qr{int(datetime.now().timestamp())}'
    suffix = '.jpg'
    Path(qrcodes_path).mkdir(exist_ok=True)
    image_path = str(Path(qrcodes_path, filename).with_suffix(suffix))
    qrcode_image.save(image_path)
    return image_path


def randomise_from_range(stop):
    return random.randrange(stop)


def get_email(request):
    customer_mail = request.GET.get('EMAIL1')
    CalculateCustomer.objects.get_or_create(
        customer_mail=customer_mail)
    print(customer_mail)
