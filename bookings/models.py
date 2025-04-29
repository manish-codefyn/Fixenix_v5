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
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('custom')

CITY_CHOICES = [
        ('Siliguri', 'Siliguri'),
        ('Darjeeling', 'Darjeeling'),
        ('Jalpaiguri', 'Jalpaiguri'),
        ('Kalimpong', 'Kalimpong'),
    ]

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class DeviceBrand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    device_type = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="brands")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class DeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    device_type = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="models")
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE, related_name="models")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.device_brand.name})"
    

class DeviceProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, related_name="problems")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.description} ({self.device_model.name})"
  

class RepairService(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('waiting', 'Waiting for Pickup'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="repairs")
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE, related_name="repairs")
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, related_name="repairs")
    device_problem = models.ForeignKey(DeviceProblem, on_delete=models.CASCADE, related_name="repairs")
    device_others_problem = models.TextField(blank=True, null=True, help_text="Optional about the device related problems.")
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    otp_verified = models.BooleanField(default=False)
    request_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
    # Only check for status updates if the instance already exists
        if self.pk:
            try:
            # Fetch the original instance
                original = RepairService.objects.get(id=self.pk)
            # Compare the status to check if it's being updated
                if original.status != self.status:
                    self.send_status_update_email()
            except RepairService.DoesNotExist:
            # Handle the edge case where the object does not exist
                pass

    # Assign a request ID if it doesn't exist
        if not self.request_id:
            self.request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"

    # Save the instance
        super().save(*args, **kwargs)

    def send_status_update_email(self):
        # Email Template Context
        context = {
            'customer_name': self.customer_name,
            'request_id': self.request_id,
            'status': self.get_status_display(),
            'company_name': 'Fixenix',  # Replace with your company name
            'company_contact': '+917992351609',  # Replace with your contact number
            'company_website': 'https://fixenix.com/',  # Replace with your website URL
            'terms_conditions_link': 'https://fixenix.com/terms-conditions/'  # Replace with your terms & conditions link
        }

        # Render the email content using the template
        subject = f"Repair Request Status Update - {self.request_id}"
        message = render_to_string('emails/repair_status_update.html', context)
        from_email = settings.DEFAULT_FROM_EMAIL

        # Send the email as HTML
        send_mail(
            subject, 
            message, 
            from_email, 
            [self.email], 
            html_message=message
        )

    def __str__(self):
        return f"Repair Request for {self.device.name} - Status: {self.get_status_display()}"


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
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
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
        max_length=20, 
        unique=True, 
        editable=False, 
        blank=True, 
        help_text="Unique 17-20 digit booking ID"
    )

    def __str__(self):
        return f"{self.customer_name} - {self.booking_id}"

    def save(self, *args, **kwargs):
        """Override save method to ensure a unique booking ID is assigned."""
        is_new = not self.pk  # Check if this is a new object
        original_status = None
        original_employee = None

        # Fetch the original instance for comparison only if the object is not new
        if not is_new:
            try:
                original = Booking.objects.get(pk=self.pk)
                original_status = original.status
                original_employee = original.assigned_employee
            except Booking.DoesNotExist:
                original_status = None  # Fallback in case the instance is not found
                original_employee = None

        # Assign booking ID if not already assigned
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()

        # Save the instance first
        super().save(*args, **kwargs)

        # Send notification emails
        try:
            if is_new:
                self.send_new_booking_email()
            else:
                if original_status != self.status:
                    self.send_status_update_email()
                if original_employee != self.assigned_employee and self.assigned_employee:
                    self.send_assignment_email_to_employee()
                    self.send_assignment_email_to_customer()
        except Exception as e:
            logger.error(f"Error in email notifications: {e}")
            raise

    def send_new_booking_email(self):
        """Send an email notification for new bookings using a modern HTML template."""
        subject = f"New Booking Confirmed: {self.booking_id}"

        # Render the HTML template with the necessary context
        context = {
        'customer_name': self.customer_name,
        'booking_id': self.booking_id,
        'service_name': self.service.service_name,
        'address': self.address,
        'distance': self.distance,
        'price': self.price,
          }
        html_message = render_to_string('emails/new_booking_email.html', context)

        send_mail(
        subject=subject,
        message="Your booking has been confirmed. Please find the details below.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[self.customer_email],
        fail_silently=False,
        html_message=html_message,  # Send HTML version of the email
        )


    def send_assignment_email_to_employee(self):
        """Send an email notification to the assigned employee using a modern HTML template."""
        subject = f"New Booking Assigned: {self.booking_id}"
    
        # Render the HTML template with the necessary context
        context = {
        'employee_name': self.assigned_employee.name,
        'booking_id': self.booking_id,
        'customer_name': self.customer_name,
        'customer_email': self.customer_email,
        'customer_phone': self.customer_phone,
        'address': self.address,
        'distance': self.distance,
        'price': self.price,
          }
        html_message = render_to_string('emails/assignment_email_to_employee.html', context)

        send_mail(
        subject=subject,
        message="A new booking has been assigned to you. Please find the details below.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[self.assigned_employee.email],
        fail_silently=False,
        html_message=html_message,  # Send HTML version of the email
        )


    def send_assignment_email_to_customer(self):
        """Send an email notification to the customer with the assigned employee details using a modern HTML template."""
        subject = f"Your Booking is Assigned: {self.booking_id}"
    
    # Render the HTML template with the necessary context
        context = {
        'customer_name': self.customer_name,
        'booking_id': self.booking_id,
        'employee_name': self.assigned_employee.name,
        'employee_email': self.assigned_employee.email,
        'employee_phone': self.assigned_employee.phone,
        }
        html_message = render_to_string('emails/assignment_email_to_customer.html', context)

        send_mail(
        subject=subject,
        message="Your booking has been assigned to an employee. Please find details attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[self.customer_email],
        fail_silently=False,
        html_message=html_message,  # Send HTML version of the email
        )



    def send_status_update_email(self):
        """Send an email notification for status updates with a modern HTML template."""
        subject = f"Booking Status Updated: {self.booking_id}"
    
    # Render the HTML template with the necessary context
        context = {
        'customer_name': self.customer_name,
        'booking_id': self.booking_id,
        'current_status': self.get_status_display(),
        }
        html_message = render_to_string('emails/status_update_email.html', context)

        send_mail(
        subject=subject,
        message="The status of your booking has been updated.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[self.customer_email],
        fail_silently=False,
        html_message=html_message,  # Send HTML version of the email
        )

    def generate_booking_id(self):
        """Generate a unique booking ID with prefix, date, and random digits."""
        prefix = "FTS"  # Example: Company prefix
        date_str = datetime.now().strftime("%Y%m%d")  # Current date in YYYYMMDD format

    # Cache existing booking IDs for the day
        existing_ids = set(
        Booking.objects.filter(booking_id__startswith=f"{prefix}-{date_str}")
        .values_list("booking_id", flat=True)
        )

        for _ in range(10):  # Retry up to 10 times to avoid collisions
            random_digits = str(random.randint(1000, 9999))  # Generate a 4-digit random number
            booking_id = f"{prefix}-{date_str}-{random_digits}"  # Construct booking ID
            if booking_id not in existing_ids:
                return booking_id

        raise ValueError("Failed to generate a unique booking ID after 10 attempts.")

    def track_status(self):
        """Return a human-readable status."""
        return f"Booking ID: {self.booking_id}, Status: {self.get_completion_status_display()}"
    
    def get_absolute_url(self, user=None):
        if user and user.is_staff:  # Adjust for your admin check
            return reverse("dashboard:bookings", args=[str(self.id)])
        return reverse("user_booking_detail", args=[str(self.id)])

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(
        "Booking", on_delete=models.CASCADE, related_name="payment"
    )
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")],
        default="pending",  # Set default to a valid choice
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_status} for Booking {self.booking.id}"
    

    def get_absolute_url(self, user=None):
        return reverse("dashboard:payments", args=[str(self.id)])



    @property
    def is_paid(self):
        return self.payment_status == "paid"