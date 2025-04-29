import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bookings.models import Device, DeviceBrand

class Command(BaseCommand):
    help = 'Import device brands from JSON file'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data/device_brands.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("device_brands.json file not found"))
            return

        with open(json_path, 'r') as file:
            device_brands_data = json.load(file)

        added = 0
        skipped = 0

        for device_type_name, brand_list in device_brands_data.items():
            device, created = Device.objects.get_or_create(name=device_type_name)

            for brand_name in brand_list:
                # Check if this brand already exists for this device
                if DeviceBrand.objects.filter(name=brand_name, device_type=device).exists():
                    skipped += 1
                    continue

                DeviceBrand.objects.create(name=brand_name, device_type=device)
                added += 1

        self.stdout.write(self.style.SUCCESS(f"{added} device brands added, {skipped} skipped (already exist)."))
