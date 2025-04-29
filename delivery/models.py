import uuid
from django.db import models
from django.utils.timezone import now
from bookings.models import Booking
from employee.models import Employee
from django.urls import reverse



class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, blank=True, null=True
    )  # Replace 'Booking' with the actual model name in your project
    employee_name = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_deliveries'
    )  # Replace 'Employee' with the actual model name in your project
    current_location_lat = models.FloatField(blank=True, null=True)
    current_location_lon = models.FloatField(blank=True, null=True)
    delivery_location_lat = models.FloatField()
    delivery_location_lon = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("out_for_delivery", "Out For Delivery"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    estimated_delivery_time = models.DateTimeField(default=now)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def send_assignment_email(self):
        """Send email to the delivery boy when assigned."""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings

        if self.employee_name and self.employee_name.email:
            submission_link = f"{settings.BASE_URL}/delivery/update-location/{self.id}/"
            subject = "New Delivery Assignment"
            context = {
                "delivery_id": self.id,
                "submission_link": submission_link,
                "delivery_location_lat": self.delivery_location_lat,
                "delivery_location_lon": self.delivery_location_lon,
            }
            html_message = render_to_string("delivery/emails/assignment_email.html", context)
            send_mail(
                subject,
                "You have a new delivery assignment.",
                settings.DEFAULT_FROM_EMAIL,
                [self.employee_name.email],
                fail_silently=False,
                html_message=html_message,
            )

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the object already exists in the database
            try:
                original = Delivery.objects.get(pk=self.pk)
            # Check if the employee assignment has changed
                if original.employee_name != self.employee_name and self.employee_name:
                    self.send_assignment_email()
            except Delivery.DoesNotExist:
            # Object doesn't exist in the database yet
                pass

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dashboard:deliveries", args=[str(self.id)])
