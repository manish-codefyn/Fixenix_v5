from django.views.generic import ListView, CreateView, UpdateView, DeleteView,View
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from delivery.models import Delivery  # Assuming you have an Employee model
from .forms import DateForm  # Assuming you have a DateForm for filtering
from django.utils.timezone import now
from . import app_settings
from sitesetting.models import Sites
from django.shortcuts import render
from django.http import HttpResponse
from employee.forms import DateForm  # Assuming you have a DateForm for filtering
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from users.mixins import TestMixinUserEmail, TestMixinUserName, StaffRequiredMixin,email_check
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from . utils import render_to_pdf,qr_generate,download_temp_image
# for csv export
import csv
# QR CODE
import io
from django.template import loader
from django.http import JsonResponse
from django.contrib import messages
# date  import
from django.http import HttpResponseBadRequest




class DeliveryExportPDFByDateView(View):
    """View to export Deliveries filtered by date as a PDF."""

    login_url = settings.LOGIN_URL
    template_name = "dashboard/delivery/reports/export_pdf_bydate." + app_settings.TEMPLATE_EXTENSION
    pdf_name = "delivery_filtered_list.pdf"

    def test_func(self):
        """Check if the user passes the email check."""
        return email_check(self.request.user)

    def post(self, request, *args, **kwargs):
        """Handle POST request for exporting filtered data."""
        app_data = Sites.objects.first()

        # Fetch date range from POST request
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both startdate and enddate are required.")

        try:
            # Filter data by date range
            data = Delivery.objects.filter(
                timestamp__date__gte=fromdate, timestamp__date__lte=enddate
            )
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        if not data.exists():
            return HttpResponseBadRequest("No deliveries found for the given dates.")

        # Context for the PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "delivery": data,
            "time": now().date(),
            "doc_name": "Deliveries",
        }

        return render_to_pdf(self.template_name, context, self.pdf_name)

    def get(self, request, *args, **kwargs):
        """Handle GET request with default data."""
        app_data = Sites.objects.first()

        # Default context with all data
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "delivery": Delivery.objects.all(),
            "time": now().date(),
            "doc_name": "Deliveries",
        }

        return render_to_pdf(self.template_name, context, self.pdf_name)


class DeliveriesExportCSVView(View):
    """View to export Deliveries as a CSV file."""

    login_url = settings.LOGIN_URL

 
    def get(self, request, *args, **kwargs):
        """Handle GET requests to export Deliveries to a CSV file."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="Deliveries.csv"'

        deliveries = Delivery.objects.all()
        writer = csv.writer(response)

        # Write the header row
        writer.writerow(
            [
                "Delivery ID",
                "Status",
                "Assigned Employee",
                "Estimated Delivery Time",
                "Current Location (Lat, Lon)",
                "Delivery Location (Lat, Lon)",
                "Timestamp",
            ]
        )

        # Write data rows
        for delivery in deliveries:
            writer.writerow(
                [
                    delivery.id,
                    delivery.status,
                    delivery.employee_name if delivery.employee_name else "Not Assigned",
                    delivery.estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if delivery.estimated_delivery_time else "N/A",
                    f"{delivery.current_location_lat}, {delivery.current_location_lon}",
                    f"{delivery.delivery_location_lat}, {delivery.delivery_location_lon}",
                    delivery.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return response


class DeliveryStatusUpdateView(UpdateView): 
    """View to update the status of a delivery."""
    model = Delivery
    fields = ['status']
    template_name = "dashboard/delivery/update_status.html"
    success_url = reverse_lazy("dashboard:delivery_list")  # Redirect to the list view after updating

    def get_object(self, queryset=None):
        """Retrieve the Delivery object by ID."""
        delivery_id = self.kwargs.get("pk")
        return get_object_or_404(Delivery, id=delivery_id)

    def form_valid(self, form):
        """If the form is valid, save the status and show a success message."""
        delivery = form.save()
        messages.success(self.request, f"Delivery status updated to '{delivery.status}'.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, show an error message."""
        messages.error(self.request, "Failed to update the delivery status. Please try again.")
        return super().form_invalid(form)
    


