from django.db import models
import uuid
from django.urls import reverse
import datetime
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, RegexValidator

def gen_work_id():
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD
    unique_id = str(uuid.uuid4()).split("-")[1].upper()  # Extract part of UUID
    work_id = f"JOB-{current_date}-{unique_id}"
    return work_id

class WorkSheet(models.Model):
    """Improved Worksheet Model"""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Delivered', 'Delivered'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(3)]
    )
    mobile = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(10),
            RegexValidator(
                regex='^[0-9]*$',
                message='Mobile number must contain only digits'
            )
        ]
    )
    email = models.EmailField()
    device_name = models.CharField(max_length=100)
    device_problem = models.TextField()  # Changed to TextField for longer descriptions
    problem_details = models.TextField(blank=True, null=True)  # Additional details
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    work_id = models.CharField(
        max_length=255,
        unique=True,
        editable=False
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def __str__(self):
        return f"{self.work_id} - {self.name} - {self.device_name}"
    
    def save(self, *args, **kwargs):
        if not self.work_id:
            self.work_id = f"WS-{uuid.uuid4().hex[:6].upper()}"
        if not self.slug:
            self.slug = slugify(f"{self.work_id}-{self.device_name}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("worksheet-detail", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["id"], name="id_index"),
            models.Index(fields=["work_id"], name="work_id_index"),
            models.Index(fields=["status"], name="status_index"),
        ]
        verbose_name = "Work Sheet"
        verbose_name_plural = "Work Sheets"