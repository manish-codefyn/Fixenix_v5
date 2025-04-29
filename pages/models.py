from django.db import models
import uuid
from django.urls import reverse

class PartnerApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    interest_reason = models.TextField(blank=True, null=True)
    agree_terms = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("dashboard:partnership", args=[str(self.id)])

class FeedBack(models.Model):
    """Feedback"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50)
    rating = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("dashboard:feedback", args=[str(self.id)])


class ContactUs(models.Model):
    """Contact form"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("msg", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Contact Us"


class EstimateRequests(models.Model):
    """Request Create Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    email = models.EmailField()
    device_name = models.CharField(max_length=100)
    device_problem = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dashboard:estimate_requests", args=[str(self.id)])

    

