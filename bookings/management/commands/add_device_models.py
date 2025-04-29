import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bookings.models import Device, DeviceBrand, DeviceModel


class Command(BaseCommand):
    help = 'Imports device categories, brands, and models from nested JSON'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data/device_models.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("device_models.json file not found in /data"))
            return

        with open(json_path, 'r') as file:
            data = json.load(file)

        added_categories = 0
        added_brands = 0
        added_models = 0

        for category_name, brands in data.items():
            # Get or create Device (category)
            category, created = Device.objects.get_or_create(name=category_name.strip())
            if created:
                added_categories += 1

            for brand_name, models in brands.items():
                # Get or create Brand
                brand, brand_created = DeviceBrand.objects.get_or_create(
                    name=brand_name.strip(),
                    device_type=category
                )
                if brand_created:
                    added_brands += 1

                for model_name in models:
                    model_name = model_name.strip()
                    if not model_name:
                        continue

                    # Avoid duplicate models
                    exists = DeviceModel.objects.filter(
                        name=model_name,
                        device_type=category,
                        device_brand=brand
                    ).exists()

                    if not exists:
                        DeviceModel.objects.create(
                            name=model_name,
                            device_type=category,
                            device_brand=brand
                        )
                        added_models += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import Complete!\n"
            f"- Categories added: {added_categories}\n"
            f"- Brands added: {added_brands}\n"
            f"- Models added: {added_models}"
        ))
