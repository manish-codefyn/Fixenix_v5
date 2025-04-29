import time
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# redirects Imports
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
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
from bookings.models import Booking,Payment
from . import app_settings
from datetime import date
# 3RD Party
# for pdf export
from .utils import render_to_pdf,qr_generate,download_temp_image
# for csv export
import csv
# QR CODE
import io
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import qrcode
import base64
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View
from django.utils.timezone import now
import tempfile
import requests
from xhtml2pdf import pisa


class GenerateInvoiceAndSendEmailView(View):
    """Generates an invoice and sends it to the customer via email."""

    def get(self, request, pk, *args, **kwargs):
        # Fetch the payment object
        payment = get_object_or_404(Payment, id=pk)

        # Ensure the payment is completed before generating the invoice
        if not payment.is_paid:
            return HttpResponse("Cannot generate invoice for unpaid payment.", status=400)

        # QR Code Generation
        qr_data = {
            "booking_id": payment.booking.booking_id,
            "customer_name": payment.booking.customer_name,
            "amount_paid": str(payment.amount_paid),
            "payment_id": payment.razorpay_payment_id,
        }
        qr_code_path = self.generate_qr_code(qr_data)

        # Fetch the app data (assuming only one app data record exists)
        app_data = Sites.objects.first()

        # Context for PDF
        context = {
            "qr_code": qr_code_path,
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "payment": payment,
            "transaction_id": payment.razorpay_payment_id,
            "order_id": payment.razorpay_order_id,
            "service": payment.booking,
            "customer_name": payment.booking.customer_name,
            "address": payment.booking.address,
            "customer_email": payment.booking.customer_email,
            "customer_phone": payment.booking.customer_phone,
            "booking_id": payment.booking.booking_id,
            "amount_paid": payment.amount_paid,
            "date": payment.created_at,
            "service_name": payment.booking.service.service_name,
            "doc_name": "Invoice",
             "time": now().date(),
        }

        # Generate PDF Invoice
        pdf = self.render_2_pdf("invoice/payments_invoice.html", context)

        if not pdf:
            return HttpResponse("Failed to generate PDF.", status=500)

        # Prepare email
        subject = f"Invoice for your booking - {payment.booking.id}"
        message = (
            "Dear Customer,\n\nPlease find attached the invoice for your recent booking. "
            "Thank you for your payment.\n\nBest regards,\n[Your Company Name]"
        )
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[payment.booking.customer_email],
        )

        # Attach PDF to email
        email.attach(f"Invoice_{payment.booking.id}.pdf", pdf, "application/pdf")

        # Send email
        try:
            email.send()
            messages.success(request, "Invoice generated and email sent successfully.")
            return redirect("dashboard:payments_list")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")
            return redirect("dashboard:payments_list")

    def generate_qr_code(self, data):
        """Generates and returns the path to a temporary QR code image."""
        import qrcode

        qr = qrcode.QRCode(version=2, box_size=2, border=0)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_file.name)
        return temp_file.name
    
    def render_2_pdf(self,template_src, context_dict):
        """Render a Django template to a PDF file and return it as bytes."""
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)

        if pisa_status.err:
            return None  # Return None if PDF generation fails

        return result.getvalue()



class PaymentStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Class-based view to update the status of a payment."""

    model = Payment
    fields = ['payment_status']
    template_name = 'dashboard/payments/status_update.html'  # Update this path to your template location
    success_url = reverse_lazy('dashboard:payments_list')  # Replace with your payments listing view name
    success_message = "Payment status was successfully updated to %(payment_status)s."

    def form_valid(self, form):
        try:
            # Perform any custom logic before saving the form
            payment = form.save(commit=False)
            payment.save()
            # Add custom success message
            messages.success(self.request, f"Payment {payment.id} status updated successfully!")
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
def payments_export_csv(request):
    """payments Export CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="payments.csv"'
    # Fetch all payments
    payments = Payment.objects.all()

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
    for payment in payments:
        writer.writerow(
            [
                payment.booking.customer_name,
                payment.booking.customer_phone,
                payment.booking.customer_email,
                payment.booking.service,
                payment.created_at,
            ]
        )

    return response


