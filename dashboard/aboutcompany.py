from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# alert msg
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import requests
# generic import
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from users.mixins import (
    TestMixinUserEmail,
    TestMixinUserName,
    StaffRequiredMixin,
    email_check,
)
from django.contrib.auth.decorators import user_passes_test

# local  import
from . import app_settings
from sitesetting.models import Sites, AboutCompany
from sitesetting.form import AboutCompanyForm

from . import app_settings


class AboutCompanyDelete(StaffRequiredMixin, TestMixinUserEmail, DeleteView):

    """Delete"""

    template_name = "dashboard/features/list." + app_settings.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = AboutCompany
    context_object_name = "delete"
    success_url = reverse_lazy(app_settings.SUCCESS_URL)
    success_message = "deleted !"


class AboutCompanyCreate(StaffRequiredMixin, CreateView):
    """Create"""

    template_name = (
        "dashboard/aboutcompany/Create." + app_settings.TEMPLATE_EXTENSION
    )
    login_url = reverse_lazy("account_login")
    model = AboutCompany
    form_class = AboutCompanyForm

    def get(self, request, *agrs, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "app_data": Sites.objects.all(),
                "pagename": "About Company",
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Addedd Success Fully.")
        return reverse(app_settings.SUCCESS_URL)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "app_data": Sites.objects.all(),
                "site_name": app_settings.SITE_NAME,
                "pagename": "About Company",
            },
        )


class AboutCompanyUpdate(StaffRequiredMixin,UpdateView):
    """update"""

    template_name = (
        "dashboard/aboutcompany/update." + app_settings.TEMPLATE_EXTENSION
    )
    login_url = reverse_lazy("account_login")
    model = AboutCompany
    success_url = reverse_lazy(app_settings.SUCCESS_URL)
    success_message = "Updated Successfully !"
    context_object_name = "ac"
    form_class = AboutCompanyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_data"] = Sites.objects.all()
        context["pagename"] = "About Company Update"
        return context


class AboutCompanyDetail(StaffRequiredMixin, TestMixinUserEmail, DetailView):
    """detail"""

    template_name = (
        "dashboard/aboutcompany/detail." + app_settings.TEMPLATE_EXTENSION
    )
    login_url = reverse_lazy("account_login")
    model = AboutCompany
    context_object_name = "ac"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_data"] = Sites.objects.all()
        context["pagename"] = "About Company Detail"
        return context

class AboutCompanyList(StaffRequiredMixin, TestMixinUserEmail, ListView):
    """Company LIST VIEWS"""

    template_name = (
        "dashboard/aboutcompany/list." + app_settings.TEMPLATE_EXTENSION
    )
    login_url = reverse_lazy("account_login")
    model = AboutCompany
    context_object_name = "ac"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_data"] = Sites.objects.all()
        context["pagename"] = "About Company List"
        return context