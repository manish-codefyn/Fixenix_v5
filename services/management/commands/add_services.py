import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from services.models import DoorstepService

class Command(BaseCommand):
    help = 'Imports doorstep services from a JSON file and updates existing ones if changed'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data/services.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("services.json file not found in /data/"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        added = 0
        updated = 0

        for entry in data:
            fields = entry.get("fields", {})
            service_name = fields.get("service_name")

            if not service_name:
                self.stdout.write(self.style.WARNING("Skipped: Missing service_name"))
                continue

            defaults = {
                "price": fields.get("price", 0.0),
                "offer_price": fields.get("offer_price", None),
                "is_available": fields.get("is_available", True),
                "is_premium": fields.get("is_premium", False),
                "is_discountable": fields.get("is_discountable", False),
                "is_featured": fields.get("is_featured", False),
                "features": fields.get("features", ""),
                "status": fields.get("status", "active"),
                "image": fields.get("image", None),
            }

            try:
                service = DoorstepService.objects.get(service_name=service_name)
                changes = []
                for field, new_value in defaults.items():
                    old_value = getattr(service, field)
                    # Handle image field which is a FileField
                    if field == "image" and old_value:
                        old_value = str(old_value)

                    if old_value != new_value:
                        setattr(service, field, new_value)
                        changes.append(f"{field}: {old_value} → {new_value}")

                if changes:
                    service.save()
                    updated += 1
                    self.stdout.write(self.style.WARNING(f"Updated '{service_name}':"))
                    for change in changes:
                        self.stdout.write(f"  - {change}")
                else:
                    self.stdout.write(f"No changes for '{service_name}'")

            except DoorstepService.DoesNotExist:
                # Create new service
                service = DoorstepService.objects.create(service_name=service_name, **defaults)
                added += 1
                self.stdout.write(self.style.SUCCESS(f"Added new service: {service_name}"))

        self.stdout.write(self.style.SUCCESS(f"\nSummary: {added} added, {updated} updated."))
