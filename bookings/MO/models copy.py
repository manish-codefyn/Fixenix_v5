import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from services.models import DoorstepService
import random
from django.contrib.auth import get_user_model
from employee.models import Employee
User = get_user_model()

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

CITY_CHOICES = [
        ('Siliguri', 'Siliguri'),
        ('Darjeeling', 'Darjeeling'),
        ('Jalpaiguri', 'Jalpaiguri'),
        ('Kalimpong', 'Kalimpong'),
    ]

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class DeviceBrand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="brands")

    def __str__(self):
        return self.name

class DeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE, related_name="models")

    def __str__(self):
        return f"{self.name} ({self.device_brand.name})"
    

class DeviceProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, related_name="problems")

    def __str__(self):
        return f"{self.description} ({self.device_model.name})"
  

class RepairService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="repairs")
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE, related_name="repairs")
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, related_name="repairs")
    device_problem = models.ForeignKey(DeviceProblem, on_delete=models.CASCADE, related_name="repairs")
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Repair Request for {self.device_name.name}"




class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(
        'Booking', 
        on_delete=models.CASCADE, 
        related_name="review"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="Rate the service between 1 (worst) and 5 (best)."
    )
    comment = models.TextField(blank=True, null=True, help_text="Optional comment about the service.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.service.name} by {self.booking.user.username} - {self.rating} Stars"
    



class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        'services.DoorstepService', on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    address = models.TextField()
    distance = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Distance in kilometers"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price for the service", default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completion_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    assigned_employee = models.ForeignKey(
        Employee,  # Referencing the Employee model
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_bookings"  # Reverse lookup to get all bookings assigned to an employee
    )
    booking_id = models.CharField(
        max_length=15, 
        unique=True, 
        editable=False, 
        blank=True, 
        help_text="Unique 10-15 digit booking ID"
    )

    def __str__(self):
        return f"{self.customer_name} - {self.booking_id}"

    def save(self, *args, **kwargs):
        """Override save method to ensure a unique booking ID is assigned."""
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()

        # If the employee is assigned and the booking is saved, send the email
        if self.assigned_employee and not self.pk:  # Ensure it only sends once, not on updates
            self.send_assignment_email()

        super().save(*args, **kwargs)

    def generate_booking_id(self):
        """Generate a unique 10-15 digit booking ID."""
        for _ in range(10):  # Retry up to 10 times to avoid collisions
            booking_id = str(random.randint(10**9, 10**15 - 1))  # Generate a 10-15 digit ID
            if not Booking.objects.filter(booking_id=booking_id).exists():
                return booking_id
        raise ValueError("Failed to generate a unique booking ID after 10 attempts.")

    def send_assignment_email(self):
        """Send an email notification to the assigned employee."""
        subject = f"New Booking Assigned: {self.booking_id}"
        message = f"""
        Hello {self.assigned_employee.name},

        You have been assigned a new booking. Here are the details:

        Booking ID: {self.booking_id}
        Customer Name: {self.customer_name}
        Customer Email: {self.customer_email}
        Customer Phone: {self.customer_phone}
        Address: {self.address}
        Distance: {self.distance} km
        Price: {self.price} INR

        Please review the booking and take the necessary actions.

        Best regards,
        Your Service Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email
            [self.assigned_employee.email],  # Recipient's email (Employee's email)
            fail_silently=False,
        )

    def track_status(self):
        """Return a human-readable status."""
        return f"Booking ID: {self.booking_id}, Status: {self.get_completion_status_display()}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("success", "Success"), ("failed", "Failed")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_status} for Booking {self.booking.id}"
