from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .models import WorkSheet


class WorkSheetTests(TestCase):
    def setUp(self):
        self.ors = WorkSheet.objects.create(
            name="manish",
            email="manish@gmail.com",
            mobile="1234567890",
            device_name="One Plus",
            device_problem="Display",
            status="pending",
            work_id="FAee21",
        )
        url = reverse("work_sheet_list")
        self.response = self.client.get(url)

    def test_worksheet_listing(self):
        self.assertEqual(f"{self.ors.name}", "manish")
        self.assertEqual(f"{self.ors.email}", "manish@gmail.com")
        self.assertEqual(f"{self.ors.mobile}", "1234567890")
        self.assertEqual(f"{self.ors.device_name}", "One Plus")
        self.assertEqual(f"{self.ors.device_problem}", "Display")
        self.assertEqual(f"{self.ors.status}", "pending")
        self.assertEqual(f"{self.ors.work_id}", "FAee21")
