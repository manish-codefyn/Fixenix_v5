from django.conf import settings
import time
from pathlib import Path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# redirects Imports
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
# msg mixin import
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# date import
import datetime
# Generic Views Imports
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    RedirectView,
    TemplateView,
    View
)
# 3RD Party
# for csv export
import csv
# QR CODE
import io
import qrcode
# App setting
from . import app_settings
# Local Import
from Invoice.models import Invoice
from .utils import render_to_pdf,qr_generate,download_temp_image
from Invoice.form import InvoiceForm,InvoiceUpdateForm
from sitesetting.models import Sites
from sitesetting.form import DateForm
from django.contrib.auth.decorators import user_passes_test
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def InvoiceExportPdfbyId(request, pk):
    """Export Invoice PDF by ID using the updated Invoice model"""

    template_name = "invoice/reports/export_pdfbyid." + app_settings.TEMPLATE_EXTENSION

    invoice = get_object_or_404(Invoice, id=pk)

    # QR code generation settings
    size = 2
    version = 2
    border = 0

    # Prepare data for QR code
    qr_data = {
        "Invoice No": invoice.invoice_no,
        "Customer Name": invoice.customer_name,
        "Email": invoice.email,
        "Mobile": invoice.mobile,
        "Total Amount": invoice.total_amount,
        "Due Date": invoice.due_date.strftime("%Y-%m-%d"),
        "Payment Status": invoice.payment_status,
        "Updated": invoice.updated_at.strftime("%Y-%m-%d %H:%M"),
    }
    qr_code_img = qr_generate(qr_data, size, version, border)

    # Fetch global app data
    app_data = Sites.objects.first()
    product_items = invoice.product_details or []

    # Ensure all product items have calculated total_price
    for item in product_items:
        try:
            item["total_price"] = float(item.get("price", 0)) * int(item.get("qty", 1))
        except (ValueError, TypeError):
            item["total_price"] = 0.0

    context = {
        "app": app_data,
        "logo": getattr(app_data.app_logo, 'url', None) if app_data else None,
        "stamp": getattr(app_data.app_stamp, 'url', None) if app_data else None,

        "invoice": invoice,
        "customer_name": invoice.customer_name,
        "email": invoice.email,
        "mobile": invoice.mobile,
        "address": invoice.address,
        "invoice_date": invoice.invoice_date,
        "due_date": invoice.due_date,
        "product_details": product_items,
        "subtotal": invoice.subtotal,
        "tax_amount": invoice.tax_amount,
        "discount_amount": invoice.discount_amount,
        "total_amount": invoice.total_amount,
        "notes": invoice.notes,
        "terms": invoice.terms,
        "created": invoice.created_at,
        "updated": invoice.updated_at,
        "payment_status": invoice.payment_status,
        "invoice_no": invoice.invoice_no,
        "time": datetime.date.today(),
        "doc_name": "INVOICE",
        "qr_code": qr_code_img,
    }
    pdf_name = f"{invoice.customer_name or 'invoice'}_{invoice.invoice_no}.pdf"
    return render_to_pdf(template_name, context, pdf_name)


