from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from django.urls import reverse_lazy, reverse


class DoorstepService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True, help_text="Upload an image or icon for this service.")
    # Price-related fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Original price of the service")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discounted price of the service (if any)")
    # Availability and features
    is_available = models.BooleanField(default=True, help_text="Whether the service is currently available.")
    is_premium = models.BooleanField(default=False, help_text="Whether this is a premium service.")
    is_discountable = models.BooleanField(default=False, help_text="Whether discounts are applicable to this service.")
    is_featured = models.BooleanField(default=False, help_text="Highlight this service as featured.")
    # New fields
    features = models.TextField(null=True, blank=True, help_text="List the key features of this service.")
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active', help_text="Current status of the service.")
    # Ratings and reviews
    rating = models.FloatField(
        default=0.0,
        help_text="Average rating of the service.",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    review_count = models.PositiveIntegerField(default=0, help_text="Number of reviews for the service.")
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} (Available: {self.is_available})"
    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})
    
    def get_final_price(self):
        """
        Returns the offer price if available, else returns the original price.
        """
        return self.offer_price if self.offer_price is not None else self.price

    def calculate_rating(self, new_rating):
        """
        Update the average rating with a new rating value.
        """
        total_rating = self.rating * self.review_count
        self.review_count += 1
        self.rating = (total_rating + new_rating) / self.review_count
        self.save()