def delivery_export_pdf_by_id(request, pk):
    """Export Delivery PDF by ID"""
    template_name = f"dashboard/delivery/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"delivery_{pk}.pdf"
    
    # Fetch the delivery object
    delivery = get_object_or_404(Delivery, id=pk)
    
    # Fetch app data (assuming only one app data record exists)
    app_data = Sites.objects.first()
    
    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # QR Code Data
    qr_data = {
        "Delivery ID": str(delivery.id),
        "Status": delivery.status,
        "Assigned Employee": delivery.employee_name.name if delivery.employee_name else "Not Assigned",
        "Estimated Delivery Time": delivery.estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Current Location": f"{delivery.current_location_lat}, {delivery.current_location_lon}",
        "Delivery Location": f"{delivery.delivery_location_lat}, {delivery.delivery_location_lon}",
    }
    img_name = qr_generate(qr_data, size, version, border)
   
    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "delivery_id": delivery.id,
        "status": delivery.status,
        "employee_name": delivery.employee_name if delivery.employee_name else "Not Assigned",
        "estimated_time": delivery.estimated_delivery_time,
        "booking_id": delivery.booking.booking_id,
        "mobile": delivery.booking.customer_phone,
        "email": delivery.booking.customer_email,
        "name": delivery.booking.customer_name,
        "amount_paid": delivery.booking.price,
        "service": delivery.booking.service,
        "address": delivery.booking.address,
        "current_location": f"{delivery.current_location_lat}, {delivery.current_location_lon}",
        "delivery_location": f"{delivery.delivery_location_lat}, {delivery.delivery_location_lon}",
        "time": now().date(),
        "doc_name": "Delivery Detail",
        "qr_code": img_name,
    }

    return render_to_pdf(template_name, context, pdf_name)



class DeliveryExportPdfAll(View):
    """Class-based view to export all deliveries to a PDF."""

    login_url = settings.LOGIN_URL
    template_name = "dashboard/delivery/reports/export_pdfall.html"
    pdf_name = "deliveries_list.pdf"

    def get(self, request, *args, **kwargs):
        """Handle GET requests and generate the PDF."""
        data = Delivery.objects.all()
        app_data = Sites.objects.first()
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "delivery": data,
            "time": now(),
            "doc_name": "Deliveries List",
        }
        return render_to_pdf(self.template_name, context)


class DeliveryDetailView(DetailView):
    """Detail view for a single delivery."""
    
    model = Delivery
    template_name = "dashboard/delivery/detail.html"  # Adjust the template path as needed
    context_object_name = "delivery"
    pk_url_kwarg = "pk"  # The URL parameter for primary key lookup

    def get_object(self, queryset=None):
        """Retrieve the specific delivery object or return a 404."""
        return get_object_or_404(Delivery, id=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        """Provide additional context for rendering."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delivery Details - {self.object.id}"
        context["pagename"] = "Delivery Details"
        context["app"] = Sites.objects.first()
        return context


class DeliveryListView(ListView):
    """View and filter Deliveries by date."""

    template_name = "dashboard/delivery/list." + app_settings.TEMPLATE_EXTENSION
    model = Delivery
    context_object_name = "delivery"
    form_class = DateForm
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        """Provide default context for template rendering."""
        context = super().get_context_data(**kwargs)
        context.update({
            "form": self.form_class(),
            "pagename": "Delivery List",
            "app": Sites.objects.first(),
            "page_title": app_settings.PAGE_TITLE,
            "date": now().date(),
        })
        return context

    def post(self, request, *args, **kwargs):
        """Handle filtering by startdate and enddate."""
        form = self.form_class(request.POST)
        context = {
            "form": form,
            "app": Sites.objects.first(),
            "pagename": "Delivery List",
            "page_title": app_settings.PAGE_TITLE,
        }

        if form.is_valid():
            fromdate = form.cleaned_data.get("startdate")
            enddate = form.cleaned_data.get("enddate")
            query = self.model.objects.all()

            # Filter based on delivery date field (adjust as necessary)
            if fromdate:
                query = query.filter(delivery_date__gte=fromdate)
            if enddate:
                query = query.filter(delivery_date__lte=enddate)

            context["deliveries"] = query
            messages.success(request, "Filter applied successfully!")
        else:
            context["deliveries"] = self.model.objects.all()
            messages.error(request, "Invalid date range. Please try again.")

        return render(request, self.template_name, context)
