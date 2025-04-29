from django.views.generic import ListView, CreateView, UpdateView, DeleteView,View
from django.urls import reverse_lazy
from employee.forms import EmployeeForm
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from employee.models import Employee  # Assuming you have an Employee model
from .forms import DateForm  # Assuming you have a DateForm for filtering
from django.utils.timezone import now
from . import app_settings
from sitesetting.models import (Sites)
from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from employee.forms import DateForm  # Assuming you have a DateForm for filtering
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.conf import settings
import os
from users.mixins import TestMixinUserEmail, TestMixinUserName, StaffRequiredMixin,email_check
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from xhtml2pdf import pisa
from . utils import render_to_pdf,qr_generate,download_temp_image
# for csv export
import csv
# QR CODE
import io
from django.template import loader
# date  import
from django.utils.timezone import now


class EmployeeIDCardView(View):
    """Generate Employee ID Card as PDF."""

    template_name = "dashboard/employees/id_card_template.html"

    def get(self, request, pk):
        # Fetch employee and app data
        employee = get_object_or_404(Employee, id=pk)
        app_data = Sites.objects.first()

        # Generate QR Code
        qr_data = {
            "Name": employee.name,
            "Employee ID": employee.employee_id,
            "Email": employee.email,
            "Phone": employee.phone,
            "Designation": employee.designation,
            "Department": employee.department,
        }
        qr_image = qr_generate(qr_data, size=2, version=2, border=0)

        # Prepare context for the template
        context = {
            "app": app_data,
            "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
            "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
            "name": employee.name,
            "email": employee.email,
            "phone": employee.phone,
            "address": employee.address,
            "designation": employee.designation,
            "department": employee.department,
            "employee_id": employee.employee_id,
            "company": "Fixenix",
            "website": "www.fixenix.com",
            "photo_local": download_temp_image(employee.photo.url) if employee.photo else None,
            "created_at": employee.created_at,
            "qr_code": qr_image,
            "time": datetime.date.today(),
        }

        # Generate PDF
        pdf_name = f"{employee.name}_ID_Card.pdf"
        try:
            pdf_file = render_to_pdf(self.template_name, context, pdf_name)
            if not pdf_file:
                raise ValueError("PDF generation failed.")
            return pdf_file
        except Exception as e:
            return HttpResponse(f"Error generating ID card: {str(e)}", status=500)


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def employees_export_pdf_by_id(request, id):
    """Export Employee PDF by ID"""
    template_name = f"dashboard/employees/employee_pdf.{app_settings.TEMPLATE_EXTENSION}"
    pdf_name = f"{id}_employees.pdf"
    
    # Fetch the employee object
    employee = get_object_or_404(Employee, id=id)
    
    # Fetch the app data (assuming only one app data record exists)
    app_data = Sites.objects.first()
    
    # QR Code Configuration
    size = 2
    version = 2
    border = 0

    # QR Code Generation
    qr_data = {
        "Customer Name": employee.name,
        "Email": employee.email,
        "Mobile": employee.phone,
        "Address": employee.address,
        "Employee Id": employee.employee_id,
    }
    img_name = qr_generate(qr_data, size, version, border)
    # Context for PDF
    context = {
        "app": app_data,
        "logo": download_temp_image(app_data.app_logo.url) if app_data and app_data.app_logo else None,
        "stamp": download_temp_image(app_data.app_stamp.url) if app_data and app_data.app_stamp else None,
        "name": employee.name,
        "email": employee.email,
        "mobile": employee.phone,
        "address": employee.address,
        "photo_local": download_temp_image(employee.photo.url) if employee.photo else None,
        "employee_id": employee.employee_id,
        "created": employee.created_at,
        "time": now().date(),
        "doc_name": "Employee Detail",
        "img_name": img_name,
    }

    return render_to_pdf(template_name, context, pdf_name)



class EmployeeDetailView(StaffRequiredMixin,DetailView):
    """View to display details of a single employee."""
    
    model = Employee
    template_name = "dashboard/employees/employee_detail.html"
    context_object_name = "employee"

    def get_object(self, queryset=None):
        """
        Override the get_object method to handle cases where
        the employee does not exist or the ID is invalid.
        """
        employee_id = self.kwargs.get("pk")
        try:
            return get_object_or_404(Employee, pk=employee_id)
        except (Employee.DoesNotExist, ValueError):
            raise Http404("Employee not found.")

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template if required.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Employee Detail"
        return context


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(email_check)
def EmployeeExportPdfAll(request):
    """Users Export Pdf all"""
    template_name = (
        "dashboard/employees/reports/export_pdfall." + app_settings.TEMPLATE_EXTENSION
    )
    data = Employee.objects.all()
    pdf_name = "employees_list.pdf"
    time = datetime.date.today()
    return render_to_pdf(
        template_name,
        {
            "app_data": Sites.objects.all(),
            "employee": data,
            "time": time,
            "doc_name": "Employees List",
        },
        pdf_name,
    )


class EmployeeEditView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'dashboard/employees/employee_edit.html'
    success_url = reverse_lazy('dashboard:employee_list')  # Redirect to the employee list page after saving

    def form_valid(self, form):
        """
        Override this method to perform additional actions if needed when the form is valid.
        """
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Override this method to handle what happens when the form is invalid.
        """
        return super().form_invalid(form)
    

class EmployeeListView(ListView):
    """View and filter Employees by hire date."""

    template_name = "dashboard/employees/list." + app_settings.TEMPLATE_EXTENSION
    model = Employee
    context_object_name = "employees"
    form_class = DateForm
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        """Provide default context for template rendering."""
        context = super().get_context_data(**kwargs)
        context.update({
            "form": self.form_class(),
            "pagename": "Employee List",
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
            "pagename": "Employee List",
            "page_title": app_settings.PAGE_TITLE,
        }

        if form.is_valid():
            fromdate = form.cleaned_data.get("startdate")
            enddate = form.cleaned_data.get("enddate")
            query = self.model.objects.all()

            # Correct field name for filtering (e.g., hire_date)
            if fromdate:
                query = query.filter(hire_date__gte=fromdate)
            if enddate:
                query = query.filter(hire_date__lte=enddate)

            context["employees"] = query
            messages.success(request, "Filter applied successfully!")
        else:
            context["employees"] = self.model.objects.all()
            messages.error(request, "Invalid date range. Please try again.")

        return render(request, self.template_name, context)



class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'dashboard/employees/form.html'
    success_url = reverse_lazy('dashboard:employee_list')


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'dashboard/employees/confirm_delete.html'
    success_url = reverse_lazy('employee_list')
