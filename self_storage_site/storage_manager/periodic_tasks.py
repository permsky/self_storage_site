from loguru import logger

from .models import Job
from .tasks import process_job_status, send_email_to_customer, create_jobs
from .utils import create_qrcode


def start_jobs():
    """
    This task will be run by APScheduler. It can prepare some
    data and parameters and then enqueue background task.
    """
    logger.warning('It is time to start the dramatiq task')
    current_jobs = Job.objects.filter(status='ready')
    for job in current_jobs:
        stored_until = job.order.end_date.strftime('%d.%m.%Y')
        email_address = job.order.customer.email
        interval = job.interval
        if job.with_qrcode:
            send_email_to_customer.send(
                email_address=email_address,
                stored_until=stored_until,
                interval=interval,
                image_path=create_qrcode(job.order.access_code)
            )
        else:
            send_email_to_customer.send(
                email_address=email_address,
                stored_until=stored_until,
                interval=interval
            )
        job.status = 'done'
        job.save()

    process_job_status.send()

    create_jobs.send()
