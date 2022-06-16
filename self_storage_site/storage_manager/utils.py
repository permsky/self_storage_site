import os
from datetime import datetime
from pathlib import Path

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