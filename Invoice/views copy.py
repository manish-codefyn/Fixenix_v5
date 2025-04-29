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
from Invoice.form import InvoiceForm
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

    context = {
        "app": app_data,
        "logo": app_data.app_logo.url if app_data and app_data.app_logo else None,
        "stamp": app_data.app_stamp.url if app_data and app_data.app_stamp else None,

        "invoice": invoice,
        "customer_name": invoice.customer_name,
        "email": invoice.email,
        "mobile": invoice.mobile,
        "address": invoice.address,
        "invoice_date": invoice.invoice_date,
        "due_date": invoice.due_date,
        "product_details": invoice.product_details,
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


@method_decorator(csrf_exempt, name='dispatch')  # Only if you're not using CSRF tokens (API-style)
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

            products = data.get('products', [])
            subtotal = sum(float(item['price']) * float(item['quantity']) for item in products)
            tax_rate = float(data.get('tax_rate', 0))
            discount = float(data.get('discount', 0))

            tax_amount = subtotal * (tax_rate / 100)
            total_amount = subtotal + tax_amount - discount

            invoice.product_details = products
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
    fields = ['name', 'mobile', 'email', 'product_detail', 'amount', 'payment_status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "app_data": Sites.objects.all(),
            "pagename": app_settings.PAGE_NAME,
            "page_title": app_settings.PAGE_TITLE,
        })
        return context


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

        # Optionally save the QR image (commented)
        # import time
        # from django.conf import settings
        # img_name = "qr_" + str(time.time()) + ".png"
        # qr_img.save(settings.MEDIA_ROOT + "/" + img_name)
        # context['qr_code_img'] = img_name

        context.update({
            "app_data": Sites.objects.all(),
            "pagename": app_settings.PAGE_NAME,
            "page_title": app_settings.PAGE_TITLE,
            "date": datetime.date.today(),
            "qr_code_img_obj": qr_img,  # you can render this as a base64 image if needed
        })
        return context


# class InvoiceCreate(StaffRequiredMixin, TestMixinUserEmail, CreateView):
#     template_name = "invoice/create." + app_settings.TEMPLATE_EXTENSION
#     login_url = reverse_lazy("account_login")
#     model = Invoice
#     form_class = InvoiceForm

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         contex = {
#             "form": form,
#             "app_data": Sites.objects.all(),
#             "page_title": app_settings.PAGE_TITLE,
#             "pagename": app_settings.PAGE_NAME,
#             "form_name": app_settings.FORM_NAME,
#         }

#         return render(request, self.template_name, contex)

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data["name"]
#             email = form.cleaned_data["email"]
#             mobile = form.cleaned_data["mobile"]
#             return self.form_valid(form, name, email)
#         else:
#             return self.form_invalid(form)

#     def get_success_url(self):
#         messages.success(self.request, " Successfully Added !")
#         return reverse("invoice_list")

#     def form_valid(self, form, name, email):
#         """
#         If the form is valid return HTTP 200 status
#         code along with name of the user
#         """
#         form.save()
#         return HttpResponseRedirect(self.get_success_url())
#         # context = {
#         #     "title": " Invoice !",
#         #     "content": f"Dear { name }.Thank you for Choosing Us!",
#         # }
#         # subject = "Invoice Generated !"
#         # from_mail = settings.EMAIL_HOST_USER
#         # template_name = "invoice/email/emails." + app_settings.TEMPLATE_EXTENSION
#         # to_mail = email
#         # try:
#         #     SendMailInHtml(subject, context, template_name, to_mail, from_mail)
#         #     return HttpResponseRedirect(self.get_success_url())
#         # except:
#         #     messages.error(self.request, "Mail Not Sent .! Try again !")
#         #     return HttpResponseRedirect(reverse_lazy("invoice_list"))

#     def form_invalid(self, form):
#         """
#         If the form is invalid return status 400
#         with the errors.
#         """
#         errors = form.errors
#         context = {
#             "form": form,
#             "app_data": Sites.objects.all(),
#             "page_title": app_settings.PAGE_TITLE,
#             "errors": errors,
#             "from_name": app_settings.FORM_NAME,
#         }
#         for error in errors:
#             messages.error(self.request, f"Please Check - {error} & Try Again ")
#             return render(self.request, self.template_name, context)


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
