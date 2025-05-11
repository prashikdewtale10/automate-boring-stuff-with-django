"""
greeting.py
----------
"""

from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help: str = "Greets specified user"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Specify name")

    def handle(self, *args, **kwargs):
        name: str = kwargs.get("name")
        greeting_message: str = self.get_greeting_message()
        msg = f"Hello {name}, {greeting_message}"
        self.stdout.write(self.style.SUCCESS(msg))

    def get_greeting_message(self):
        current_time_hour = datetime.now().hour

        if 5 <= current_time_hour < 12:
            return "Good Morning !"
        elif 12 <= current_time_hour < 17:
            return "Good Afternoon !"
        elif 17 <= current_time_hour < 21:
            return "Good Evening !"
        else:
            return "Good Night !"
