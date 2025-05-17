"""
hello_world.py
--------------
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str = "This is simple custom command, which prints hello-world"

    def handle(self, *args, **options):
        self.stdout.write("Hello-World")
