from django.conf import settings
import time
from pathlib import Path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# redirects Imports
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
# msg mixin import
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# date  import
import datetime
import tempfile
import requests
from datetime import date
# Generic Views Imports
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    RedirectView,
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
from .models import WorkSheet
from works.form import WorkSheetForm, StatusUpdateForm
from sitesetting.models import Sites
from sitesetting.form import DateForm
from django.contrib.auth.decorators import user_passes_test
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
from django.template.loader import render_to_string
from .utils import render_to_pdf,qr_generate,download_temp_image,send_html_mail
from django.core.mail import EmailMessage



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def WorkSheetCustomerCopySend(request, pk):
    """Send Worksheet Copy to Customer By Mail"""
    template_name = f"dashboard/works/email/work_sheet.{app_settings.TEMPLATE_EXTENSION}"
    # Fetch the worksheet object
    work = get_object_or_404(WorkSheet, id=pk)
    # QR Code Configuration
    size = 2
    version = 2
    border = 0
    # Extract Work Details
    name = work.name
    email = work.email
    mobile = work.mobile
    device = work.device_name
    problem = work.device_problem
    created = work.created_at
    updated = work.updated_at
    status = work.status
    work_id = work.work_id
    # QR Code Generation
    qr_data = {
        "Customer Name": name,
        "Email": email,
        "Mobile": mobile,
        "Device": device,
        "Problem": problem,
        "Updated": updated,
        "Status": status,
        "Work ID": work_id,
    }
    app_data = Sites.objects.first()
    qr_code_img = qr_generate(qr_data, size, version, border)
    print(app_data)
    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "title": "Work Sheet",
        "name": name,
        "email": email,
        "mobile": mobile,
        "device": device,
        "problem": problem,
        "updated": updated,
        "status": status,
        "work_id": work_id,
        "created": created,
        "time": datetime.date.today(),
        "doc_name": "Work Sheet",
        "qr_code": qr_code_img,
    }
    pdf_name = f"{name}_work_sheet.pdf"
    try:
        # Generate PDF
        pdf_file = render_to_pdf(template_name, context, pdf_name)
        if not pdf_file:
            raise ValueError("PDF generation failed.")
        # Email Configuration
        subject = "Worksheet Created!"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        email_template = f"dashboard/works/email/emails.{app_settings.TEMPLATE_EXTENSION}"
        # Render Email Content
        email_content = render_to_string(email_template, context)
        # Send Email
        email_message = EmailMessage(subject, email_content, from_email, to_email)
        email_message.attach(pdf_name, pdf_file.getvalue(), "application/pdf")
        email_message.content_subtype = "html"  # Set email content type to HTML
        email_message.send()
        messages.success(request, f"Mail sent to {email} successfully!")
    except Exception as e:
        messages.error(request, f"Failed to send mail to {email}. Error: {str(e)}")
    finally:
        return HttpResponseRedirect(reverse_lazy("work_sheet_list"))


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def WorksExportCsv(request):
    """Online Requests Export CSV"""

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="workslist.csv"'
    works = WorkSheet.objects.all()
    writer = csv.writer(response)
    for r in works:
        writer.writerow(
            [
                "Work ID",
                "Name",
                "Mobile",
                "Email",
                "Device Name",
                "Device Problem",
                "Created Date",
            ]
        )
        writer.writerow(
            [
                r.work_id,
                r.name,
                r.mobile,
                r.email,
                r.device_name,
                r.device_problem,
                r.created_at,
            ]
        )
    return response


