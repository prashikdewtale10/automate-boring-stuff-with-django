"""
exportdata.py
-------------
"""

import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help: str = "Export data from specified model into csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            "-m",
            "--model-name",
            dest="model_name",
            help="Spefity model name",
            required=True,
            type=str,
        )

    def handle(self, *args, **options):
        # --- Getting model name ---
        model_name: str = options.get("model_name").capitalize()

        # --- Search for model in all the installed apps ---
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # Once model found break loop
            except LookupError:
                pass  # Continue searching for in another app

        if not model:
            raise CommandError(f"Model '{model_name}' not found in any app !")

        # --- Fetch the students data from db ---
        queryest = model.objects.all()

        # --- Generate the timestamp of current date and time ---
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # --- Define file_name or path ---
        file_path = f"exported_{model_name}_data_{timestamp}.csv"

        # ---- Storing data into file ---
        with open(
            file=file_path,
            mode="w",
            encoding="utf-8",
            newline="",
        ) as file:
            writter = csv.writer(file)

            # --- Getting models field name ---
            writter.writerow([field.name for field in model._meta.get_fields()])

            # Write rows data
            for data in queryest:
                writter.writerow(
                    [
                        getattr(data, field.name)
                        for field in model._meta.get_fields()  # noqa
                    ]
                )

        self.stdout.write(self.style.SUCCESS("Data exported successfully"))
