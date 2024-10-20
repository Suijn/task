import csv

import structlog
from django.core.management.base import BaseCommand

from task.apps.prefixes.models import PrefixRaw
from task.apps.prefixes.services import map_items_to_prefixes

logger = structlog.get_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        log = logger.bind(command="prefixes")
        log.info("Running")

        prefixes: list[PrefixRaw] = []
        with open("data/names.csv", newline="") as f:
            reader = csv.DictReader(f, fieldnames=["name"])
            for row in reader:
                prefixes.append(PrefixRaw(name=row["name"]))

        map_items_to_prefixes(prefixes)

        log.info("Finished")
