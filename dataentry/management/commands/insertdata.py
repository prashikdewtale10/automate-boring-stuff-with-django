"""
insertdata.py
-------------
"""

from django.core.management.base import BaseCommand

from dataentry.models import Student


class Command(BaseCommand):
    help: str = "This command inserts data in students db"

    def handle(self, *args, **options):
        # Adding multiple records
        dataset = [
            {"roll_no": "0002", "name": "John Doe", "age": 27},
            {"roll_no": "0003", "name": "Thomson Cook", "age": 26},
        ]
        for data in dataset:
            roll_no = data["roll_no"]
            if not Student.objects.filter(roll_no=roll_no).exists():
                Student.objects.create(
                    roll_no=roll_no, name=data["name"], age=data["age"]
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Skipping student with roll number '%s', already exists!",  # noqa
                        str(roll_no),
                    )
                )

        self.stdout.write(self.style.SUCCESS("Data inserted successfully."))
