from django.db import models
import uuid
from django.urls import reverse


class Brands(models.Model):
    id = models.UUIDField(
        primary_key=True, db_index=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=150)
    pic = models.FileField(upload_to="upload/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dashboard:brand", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Brand"


class Sites(models.Model):
    id = models.UUIDField(
        primary_key=True, db_index=True, default=uuid.uuid4, editable=False
    )
    domain_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    app_email = models.EmailField(max_length=100)
    app_mobile = models.CharField(max_length=20)
    app_address = models.TextField(max_length=150)
    app_version = models.CharField(max_length=20)
    app_logo = models.FileField(upload_to="upload/")
    app_fevicon = models.FileField(upload_to="upload/")
    app_stamp = models.FileField(upload_to="upload/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.domain_name

    def get_absolute_url(self):  # new
        return reverse("dashboard:sites", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Sites"


class Faq(models.Model):
    """
    faqs
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    que = models.CharField(max_length=255)
    ans = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.que

    def get_absolute_url(self):
        return reverse("dashboard:faq", args=[str(self.id)])


class AboutCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    about_company = models.TextField(max_length=555, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.about_company

    def get_absolute_url(self):
        return reverse("dashboard:aboutcompany", args=[str(self.id)])

