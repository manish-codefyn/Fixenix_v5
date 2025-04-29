from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# redirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect

# generic import
from django.views.generic import (
    CreateView,
    DeleteView,
    View,
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
)
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
from django.contrib.auth.decorators import user_passes_test

# alert Msg
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# local import
from . import app_settings
from sitesetting.models import Sites, Brands
from sitesetting.form import BrandForm, DateForm
from . utils import render_to_pdf

# date time
import datetime

# 3rd party
import csv


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def BrandExportCsv(request):
    """Brand Export CSV"""

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="brands.csv"'
    brand = Brands.objects.all()
    writer = csv.writer(response)
    for b in brand:
        writer.writerow(
            [
                b.name,
                b.pic,
            ]
        )
    return response


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def BrandExportPdfAll(request):
    """Staff Slider Export Pdf ALL"""
    template_name = (
        "dashboard/brand/reports/export_pdfall." + app_settings.TEMPLATE_EXTENSION
    )
    pdf_name = "brand_list.pdf"
    context = {
        "app_data": Sites.objects.all(),
        "brand": Brands.objects.all(),
        "time": datetime.date.today(),
        "doc_name": "Brand_list",
    }
    return render_to_pdf(template_name, context, pdf_name)


class BrandDelete(StaffRequiredMixin, TestMixinUserEmail, DeleteView):
    """DeleteView"""

    template_name = "dashboard/brand/list." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = Brands
    context_object_name = "delete"
    success_url = reverse_lazy("dashboard:brand_list")
    success_message = "Item Deleted Successfully !"


class BrandUpdate(StaffRequiredMixin, TestMixinUserEmail, UpdateView):
    """UpadteView"""

    template_name = "dashboard/brand/update." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = Brands
    success_url = reverse_lazy("dashboard:brand_list")
    success_message = "Updated !"
    form_class = BrandForm
    extra_context = {
        "app_data": Sites.objects.all(),
        "pagename": "Brand",
        "page_titel": app_settings.PAGE_TITLE,
    }


class BrandDetail(StaffRequiredMixin, TestMixinUserEmail, DetailView):
    """DetailView"""

    model = Brands
    login_url = reverse_lazy("account_login")
    context_object_name = "brand"
    template_name = "dashboard/brand/detail." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "app_data": Sites.objects.all(),
        "pagename": "Brand",
        "page_titel": app_settings.PAGE_TITLE,
    }


class BrandCreate(StaffRequiredMixin, TestMixinUserEmail, CreateView):
    """createView"""

    template_name = "dashboard/brand/create." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = Brands
    form_class = BrandForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contex = {
            "form": form,
            "pagename": "Create Brand",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }

        return render(request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Created Successfully!")
        return reverse("dashboard:brand_list")

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """
        errors = form.errors
        context = {
            "form": form,
            "pagename": "Create Brand",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
            "errors": errors,
        }
        for error in errors:
            messages.error(self.request, f"Please Check - {error} & Try Again ")
            return render(self.request, self.template_name, context)


class BrandList(StaffRequiredMixin, TestMixinUserEmail, ListView):
    """Views By date"""

    login_url = reverse_lazy("account_login")
    form_class = DateForm
    model = Brands
    template_name = "dashboard/brand/list." + app_settings.TEMPLATE_EXTENSION


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form": form,
            "brand": self.model.objects.all(),
            "pagename": "Brand List",
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
            "brand": self.model.objects.all().filter(created_at__gte=fromdate),
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": "Brand list",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        if fromdate:
            return render(self.request, self.template_name, context)
        if enddate:
            context = {
                "brand": self.model.objects.all().filter(created_at__lte=enddate),
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
                "brand": self.model.objects.all(),
                "form": form,
            },
        )
