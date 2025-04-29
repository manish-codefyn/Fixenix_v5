import time
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
)
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
# local Imports
from sitesetting.models import Sites
from sitesetting.form import DateForm
from pages.models import EstimateRequests
from pages.form import EstimateRequestForm
from . import app_settings
from datetime import date
# 3RD Party
# for pdf export
from . utils import render_to_pdf
# for csv export
import csv
# QR CODE
import io
import qrcode
from .utils import render_to_pdf,qr_generate,download_temp_image
from django.http import HttpResponseBadRequest


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def estimate_requests_export_csv(request):
    """Estimate Requests Export CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="EstimateRequests.csv"'
    EstimateRequests = EstimateRequests.objects.all()
    writer = csv.writer(response)
    for r in EstimateRequests:
        writer.writerow(
            [
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
def estimate_requests_export_pdf_by_id(request, pk):
    """Estimate Request Export PDF by ID"""
    template_name = f"dashboard/estimate_requests/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{pk}_estimate_requests.pdf"
    estimate_request = get_object_or_404(EstimateRequests, id=pk)

    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # Estimate Request Details
    name = estimate_request.name
    email = estimate_request.email
    mobile = estimate_request.mobile
    device = estimate_request.device_name
    problem = estimate_request.device_problem
    created = estimate_request.created_at

    # QR Code Generation
    qr_data = {
        "Customer Name": name,
        "Email": email,
        "Mobile": mobile,
        "Device": device,
        "Problem": problem,
    }
    img_name = qr_generate(qr_data, size, version, border)

    # Fetch app data
    app_data = Sites.objects.first()

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "name": name,
        "email": email,
        "mobile": mobile,
        "device": device,
        "problem": problem,
        "created": created,
        "time": now().date(),
        "doc_name": "Estimate Requests Detail",
        "qr_code": img_name,
    }

    return render_to_pdf(template_name, context, pdf_name)



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def estimate_requests_export_pdf_by_date(request):
    """EstimateRequests Export Pdf by DATE"""
    template_name = (
        f"dashboard/estimate_requests/reports/export_pdf_bydate.{app_settings.TEMPLATE_EXTENSION}"
    )
    pdf_name = "estimate_request_filtered_list.pdf"

    # Fetch app data
    app_data = Sites.objects.first()


    if request.method == "POST":
        # Fetch date range from POST request
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both startdate and enddate are required.")

        # Filter data by date range
        try:
            data = EstimateRequests.objects.filter(
                created_at__date__gte=fromdate, created_at__date__lte=enddate
            )
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        if not data.exists():
            return HttpResponseBadRequest("No estimate requests found for the given dates.")

        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "estimate_requests": data,
            "time": now().date(),
            "doc_name": "Estimate Requests",
        }
    else:
        # Default context if no filtering is applied
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "estimate_requests": EstimateRequests.objects.all(),
            "time": now().date(),
            "doc_name": "Estimate Requests",
        }

    return render_to_pdf(template_name, context, pdf_name)


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def estimate_requests_export_pdf_all(request):
    """Estimate Request Export Pdf ALL"""
    template_name = (
        f"dashboard/estimate_requests/reports/export_pdfall.{app_settings.TEMPLATE_EXTENSION}"
    )
    pdf_name = "estimate_requests_list.pdf"

    # Fetch app data
    app_data = Sites.objects.first()

    # Prepare context for the PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "estimate_requests": EstimateRequests.objects.all(),
        "time": now().date(),
        "doc_name": "Estimate Requests List",
    }

    return render_to_pdf(template_name, context, pdf_name)


class EstimateRequestsListView(ListView):
    """Combined view for listing and filtering Estimate Requests by date."""

    template_name = "dashboard/estimate_requests/list." + app_settings.TEMPLATE_EXTENSION
    model = EstimateRequests
    context_object_name = "estimate_requests"
    form_class = DateForm
    login_url = reverse_lazy("account_login")
    page_name = "Estimate Request Detail"

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            "form": self.form_class(),
            "app_data": Sites.objects.all(),
            "pagename": self.page_name,
            "doc_name": "Estimate Request Detail",
            "date": now().date(),
        })
        return context

    def post(self, request, *args, **kwargs):
        """Handle filtering of requests based on date range."""
        form = self.form_class(request.POST)
        context = {
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": self.page_name,
            "page_title": app_settings.PAGE_TITLE,
        }

        if form.is_valid():
            fromdate = form.cleaned_data.get("startdate")
            enddate = form.cleaned_data.get("enddate")
            query = self.model.objects.all()

            if fromdate:
                query = query.filter(created_at__gte=fromdate)
            if enddate:
                query = query.filter(created_at__lte=enddate)

            context["estimate_requests"] = query
        else:
            context["estimate_requests"] = self.model.objects.all()

        return render(request, self.template_name, context)

class EstimateRequestsDetails(DetailView):
    """DetailView"""

    model = EstimateRequests
    login_url = reverse_lazy("account_login")
    context_object_name = "estimate_request"
    template_name = (
        "dashboard/estimate_requests/detail." + app_settings.TEMPLATE_EXTENSION
    )
    data = "www.fixenix.com"
    # img = qrcode.make(data, box_size=2)
    # img_name = "qr" + str(time.time()) + ".png"
    # img.save(settings.MEDIA_ROOT + "/" + img_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "app_data": Sites.objects.all(),
            "pagename": "Estimate Request Detail",
            "doc_name": "Estimate Request Detail",
            "date": now().date(),
        })
        return context
