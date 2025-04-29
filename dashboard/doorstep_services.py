
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# alert msg
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users.models import CustomUser
from .mixins import StaffRequiredMixin,email_check
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView
from services.models import DoorstepService
from services.forms import DoorstepServiceForm
from .forms import DateForm
from sitesetting.models import Sites
from . import app_settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
# local Imports
from sitesetting.models import Sites
from sitesetting.form import DateForm
from datetime import date
from django.utils.timezone import now
import time
from django.conf import settings
# for csv export
import csv
# QR CODE
import io
import qrcode
from . utils import render_to_pdf,qr_generate,download_temp_image


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def doorstep_services_export_pdf_all(request):
    """Export PDF for All Doorstep Services"""
    login_url = reverse_lazy("account_login")
    template_name = (
        "dashboard/doorstep_services/reports/export_pdfall."
        + app_settings.TEMPLATE_EXTENSION
    )
    pdf_name = "services_list.pdf"

    # Fetch the app data (assuming only one app data record exists)
    app_data = Sites.objects.first()

    # Fetch all doorstep services
    doorstep_services = DoorstepService.objects.all()

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "doorstep_services": doorstep_services,
        "time": date.today(),
        "doc_name": "Services List",
    }

    return render_to_pdf(template_name, context, pdf_name)


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def doorstep_services_export_csv(request):
    """ Export CSV"""
    login_url = reverse_lazy("account_login")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="doorstep-services.csv"'
    DoorstepServices = DoorstepService.objects.all()
    writer = csv.writer(response)
    for r in DoorstepServices:
        writer.writerow(
            [
                "Service Name",
                "Service Price",
                "Offer Price",
                "status",
                "Rating",
                "Created Date",
            ]
        )
        writer.writerow(
            [
                r.service_name,
                r.price,
                r.offer_price,
                r.status,
                r.rating,
                r.updated_at,
            ]
        )
    return response


class DoorstepServiceListView(StaffRequiredMixin, ListView):
    """View and filter Doorstep Services by date."""

    template_name = "dashboard/doorstep_services/list." + app_settings.TEMPLATE_EXTENSION
    model = DoorstepService
    context_object_name = "doorstep_services"
    form_class = DateForm
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        """Provide default context for template rendering."""
        context = super().get_context_data(**kwargs)
        context.update({
            "form": self.form_class(),
            "pagename": "Doorstep Service List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
            "date": now().date(),
        })
        return context

    def post(self, request, *args, **kwargs):
        """Handle filtering by startdate and enddate."""
        form = self.form_class(request.POST)
        context = {
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": "Doorstep Service List",
            "page_title": app_settings.PAGE_TITLE,
        }

        if form.is_valid():
            fromdate = form.cleaned_data.get("startdate")
            enddate = form.cleaned_data.get("enddate")
            query = self.model.objects.all()

            # Correct field name for filtering
            if fromdate:
                query = query.filter(requested_at__gte=fromdate)  # Replace `created_at` with `requested_at`
            if enddate:
                query = query.filter(requested_at__lte=enddate)  # Replace `created_at` with `requested_at`

            context["doorstep_services"] = query
            messages.success(request, "Filter applied successfully!")
        else:
            context["doorstep_services"] = self.model.objects.all()
            messages.error(request, "Invalid date range. Please try again.")

        return render(request, self.template_name, context)


# CreateView for adding a new service
class DoorstepServiceCreateView(StaffRequiredMixin,SuccessMessageMixin,CreateView):
    model = DoorstepService
    form_class = DoorstepServiceForm
    template_name = 'dashboard/doorstep_services/service_form.html'
    success_url = reverse_lazy('dashboard:doorstep_service_list')

# UpdateView for editing an existing service
class DoorstepServiceUpdateView(StaffRequiredMixin,SuccessMessageMixin,UpdateView):
    model = DoorstepService
    form_class = DoorstepServiceForm
    template_name = 'dashboard/doorstep_services/service_form.html'
    success_url = reverse_lazy('dashboard:doorstep_service_list')

# DeleteView for deleting a service
class DoorstepServiceDeleteView(StaffRequiredMixin,SuccessMessageMixin,DeleteView):
    model = DoorstepService
    template_name = 'dashboard/doorstep_services/service_confirm_delete.html'
    success_url = reverse_lazy('dashboard:doorstep_service_list')

        


   
        
        




