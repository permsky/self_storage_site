from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BlockingScheduler
import pytz

from apscheduler.triggers.cron import CronTrigger

from storage_manager.periodic_tasks import start_jobs


class Command(BaseCommand):
    help = 'Run blocking scheduler to create periodical tasks'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Preparing scheduler'))
        scheduler = BlockingScheduler(timezone=pytz.UTC)
        every_day_at_01_00_utc = CronTrigger(
            hour=19, minute=42,
            timezone=pytz.UTC
        )
        scheduler.add_job(start_jobs, every_day_at_01_00_utc)
        # ... add another jobs
        self.stdout.write(self.style.NOTICE('Start scheduler'))
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
