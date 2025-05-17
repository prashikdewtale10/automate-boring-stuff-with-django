"""
importdata.py
-------------
"""

import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help: str = "Import data from csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--file-path",
            dest="file_path",
            help="Spefity csv file path",
            required=True,
        )
        parser.add_argument(
            "-m",
            "--model-name",
            dest="model_name",
            help="Spefity model name",
            required=True,
        )

    def handle(self, *args, **options):
        file_path = options.get("file_path")
        model_name = options.get("model_name")

        # --- Search for model across all installed apps ---
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(
                    app_label=app_config.label, model_name=model_name
                )
            except LookupError:
                # --- if model not found in this app, continue searching ---
                continue

        if not model:
            raise CommandError(f"Model '{model_name}' not found in any app !")

        # --- Converting csv to dict of object ---
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(
            self.style.SUCCESS("Data imported from csv successfully.")
        )  # noqa