@login_required(login_url=settings.LOGIN_URL)
def payments_export_pdf_by_id(request, pk):
    """Payments Export PDF by ID"""
    template_name = f"dashboard/payments/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{pk}_payment.pdf"
    payment = get_object_or_404(Payment, id=pk)

    # QR Code Configuration
    qr_data = {
        "Service Name": payment.booking.service.service_name,
        "Order ID": payment.razorpay_order_id,
        "Transaction Id": payment.razorpay_payment_id,
        "Amount Paid": str(payment.amount_paid),
    }
    qr_code_path = qr_generate(qr_data)

    # Fetch app data
    app_data = Sites.objects.first()

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "service": payment.booking.service.service_name,
        "order_id": payment.razorpay_order_id,
        "transaction_id": payment.razorpay_payment_id,
        "name": payment.booking.customer_name,
        "mobile": payment.booking.customer_phone,
        "email": payment.booking.customer_email,
        "booking_id": payment.booking.booking_id,
        "address": payment.booking.address,
        "amount": payment.amount_paid,
        "created": payment.created_at,
        "time": now().date(),
        "doc_name": "Payments Detail",
        "qr_code": qr_code_path,
    }

    return render_to_pdf(template_name, context, pdf_name)


class PaymentsExportPdfByDateView(StaffRequiredMixin, View):
    """Exports payments filtered by date range as a PDF."""
    login_url = settings.LOGIN_URL  # Redirect URL for unauthenticated users

    template_name = (
        "dashboard/payments/reports/export_pdf_bydate."
        + app_settings.TEMPLATE_EXTENSION
    )
    pdf_name = "payments_filtered_list.pdf"

    def post(self, request, *args, **kwargs):
        """Handle POST requests to filter payments by date."""
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both startdate and enddate are required.")

        # Filter data by date range
        try:
            data = Payment.objects.filter(
                created_at__date__gte=fromdate, created_at__date__lte=enddate
            )
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        if not data.exists():
            return JsonResponse({"message": "No payments found for the specified dates."}, status=404)

        # Fetch app data
        app_data = Sites.objects.first()

        # Context for PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "payments": data,
            "time": date.today(),
            "doc_name": "Payments Report",
        }

        return render_to_pdf(self.template_name, context, self.pdf_name)

    def get(self, request, *args, **kwargs):
        """Handle GET requests to export all payments."""
        context = {
            "app_data": Sites.objects.all(),
            "payments": Payment.objects.all(),
            "time": now().date(),
            "doc_name": "payments",
        }
        return render_to_pdf(self.template_name, context, self.pdf_name)


class PaymentsExportPdfAllView(StaffRequiredMixin, View):
    """Exports all payments as a PDF."""
    login_url = settings.LOGIN_URL  # Redirect URL for unauthenticated users

    def get(self, request, *args, **kwargs):
        template_name = (
            "dashboard/payments/reports/export_pdfall."
            + app_settings.TEMPLATE_EXTENSION
        )
        pdf_name = "payments_list.pdf"

        # Fetch app data
        app_data = Sites.objects.first()

        # Context for PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "payments": Payment.objects.all(),
            "time": now().date(),
            "doc_name": "Payments List",
        }

        return render_to_pdf(template_name, context, pdf_name)


class PaymentsListView(StaffRequiredMixin, ListView):
    """Views By date"""

    login_url = reverse_lazy("account_login")
    form_class = DateForm
    model = Payment
    template_name = "dashboard/payments/list." + app_settings.TEMPLATE_EXTENSION


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form": form,
            "payments": self.model.objects.all(),
            "pagename": "Payments List",
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
            "payments": self.model.objects.all().filter(created_at__gte=fromdate),
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": "payments list",
            "page_title": app_settings.PAGE_TITLE,
        }
        if fromdate:
            return render(self.request, self.template_name, context)
        if enddate:
            context = {
                "payments": self.model.objects.all().filter(created_at__lte=enddate),
                "form": form,
                "pagename": "payments List",
                "app_data": Sites.objects.all(),
                "page_title": app_settings.PAGE_TITLE,
            }
            return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "payments": self.model.objects.all(),
                "form": form,
            },
        )

class PaymentsDetailsViews(StaffRequiredMixin,DetailView):
    """DetailView"""

    model = Payment
    login_url = reverse_lazy("account_login")
    context_object_name = "payments"
    template_name = (
        "dashboard/payments/detail." + app_settings.TEMPLATE_EXTENSION
    )
    data = "www.fixenix.com"
    # img = qrcode.make(data, box_size=2)
    # img_name = "qr" + str(time.time()) + ".png"
    # img.save(settings.MEDIA_ROOT + "/" + img_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "app_data": Sites.objects.all(),
            "pagename": "payments Detail",
            "doc_name": "payments Detail",
            "date": now().date(),
        })
        return context
