import time
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# redirects Imports
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# msg mixin import
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# template loader
from django.template import loader
# date  import
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


class BookingsExportPdfAllView(StaffRequiredMixin, View):
    login_url = settings.LOGIN_URL  # Redirect URL for unauthenticated users

    def get(self, request, *args, **kwargs):
        template_name = (
            "dashboard/bookings/reports/export_pdfall."
            + app_settings.TEMPLATE_EXTENSION
        )
        pdf_name = "bookings_list.pdf"

        # Fetch the app data (assuming only one app data record exists)
        app_data = Sites.objects.first()

        # Fetch all bookings
        bookings = Booking.objects.all()

        # Context for PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "bookings": bookings,
            "time": now().date(),
            "doc_name": "Booking List",
        }

        return render_to_pdf(template_name, context, pdf_name)


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def bookings_export_pdf_by_id(request, pk):
    """Bookings Export PDF by ID"""
    template_name = f"dashboard/bookings/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
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

class BookingStatusUpdateView(
    StaffRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    """Class-based view to update the status of a booking."""

    model = Booking
    fields = ['status']  # Adjust the field name as per your model
    template_name = 'dashboard/bookings/update_booking.html'  # Update this to your template location
    success_url = reverse_lazy('dashboard:bookings_list')  # Replace with your bookings listing view name
    success_message = "Booking status was successfully updated to %(status)s."

    def form_valid(self, form):
        try:
            # Perform any custom logic before saving the form
            booking = form.save(commit=False)
            booking.save()
            # Add custom success message
            messages.success(self.request, f"Booking {booking.id} status updated successfully!")
            return super().form_valid(form)
        except Exception as e:
            # Add custom error message
            messages.error(self.request, f"An error occurred: {str(e)}")
            return self.form_invalid(form)

    def test_func(self):
        # Restrict access to staff users or other permissions
        return self.request.user.is_staff



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def bookings_export_csv(request):
    """Bookings Export CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Bookings.csv"'
    # Fetch all bookings
    bookings = Booking.objects.all()
    # CSV Writer
    writer = csv.writer(response)
    # Write Header Row
    writer.writerow(
        [
            "Customer Name",
            "Mobile",
            "Email",
            "Service Name",
            "Created Date",
        ]
    )

    # Write Data Rows
    for booking in bookings:
        writer.writerow(
            [
                booking.customer_name,
                booking.customer_phone,
                booking.customer_email,
                booking.service.service_name,
                booking.created_at,
            ]
        )

    return response


class BookingsExportPdfByDateView(StaffRequiredMixin, View):
    """Exports bookings filtered by date range as a PDF."""
    login_url = settings.LOGIN_URL  # Redirect URL for unauthenticated users

    template_name = (
        "dashboard/bookings/reports/export_pdf_bydate."
        + app_settings.TEMPLATE_EXTENSION
    )
    pdf_name = "bookings_filtered_list.pdf"

    def post(self, request, *args, **kwargs):
        """Handle POST requests to filter bookings by date."""
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both startdate and enddate are required.")

        # Filter data by date range
        try:
            data = Booking.objects.filter(
                created_at__date__gte=fromdate, created_at__date__lte=enddate
            )
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        if not data.exists():
            return JsonResponse({"message": "No bookings found for the specified dates."}, status=404)

        # Fetch app data
        app_data = Sites.objects.first()

        # Context for PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "bookings": data,
            "time": date.today(),
            "doc_name": "Bookings Report",
        }

        return render_to_pdf(self.template_name, context, self.pdf_name)
    

    def get(self, request, *args, **kwargs):
        """Handle GET requests to export all bookings."""
        context = {
            "app_data": Sites.objects.all(),
            "bookings": Booking.objects.all(),
            "time": now().date(),
            "doc_name": "Bookings",
        }
        return render_to_pdf(self.template_name, context, self.pdf_name)


class BookingsListView(StaffRequiredMixin,ListView):
    """Views By date"""

    login_url = reverse_lazy("account_login")
    form_class = DateForm
    model = Booking
    template_name = "dashboard/bookings/list." + app_settings.TEMPLATE_EXTENSION


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form": form,
            "bookings": self.model.objects.all(),
            "pagename": "Bookings List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }

        return render(request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        fromdate = self.request.POST.get("startdate")
        enddate = self.request.POST.get("enddate")
        context = {
            "bookings": self.model.objects.all().filter(created_at__gte=fromdate),
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": "Bookings list",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        if fromdate:
            return render(self.request, self.template_name, context)
        if enddate:
            context = {
                "bookings": self.model.objects.all().filter(created_at__lte=enddate),
                "form": form,
                "pagename": "RepairService List",
                "app_data": Sites.objects.all(),
                "page_title": app_settings.PAGE_TITLE,
            }
            return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "bookings": self.model.objects.all(),
                "form": form,
            },
        )


class BookingsDetailsViews(StaffRequiredMixin,DetailView):
    """DetailView"""

    model = Booking
    login_url = reverse_lazy("account_login")
    context_object_name = "bookings"
    template_name = (
        "dashboard/bookings/detail." + app_settings.TEMPLATE_EXTENSION
    )
    data = "www.fixenix.com"
    # img = qrcode.make(data, box_size=2)
    # img_name = "qr" + str(time.time()) + ".png"
    # img.save(settings.MEDIA_ROOT + "/" + img_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "app_data": Sites.objects.all(),
            "pagename": "Bookings Detail",
            "doc_name": "Bookings Detail",
            "date": now().date(),
        })
        return context
