import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bookings.models import Device

class Command(BaseCommand):
    help = 'Imports device types from a JSON file'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data/devices.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("devices.json file not found"))
            return

        with open(json_path, 'r') as file:
            data = json.load(file)

        added = 0
        updated = 0

        for entry in data:
            name = entry.get("name")
            if not name:
                self.stdout.write(self.style.WARNING("Skipped empty device name"))
                continue

            device, created = Device.objects.get_or_create(name=name)
            if created:
                added += 1
            else:
                updated += 1  # In case you want to do more updates later

        self.stdout.write(self.style.SUCCESS(f"{added} devices added, {updated} already existed."))
