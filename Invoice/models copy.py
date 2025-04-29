from django.db import models
import uuid
from django.urls import reverse
import datetime

def invoice_no():
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD
    unique_id = str(uuid.uuid4()).split("-")[1].upper()
    invoice_number = f"INV-{current_date}-{unique_id}"
    return invoice_number

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Paid", "Paid"),
)


class Invoice(models.Model):
    """Worksheet Create Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    product_detail = models.CharField(max_length=255)
    amount = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoice_no = models.CharField(
        max_length=255, default=invoice_no, unique=True, editable=False
    )
    payment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse("invoice", args=[str(self.id)])
