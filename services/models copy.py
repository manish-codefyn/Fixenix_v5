import uuid
from django.db import models
from django.conf import settings

from django.db import models
import uuid
from django.conf import settings

class DoorstepService(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True, help_text="Upload an image or icon for this service.")
    # description = models.TextField()
    status = models.CharField(max_length=20, choices=SERVICE_STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Original price of the service")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discounted price of the service (if any)")
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} ({self.status})"

    def get_final_price(self):
        """
        Returns the offer price if available, else returns the original price.
        """
        return self.offer_price if self.offer_price is not None else self.price

