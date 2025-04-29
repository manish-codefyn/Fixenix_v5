from django.conf import settings
from pathlib import Path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
# revers and redirect
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# validation
from django.core.exceptions import ValidationError
# random number
import random
# requests
import requests
# mail
from sitesetting.form import DateForm
from django.core.mail import EmailMultiAlternatives  # form html send
# template rendering
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# jason response
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView, ListView,DetailView, FormView, View
from .models import CustomUser
from sitesetting.models import Sites
from users import app_settings
from users.mixins import TestMixinUserEmail, TestMixinUserName, StaffRequiredMixin
# All auth signup
from allauth.account.views import SignupView
from .forms import CustomUserCreationForm, UserVerifyForm, CodeVerifyForm
from bookings.models import Booking, Payment, Review  # Import your models
from django.shortcuts import get_object_or_404
from bookings.models import Booking,Payment
from django.http import HttpResponse, FileResponse,Http404
from .utils import render_to_pdf

from django.utils.timezone import now
# Generic Views Imports
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    View
)
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
# local Imports
from sitesetting.models import Sites
from sitesetting.form import DateForm
from bookings.models import RepairService,Booking,Review,Payment,Device,DeviceBrand,DeviceModel,DeviceProblem
from . import app_settings
from datetime import date
# 3RD Party
# for pdf export
from .utils import render_to_pdf
# for csv export
import csv
# QR CODE
import io
import qrcode
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from . utils import render_to_pdf,qr_generate,download_temp_image



@login_required(login_url=settings.LOGIN_URL)
def user_bookings_export_pdf_by_id(request, pk):
    """Bookings Export PDF by ID"""
    template_name = f"account/dashboard/bookings/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{pk}_booking.pdf"

    # Fetch the booking object
    booking = get_object_or_404(Booking, id=pk)

    # Fetch the app data (assuming only one app data record exists)
    app_data = Sites.objects.first()

    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # Booking Details
    service = booking.service.service_name
    name = booking.customer_name
    email = booking.customer_email
    mobile = booking.customer_phone
    address = booking.address
    booking_id = booking.booking_id
    price = booking.price
    created = booking.created_at

    # QR Code Generation
    qr_data = {
        "Service Name": service,
        "Customer Name": name,
        "Customer Mobile": mobile,
        "Customer Email": email,
    }
    qr_image_path = qr_generate(qr_data, size, version, border)

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "service": service,
        "name": name,
        "email": email,
        "mobile": mobile,
        "address": address,
        "price": price,
        "booking_id": booking_id,
        "created": created,
        "time": now().date(),
        "doc_name": "Bookings Detail",
        "qr_image_path": qr_image_path,  # Absolute path for QR code image
    }

    return render_to_pdf(template_name, context, pdf_name)


class UserOrderDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a specific booking"""

    model = RepairService
    template_name = "account/dashboard/orders/detail." + app_settings.TEMPLATE_EXTENSION  # Ensure TEMPLATE_EXTENSION is correctly defined
    context_object_name = "orders"
    login_url = reverse_lazy("account_login")

    def get_object(self, queryset=None):
        """Override to ensure the booking belongs to the logged-in user"""
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You do not have permission to view this booking.")
        return obj

    def get_context_data(self, **kwargs):
        """Add additional context data for the template"""
        context = super().get_context_data(**kwargs)
        data = "www.fixenix.com"

        # Uncomment the following lines if QR code generation is needed
        # import qrcode, time
        # img = qrcode.make(data, box_size=2)
        # img_name = "qr_" + str(int(time.time())) + ".png"
        # img_path = settings.MEDIA_ROOT + "/" + img_name
        # img.save(img_path)
        # context["qr_image"] = settings.MEDIA_URL + img_name

        context.update({
            "app": Sites.objects.first(),
            "pagename": "Bookings Detail",
            "doc_name": "Bookings Detail",
            "date": now().date(),
        })
        return context


class UserOrderList(LoginRequiredMixin, ListView):
    """View bookings filtered by date for the logged-in user"""

    login_url = reverse_lazy("account_login")
    form_class = DateForm
    model = RepairService
    template_name = "account/dashboard/orders/list."+ app_settings.TEMPLATE_EXTENSION  # Customize your template path

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = request.user
        context = {
            "form": form,
            "order": self.model.objects.filter(user=user),
            "pagename": "My Order List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        fromdate = self.request.POST.get("startdate")
        enddate = self.request.POST.get("enddate")
        filters = {"user": user}
        if fromdate:
            filters["created_at__gte"] = fromdate
        if enddate:
            filters["created_at__lte"] = enddate

        context = {
            "order": self.model.objects.filter(**filters),
            "form": form,
            "pagename": "My Order List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        user = self.request.user
        return render(
            self.request,
            self.template_name,
            {
                "order": self.model.objects.filter(user=user),
                "form": form,
            },
        )
    


@login_required(login_url=settings.LOGIN_URL)
def user_bookings_export_pdf_by_id(request, pk):
    """Bookings Export PDF by ID"""
    template_name = f"account/dashboard/bookings/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{pk}_booking.pdf"

    # Fetch the booking object
    booking = get_object_or_404(Booking, id=pk)

    # Fetch the app data (assuming only one app data record exists)
    app_data = Sites.objects.first()

    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # Booking Details
    service = booking.service.service_name
    name = booking.customer_name
    email = booking.customer_email
    mobile = booking.customer_phone
    address = booking.address
    booking_id = booking.booking_id
    price = booking.price
    created = booking.created_at

    # QR Code Generation
    qr_data = {
        "Service Name": service,
        "Customer Name": name,
        "Customer Mobile": mobile,
        "Customer Email": email,
    }
    qr_image_path = qr_generate(qr_data, size, version, border)

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "service": service,
        "name": name,
        "email": email,
        "mobile": mobile,
        "address": address,
        "price": price,
        "booking_id": booking_id,
        "created": created,
        "time": now().date(),
        "doc_name": "Bookings Detail",
        "qr_image_path": qr_image_path,  # Absolute path for QR code image
    }

    return render_to_pdf(template_name, context, pdf_name)


class UserBookingDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a specific booking"""

    model = Booking
    template_name = "account/dashboard/bookings/detail." + app_settings.TEMPLATE_EXTENSION  # Ensure TEMPLATE_EXTENSION is correctly defined
    context_object_name = "bookings"
    login_url = reverse_lazy("account_login")

    def get_object(self, queryset=None):
        """Override to ensure the booking belongs to the logged-in user"""
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You do not have permission to view this booking.")
        return obj

    def get_context_data(self, **kwargs):
        """Add additional context data for the template"""
        context = super().get_context_data(**kwargs)
        data = "www.fixenix.com"

        # Uncomment the following lines if QR code generation is needed
        # import qrcode, time
        # img = qrcode.make(data, box_size=2)
        # img_name = "qr_" + str(int(time.time())) + ".png"
        # img_path = settings.MEDIA_ROOT + "/" + img_name
        # img.save(img_path)
        # context["qr_image"] = settings.MEDIA_URL + img_name

        context.update({
            "app": Sites.objects.first(),
            "pagename": "Bookings Detail",
            "doc_name": "Bookings Detail",
            "date": now().date(),
        })
        return context

class InvoiceDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Fetch the specific booking
        booking = get_object_or_404(Booking, id=self.kwargs.get('pk'), user=request.user)
        # Generate the PDF
        context = {
            "booking": booking,
          
            "user": request.user,
        }
        pdf_buffer = render_to_pdf("bookings/user/invoice_template.html", context)

        if not pdf_buffer:
            return HttpResponse("Error generating PDF", status=500)

        # Return the PDF as a downloadable response
        response = FileResponse(pdf_buffer, as_attachment=True, filename=f"Invoice-{booking.id}.pdf")
        return response


class UserBookingList(LoginRequiredMixin, ListView):
    """View bookings filtered by date for the logged-in user"""

    login_url = reverse_lazy("account_login")
    form_class = DateForm
    model = Booking
    template_name = "account/dashboard/bookings/list."+ app_settings.TEMPLATE_EXTENSION  # Customize your template path

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = request.user
        context = {
            "form": form,
            "bookings": self.model.objects.filter(user=user),
            "pagename": "My Booking List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        fromdate = self.request.POST.get("startdate")
        enddate = self.request.POST.get("enddate")
        filters = {"user": user}
        if fromdate:
            filters["created_at__gte"] = fromdate
        if enddate:
            filters["created_at__lte"] = enddate

        context = {
            "bookings": self.model.objects.filter(**filters),
            "form": form,
            "pagename": "My Booking List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        user = self.request.user
        return render(
            self.request,
            self.template_name,
            {
                "bookings": self.model.objects.filter(user=user),
                "form": form,
            },
        )




