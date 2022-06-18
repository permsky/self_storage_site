import os
import random
from datetime import datetime
from pathlib import Path
from storage_manager.models import CalculateCustomer
import qrcode

import self_storage_site.settings


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

