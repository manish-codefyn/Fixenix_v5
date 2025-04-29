from django.db import models
import uuid
from django.urls import reverse
import datetime

def work_id():
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD
    unique_id = str(uuid.uuid4()).split("-")[1].upper()  # Extract part of UUID
    work_id = f"JOB-{current_date}-{unique_id}"
    return work_id


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Done", "Done"),
    ("Delivered", "Delivered"),
    ("Returned", "Returned"),
)


class WorkSheet(models.Model):
    """Worksheet Create Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    email = models.EmailField()
    device_name = models.CharField(max_length=100)
    device_problem = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    work_id = models.CharField(
        max_length=255, default=work_id, unique=True, editable=False
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("work_sheet", args=[str(self.id)])

    class Meta:
        indexes = [models.Index(fields=["id"], name="id_index")]
