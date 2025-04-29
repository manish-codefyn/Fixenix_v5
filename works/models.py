from django.db import models
import uuid
from django.urls import reverse
import datetime
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


def gen_work_id():
    """Generate formatted work ID: WS-YYYYMMDD-UUID_PART"""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4()).split("-")[1].upper()
    return f"WS-{current_date}-{unique_id}"

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
        max_length=255, default=gen_work_id, unique=True, editable=False
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def __str__(self):
        return f"{self.work_id} - {self.name} - {self.device_name}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('work_sheet_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        from django.urls import reverse
        return reverse('work_sheet_update', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """Ensure slug is generated even when created via bulk operations"""
        if not self.slug:
            base_slug = slugify(f"{self.work_id}-{self.device_name}")
            self.slug = base_slug
            
            # Handle potential duplicates
            counter = 1
            while WorkSheet.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)


    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["id"], name="id_index"),
            models.Index(fields=["work_id"], name="work_id_index"),
            models.Index(fields=["status"], name="status_index"),
        ]
        verbose_name = "Work Sheet"
        verbose_name_plural = "Work Sheets"


class DeviceChecklist(models.Model):
    """Checklist for each device component with selectable names and Yes/No choices."""

    COMPONENT_CHOICES = [
        ('Mic', 'Mic'),
        ('Camera', 'Camera'),
        ('Speaker', 'Speaker'),
        ('Display', 'Display'),
        ('Touchscreen', 'Touchscreen'),
        ('Charging Port', 'Charging Port'),
        ('Battery', 'Battery'),
        ('Volume Buttons', 'Volume Buttons'),
        ('Power Button', 'Power Button'),
        ('WiFi', 'WiFi'),
        ('Bluetooth', 'Bluetooth'),
        ('Headphone Jack', 'Headphone Jack'),
        ('Fingerprint Sensor', 'Fingerprint Sensor'),
        ('Face ID', 'Face ID'),
        # Add more as needed
    ]

    WORKING_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    worksheet = models.ForeignKey(WorkSheet, related_name='checklist_items', on_delete=models.CASCADE)
    component_name = models.CharField(max_length=50, choices=COMPONENT_CHOICES)
    is_working = models.BooleanField(choices=WORKING_CHOICES, default=True)

    def __str__(self):
        return f"{self.component_name} - {'Yes' if self.is_working else 'No'}"