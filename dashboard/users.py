from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# redirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse, HttpResponseBadRequest

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
# date time
import datetime
# template loader
from django.template import loader
# 3RD Party
import csv
# LOCAL
from . utils import render_to_pdf
from .import app_settings
from sitesetting.form import DateForm
from sitesetting.models import Sites
from users.models import CustomUser
from . utils import render_to_pdf,qr_generate,download_temp_image
from django.utils.timezone import now
from django.shortcuts import get_object_or_404


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def UsersExportPdfAll(request):
    """Export all users as a PDF."""
    template_name = f"dashboard/users/reports/export_pdfall.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "users_list.pdf"
    app_data = Sites.objects.first()

    try:
        # Fetch all users
        users = CustomUser.objects.all()
        if not users.exists():
            return HttpResponse("No users found.", status=404)

        # Context for the PDF
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "data": users,
            "time": datetime.date.today(),
            "doc_name": "Users List",
        }

        # Generate PDF
        pdf_file = render_to_pdf(template_name, context, pdf_name)
        if not pdf_file:
            raise ValueError("PDF generation failed.")
        return pdf_file

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
    

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def users_export_pdf_by_date(request):
    """Export Users as PDF filtered by date range."""
    template_name = f"dashboard/users/reports/export_pdf_by_date.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = "users_filtered_list.pdf"
    app_data = Sites.objects.first()
    time = datetime.date.today()

    if request.method == "POST":
        fromdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        # Validate date inputs
        if not fromdate or not enddate:
            return HttpResponseBadRequest("Both start date and end date are required.")

        try:
            # Filter users by the provided date range
            data = CustomUser.objects.filter(
                date_joined__date__gte=fromdate, date_joined__date__lte=enddate
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
            "data": data,
            "time": time,
            "doc_name": "Users List",
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
        # Handle GET request to display all users as fallback
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "data": CustomUser.objects.all(),
            "time": time,
            "doc_name": "Users List",
        }

        try:
            # Generate and return the PDF for all users
            pdf_file = render_to_pdf(template_name, context, pdf_name)
            if not pdf_file:
                raise ValueError("PDF generation failed.")
            return pdf_file
        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


class UsersList(StaffRequiredMixin, TestMixinUserEmail, ListView):
    """Staff Users Views By date"""

    template_name = "dashboard/users/list." + app_settings.TEMPLATE_EXTENSION
    form_class = DateForm
    model = CustomUser
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contex = {
            "form": form,
            "users": self.model.objects.all(),
            "pagename": "Users List",
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
        users = self.model.objects.all()
        context = {
            "users": users.filter(created_at__gte=fromdate),
            "form": form,
            "app_data": Sites.objects.all(),
            "pagename": "Users List",
            "app_data": Sites.objects.all(),
            "page_title": app_settings.PAGE_TITLE,
        }
        if fromdate:
            return render(self.request, self.template_name, context)
        if enddate:
            context = {
                "users": users.filter(created_at__lte=enddate),
                "form": form,
                "pagename": "Users List",
                "app_data": Sites.objects.all(),
                "page_title": app_settings.PAGE_TITLE,
            }
            return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        form = DateForm
        data = self.model.objects.all()
        return render(
            self.request,
            self.template_name,
            {
                "users": data,
                "form": form,
            },
        )


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def UsersExportCsv(request):
    """Users Export CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users.csv"'
    users = CustomUser.objects.all()
    writer = csv.writer(response)
    for u in users:
        writer.writerow(
            [
                "Username",
                "Email",
            ]
        )
        writer.writerow(
            [
                u.username,
                u.email,
            ]
        )
    return response


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def user_export_pdf_by_id(request, pk):
    """Export User PDF by ID"""
    template_name = f"dashboard/users/reports/export_pdfbyid.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{id}_user_details.pdf"
    
    # Fetch the user object
    user = get_object_or_404(CustomUser, id=pk)
    
    # Fetch the app data (assuming only one app data record exists)
    app_data = Sites.objects.first()
    
    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # QR Code Generation
    qr_data = {
        "User Name": user.username,
        "Email": user.email,
        "Full Name": user.get_full_name(),
        "Phone": user.phone_number if hasattr(user, 'phone_number') else "N/A",
        "User ID": user.id,
    }
    img_name = qr_generate(qr_data, size, version, border)

    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "username": user.username,
        "email": user.email,
        "full_name": user.get_full_name(),
        "phone_number": user.phone_number if hasattr(user, 'phone_number') else None,
        "photo_local": download_temp_image(user.profile_picture.url) if hasattr(user, 'profile_picture') and user.profile_picture else None,
        "user_id": user.id,
        "date_joined": user.date_joined,
        "time": now().date(),
        "doc_name": "User Detail",
        "img_name": img_name,
    }

    try:
        # Generate and return the PDF
        pdf_file = render_to_pdf(template_name, context, pdf_name)
        if not pdf_file:
            raise ValueError("PDF generation failed.")
        return pdf_file
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)



class UsersDetail(StaffRequiredMixin, TestMixinUserEmail, DetailView):
    """Users Detail view"""

    model = CustomUser
    context_object_name = "users"
    template_name = "dashboard/users/detail." + app_settings.TEMPLATE_EXTENSION
    login_url = "account_login"
    extra_context = {
        "page_title": app_settings.PAGE_TITLE,
        "pagename": "Users Details",
        "app_data": Sites.objects.all(),
    }
