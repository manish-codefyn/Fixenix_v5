import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run all device problem import commands in sequence."

    def handle(self, *args, **kwargs):
        commands = [
            "python manage.py add_devices",
            "python manage.py add_device_brands",
            "python manage.py add_device_models",
            "python manage.py add_device_problems",

            # Add more commands here if needed
        ]

        for cmd in commands:
            self.stdout.write(self.style.NOTICE(f"▶ Running: {cmd}"))
            try:
                subprocess.run(cmd, shell=True, check=True)
                self.stdout.write(self.style.SUCCESS(f"✅ Successfully ran: {cmd}"))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f"❌ Error running {cmd}: {e}"))

        self.stdout.write(self.style.SUCCESS("🚀 All problem import commands have been executed."))
