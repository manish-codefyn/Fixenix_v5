import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bookings.models import DeviceModel, DeviceProblem


class Command(BaseCommand):
    help = 'Attach device problems to every device model'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data/device_problems.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("device_problems.json file not found in /data"))
            return

        with open(json_path, 'r') as file:
            data = json.load(file)

        # Fix: now reads the correct key "description"
        problems_list = data.get("description", [])
        if not problems_list:
            self.stdout.write(self.style.WARNING("No problems found under 'description' key in the JSON file"))
            return

        added = 0
        skipped = 0
        all_models = DeviceModel.objects.all()

        for model in all_models:
            for problem_text in problems_list:
                problem_text = problem_text.strip()
                if not problem_text:
                    continue

                exists = DeviceProblem.objects.filter(
                    description=problem_text,
                    device_model=model
                ).exists()

                if not exists:
                    DeviceProblem.objects.create(
                        description=problem_text,
                        device_model=model
                    )
                    added += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ device problems added to models.\n"
            f"- Total problems added: {added}\n"
            f"- Skipped duplicates: {skipped}"
        ))