class WorksUpdate(StaffRequiredMixin,UpdateView):
    """Update"""

    model = WorkSheet
    success_message = "  Successfully Updated!"
    template_name = "dashboard/works/update." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("work_sheet_list")
    fields = ["status"]
    extra_context = {
        "app_data": Sites.objects.all(),
        "pagename": app_settings.PAGE_NAME,
        "page_title": app_settings.PAGE_TITLE,
    }


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def WorksExportPdfbyId(request, pk):
    """Works Export Pdf by ID"""
    template_name = f"dashboard/works/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    # Fetch the worksheet object
    work = get_object_or_404(WorkSheet, id=pk)
    # QR Code Configuration
    size = 2
    version = 2
    border = 0
    # Extract Work Details
    name = work.name
    email = work.email
    mobile = work.mobile
    device = work.device_name
    problem = work.device_problem
    created = work.created_at
    updated = work.updated_at
    status = work.status
    work_id = work.work_id
    # QR Code Generation
    qr_data = {
        "Customer Name": name,
        "Email": email,
        "Mobile": mobile,
        "Device": device,
        "Problem": problem,
        "Updated": updated,
        "Status": status,
        "Work ID": work_id,
    }
    qr_code_img = qr_generate(qr_data, size, version, border)
    # Fetch app data
    app_data = Sites.objects.first()
    # Prepare Context for PDF
    context = {
        "app": app_data,
        "logo": getattr(app_data.app_logo, 'url', None) if app_data else None,
        "stamp": getattr(app_data.app_stamp, 'url', None) if app_data else None,

        "name": name,
        "email": email,
        "mobile": mobile,
        "device": device,
        "problem": problem,
        "updated": updated,
        "status": status,
        "work_id": work_id,
        "created": created,
        "time": date.today(),
        "doc_name": "Work Sheet",
        "qr_code": qr_code_img,
    }

    pdf_name = f"{name}_work_sheet.pdf"

    # Generate and Return PDF
    return render_to_pdf(template_name, context, pdf_name)



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def WorksExportCsv(request):
    """Export CSV"""

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="workslist.csv"'
    works = WorkSheet.objects.all()
    writer = csv.writer(response)
    for r in works:
        writer.writerow(
            [
                "Work ID",
                "Name",
                "Mobile",
                "Email",
                "Device Name",
                "Device Problem",
                "Created Date",
            ]
        )
        writer.writerow(
            [
                r.work_id,
                r.name,
                r.mobile,
                r.email,
                r.device_name,
                r.device_problem,
                r.created_at,
            ]
        )
    return response


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def WorksExportPdfbyDate(request):
    """Export Work Sheets as PDF filtered by date range."""
    template_name = f"dashboard/works/reports/export_pdf_bydate.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "Work_sheet_filtered_list.pdf"
    app_data = Sites.objects.first()
    if request.method == "POST":
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        # Validate date inputs
        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both start date and end date are required.")

        try:
            # Filter worksheets by the provided date range
            data = WorkSheet.objects.filter(
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
            "works": data,
            "time": datetime.date.today(),
            "doc_name": "Work Sheet",
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
        # Handle GET request to display all worksheets as fallback
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "works": WorkSheet.objects.all(),
            "time": datetime.date.today(),
            "doc_name": "Work Sheet",
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
def WorksExportPdfAll(request):
    """Generate and Export PDF for All Work Sheets"""
    template_name = f"dashboard/works/reports/export_pdfall.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "works_list.pdf"
    # Fetch all required data
    works = WorkSheet.objects.all()
    app_data = Sites.objects.first()
    # Context for the PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "works": works,
        "time": datetime.date.today(),
        "doc_name": "Work List",
    }
    try:
        # Generate PDF
        pdf_file = render_to_pdf(template_name, context, pdf_name)
        if not pdf_file:
            raise ValueError("PDF generation failed.")
        return pdf_file
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


class WorkCreate(StaffRequiredMixin, TestMixinUserEmail, CreateView):
    template_name = "dashboard/works/create." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = WorkSheet
    form_class = WorkSheetForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contex = {
            "work_sheet_form": form,
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
            "pagename": app_settings.PAGE_NAME,
            "form_name": app_settings.FORM_NAME,
        }

        return render(request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            from_mail = settings.EMAIL_HOST_USER
            return self.form_valid(form, name, email)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Successfully Added !")
        return reverse("work_sheet_list")

    def form_valid(self, form, name, email):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        form.save()
        context = {
            "title": "Work Sheet !",
            "content": f"Dear {name}.Thank you for Choosing Us!",
        }
        subject = "Worksheet Created !"
        from_mail = settings.EMAIL_HOST_USER
        template_name = (
            "dashboard/works/email/emails." + app_settings.TEMPLATE_EXTENSION
        )
        to_mail = email
        try:
            send_html_mail(subject, context, template_name, to_mail, from_mail)
            return HttpResponseRedirect(self.get_success_url())
        except:
            messages.error(self.request, "Mail Not Sent .! Try again !")
            return HttpResponseRedirect(reverse_lazy("work_sheet_list"))

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """
        errors = form.errors
        context = {
            "form_work": form,
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
            "errors": errors,
            "from_name": app_settings.FORM_NAME,
        }
        for error in errors:
            messages.error(self.request, f"Please Check - {error} & Try Again ")
            return render(self.request, self.template_name, context)


class WorkDetails(StaffRequiredMixin, TestMixinUserEmail, DetailView):
    """DETAIL VIEWS"""

    template_name = "dashboard/works/detail." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = WorkSheet
    context_object_name = "work_sheet"
    data = "www.fixenix.com"
    img = qrcode.make(data, box_size=2)
    # img_name = "qr" + str(time.time()) + ".png"
    # img.save(settings.MEDIA_ROOT + "/" + img_name)
    extra_context = {
        "app_data": Sites.objects.all(),
        "pagename": app_settings.PAGE_NAME,
        "page_title": app_settings.PAGE_TITLE,
        "date": datetime.date.today(),
        # "qr_code_img": img_name,
    }


class WorkList(StaffRequiredMixin, TestMixinUserEmail, ListView):
    """Views By date"""

    form_class = DateForm
    model = WorkSheet
    template_name = "dashboard/works/list." + app_settings.TEMPLATE_EXTENSION
    page_name = app_settings.PAGE_NAME

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form": form,
            "works": self.model.objects.all(),
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
        works = self.model.objects.all()
        context = {
            "works": works.filter(created_at__gte=fromdate),
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
                "works": works.filter(created_at__lte=enddate),
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
                "works": self.model.objects.all(),
                "form": form,
            },
        )
