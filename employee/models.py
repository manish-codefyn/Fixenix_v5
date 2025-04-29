from django.db import models
import uuid
import random
from django.urls import reverse

class Employee(models.Model):
    EXPERIENCE_CHOICES = [(i, f"{i} years") for i in range(1, 31)]  # Choices from 1 to 30 years

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proofs/')
    photo = models.FileField(upload_to='id_proofs/')
    experience = models.PositiveIntegerField(choices=EXPERIENCE_CHOICES, default=1, help_text="Years of experience")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Monthly salary in USD")
    current_location_lat = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    current_location_lon = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    employee_id = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
        blank=True,
        help_text="Unique employee ID with prefix"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    def save(self, *args, **kwargs):
        """Override save method to ensure a unique employee ID is assigned."""
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dashboard:employees", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Employees"

    def generate_employee_id(self):
        """Generate a unique employee ID with a prefix."""
        prefix = "FTS"  # Define your prefix here
        for _ in range(10):  # Retry up to 10 times to avoid collisions
            unique_id = str(random.randint(10**9, 10**10 - 1))  # Generate a 10-digit ID
            employee_id = f"{prefix}{unique_id}"
            if not Employee.objects.filter(employee_id=employee_id).exists():
                return employee_id
        raise ValueError("Failed to generate a unique employee ID after 10 attempts.")
