from django.db import models
import uuid
from django.urls import reverse
from django.utils.timezone import now
import random
import string

def generate_invoice_no():
    """
    Generates a 16-character invoice number like: INV250409153012A7
    (INV + YYMMDDHHMM + 3 random alphanumerics)
    """
    timestamp = now().strftime("%y%m%d%H%M")  # e.g., 2504091530 (YYMMDDHHMM)
    rand_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"INV{timestamp}{rand_suffix}"

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Paid", "Paid"),
)


class Invoice(models.Model):
    """Invoice Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    invoice_date = models.DateField(default=now)
    due_date = models.DateField()
    product_details = models.JSONField(default=list)  # Stores list of products
    subtotal = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    notes = models.TextField(
        null=True,
        blank=True,
        default="Thank you for your business. If you have any questions, feel free to contact us."
    )
    
    terms = models.TextField(
            null=True,
            blank=True,
            default="Payment is due within 7 days. Late payments may be subject to a late fee."
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoice_no = models.CharField(
        max_length=255,
        default=generate_invoice_no,
        unique=True,
        editable=False
    )
    payment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    def __str__(self):
        return f"Invoice #{self.invoice_no} - {self.customer_name}"

    class Meta:
        ordering = ['-invoice_date']

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse("invoice", args=[str(self.id)])