@method_decorator(csrf_exempt, name='dispatch')  # Only for API-style POST without CSRF
class InvoiceCreateView(View):
    """Handles Invoice creation via JSON POST"""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        form = InvoiceForm(data)
        if form.is_valid():
            invoice = form.save(commit=False)

            products = data.get('product_details', [])  # ✅ FIXED: matches frontend key
            subtotal = sum(float(item['price']) * float(item['quantity']) for item in products)
            tax_rate = float(data.get('tax_rate', 0))
            discount = float(data.get('discount_amount', 0))

            tax_amount = subtotal * (tax_rate / 100)
            total_amount = subtotal + tax_amount - discount

            invoice.product_details = products  # Ensure this is a JSONField in your model
            invoice.subtotal = subtotal
            invoice.tax_amount = tax_amount
            invoice.discount_amount = discount
            invoice.total_amount = total_amount
            invoice.save()

            return JsonResponse({
                'success': True,
                'invoice_id': str(invoice.id),
                'invoice_no': invoice.invoice_no
            })

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def get(self, request, *args, **kwargs):
        form = InvoiceForm()
        return render(request, 'invoice/create.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def invoiceExportPdfByDate(request):
    """Export Invoices as PDF filtered by date range."""
    template_name = f"invoice/reports/export_pdf_bydate.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "invoice_filtered_list.pdf"
    app_data = Sites.objects.first()

    if request.method == "POST":
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        # Validate date inputs
        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both start date and end date are required.")

        try:
            # Filter invoices by the provided date range
            data = Invoice.objects.filter(
                created_at__date__gte=fromdate, created_at__date__lte=enddate
            )
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        if not data.exists():
            return HttpResponse("No records found for the specified date range.", status=404)

        # Context for the filtered data
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "invoice": data,
            "time": datetime.date.today(),
            "doc_name": "Invoice List",
        }

        try:
            # Generate and return the filtered PDF
            pdf_file = render_to_pdf(template_name, context, pdf_name)
            if not pdf_file:
                raise ValueError("PDF generation failed.")
            return pdf_file
        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

    else:
        # Handle GET request to display all invoices as fallback
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "invoice": Invoice.objects.all(),
            "time": datetime.date.today(),
            "doc_name": "Invoice List",
        }

        try:
            # Generate and return the PDF for all records
            pdf_file = render_to_pdf(template_name, context, pdf_name)
            if not pdf_file:
                raise ValueError("PDF generation failed.")
            return pdf_file
        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def invoiceExportPdfAll(request):
    """Generate and Export PDF for All Invoices"""
    template_name = f"invoice/reports/export_pdfall.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "invoice_list.pdf"

    try:
        # Fetch all required data
        invoice = Invoice.objects.all()
        app_data = Sites.objects.first()

        # Prepare context with fallback values
        context = {
            "app": app_data,
            "logo": app_data.app_logo.url
            if app_data and app_data.app_logo
            else None,
            "stamp": download_temp_image(app_data.app_stamp.url)
            if app_data and app_data.app_stamp
            else None,
            "invoice": invoice,
            "time": datetime.date.today(),
            "doc_name": "Invoice List",
        }

        # Ensure the context contains all necessary data
        if not invoice.exists():
            return HttpResponse("No invoices available to export.", status=404)

        # Generate PDF
        pdf_file = render_to_pdf(template_name, context, pdf_name)
        if not pdf_file:
            raise ValueError("PDF generation failed.")
        return pdf_file

    except Invoice.DoesNotExist:
        return HttpResponse("No invoices found.", status=404)
    except Sites.DoesNotExist:
        return HttpResponse("Application data not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)



class InvoiceT(TemplateView):
    """Update VIEW"""

    template_name = "invoice/reports/invoice." + app_settings.TEMPLATE_EXTENSION

    extra_context = {
        "app_data": Sites.objects.all(),
        "pagename": app_settings.PAGE_NAME,
        "page_title": app_settings.PAGE_TITLE,
    }


class InvoiceUpdate(StaffRequiredMixin, TestMixinUserEmail, SuccessMessageMixin, UpdateView):
    """
    Staff-only view for updating an existing Invoice.
    Includes user email validation and a success message.
    """

    model = Invoice
    template_name = f"invoice/update.{app_settings.TEMPLATE_EXTENSION}"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("invoice_list")
    success_message = "Invoice successfully updated!"
    fields = ['customer_name', 'mobile', 'email', 'product_details', 'total_amount', 'payment_status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "app_data": Sites.objects.all(),
            "pagename": app_settings.PAGE_NAME,
            "page_title": app_settings.PAGE_TITLE,
        })
        return context

# class InvoiceUpdate(LoginRequiredMixin, UpdateView):
#     model = Invoice
#     form_class = InvoiceUpdateForm
#     template_name = f"invoice/update.{app_settings.TEMPLATE_EXTENSION}"
#     success_url = reverse_lazy('invoice_list')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         allowed_fields =   [
#             'customer_name',
#             'mobile',
#             'email',
#             'address',
#             'due_date',
#             'product_details',
#             'subtotal',
#             'tax_amount',
#             'discount_amount',
#             'total_amount',
#             'notes',
#             'terms',
#             'payment_status',
#         ]
#         for field_name in list(form.fields):
#             if field_name not in allowed_fields:
#                 del form.fields[field_name]
#         return form


class InvoiceDetail(StaffRequiredMixin, TestMixinUserEmail, SuccessMessageMixin,DetailView):
    """Displays the details of a specific Invoice with QR code"""

    model = Invoice
    template_name = f"invoice/detail.{app_settings.TEMPLATE_EXTENSION}"
    context_object_name = "inv"
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate QR code from invoice URL or data
        data = "https://www.fixenix.com/invoice/" + str(self.object.pk)
        qr_img = qrcode.make(data, box_size=2)

        # Process product_details to add total_price for each item
        product_items = self.object.product_details
        for item in product_items:
            try:
                item["total_price"] = float(item.get("price", 0)) * int(item.get("qty", 1))
            except (ValueError, TypeError):
                item["total_price"] = 0.0

        context.update({
            "app_data": Sites.objects.all(),
            "pagename": app_settings.PAGE_NAME,
            "page_title": app_settings.PAGE_TITLE,
            "date": datetime.date.today(),
            "qr_code_img_obj": qr_img,
            "product_items": product_items,  # 👈 Pass this to your template
        })
        return context


class InvoiceList(StaffRequiredMixin, TestMixinUserEmail, ListView):
    """Views By date"""

    form_class = DateForm
    model = Invoice
    template_name = "invoice/list." + app_settings.TEMPLATE_EXTENSION
    page_name = app_settings.PAGE_NAME

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form": form,
            "invoice": self.model.objects.all(),
            "pagename": self.page_name,
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }

        return render(request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == "POST":
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        fromdate = self.request.POST.get("startdate")
        enddate = self.request.POST.get("enddate")
        invoice = self.model.objects.all()
        context = {
            "invoice": invoice.filter(created_at__gte=fromdate),
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": self.page_name,
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        if fromdate:
            return render(self.request, self.template_name, context)
        if enddate:
            context = {
                "invoice": invoice.filter(created_at__lte=enddate),
                "form": form,
                "pagename": app_settings.PAGE_NAME,
                "app_data": Sites.objects.all(),
                "page_title": app_settings.PAGE_TITLE,
            }
            return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "invoice": self.model.objects.all(),
                "form": form,
            },
        )
