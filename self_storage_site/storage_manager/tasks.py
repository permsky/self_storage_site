from datetime import datetime, timedelta
from pathlib import Path

import dramatiq
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from loguru import logger

import self_storage_site.settings
from .models import Job, Order


@dramatiq.actor()
def send_email_to_customer(
    email_address,
    stored_until,
    interval,
    image_path=None
):
    intervals_before = (
        'месяц',
        '2 недели',
        'неделю',
        '3 дня',
    )
    intervals_after = (
        '1 месяц',
        '2 месяца',
        '3 месяца',
        '4 месяца',
        '5 месяцев',
        '6 месяцев',
    )
    if interval in intervals_before:
        message = f'''
        Через {interval} заканчивается срок хранения (до {stored_until}).
        Чтобы забрать вещи воспользуйтесь QR-кодом.
        '''
    if interval in intervals_after:
        message = f'''
        Срок хранения (до {stored_until}) закончился. Ваши вещи будут
        храниться еще {interval} по тарифу, увеличенному на 10%. Если не
        забрать вещи в течение данного периода, то они будут потеряны.
        '''
    
    email = EmailMultiAlternatives(
        subject='Оповещение от сервиса SelfStorage',
        body=message,
        from_email=self_storage_site.settings.EMAIL_HOST_USER,
        to=list(email_address)
    )
    if image_path:
        image_name = Path(image_path).name
        html_content = f'''
        <!doctype html>
            <html lang=en>
                <head>
                    <meta charset=utf-8>
                </head>
                <body>
                    <p>
                    QR-код для доступа к ячейке.<br>
                    <img src='cid:{image_name}'/>
                    </p>
                </body>
            </html>
        '''
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'
        with open(image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header('Content-ID', f"<{image_name}>")
    email.send()


@dramatiq.actor()
def process_job_status():
    logger.warning('Start task')
    new_jobs = Job.objects.filter(status='new')
    if new_jobs:
        for job in new_jobs:
            if job.date_to_run <= datetime.now().date():
                job.status = 'ready'
                job.save()
    logger.warning('Task is ended')


@dramatiq.actor()
def create_jobs():
    active_orders = Order.objects.filter(status='active')
    for order in active_orders:
        if order.end_date < datetime.now():
            interval = '6 месяцев'
            Job.objects.create(
                status='new',
                customer_email=order.customer_email,
                interval=interval,
                with_qrcode=False,
                date_to_run=datetime.now().date(),
                order=order
            )
            order.status = 'expired'
            order.save()
    logger.warning('Jobs created')
