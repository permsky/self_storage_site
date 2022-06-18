import json
from django.core.management.base import BaseCommand

from storage_manager.utils import fill_database


class Command(BaseCommand):
    def handle(self, *args, **options):
        storages_filepath = 'storages.json'

        fill_database(storages_filepath)