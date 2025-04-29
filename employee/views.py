# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from .models import Employee
# from .forms import EmployeeForm
# from django.shortcuts import render
# from django.views.generic import ListView
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required, user_passes_test
# from .models import Employee  # Assuming you have an Employee model
# from .forms import DateForm  # Assuming you have a DateForm for filtering
# from django.utils.timezone import now
# from . import app_settings
# from sitesetting.models import (Sites)
# from django.shortcuts import render
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# from .forms import DateForm  # Assuming you have a DateForm for filtering
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import datetime
# from django.conf import settings
# import os
# from users.mixins import TestMixinUserEmail, TestMixinUserName, StaffRequiredMixin,email_check

# def fetch_resources(uri, rel):
#        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
#        return path


# def render_to_pdf(template_src, context_dict={}, pdf_name = {}):
   
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
#     pdf_status = pisa.CreatePDF(html.encode("ISO-8859-1"), dest=response,link_callback=fetch_resources )

#     if pdf_status.err:
#         return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

#     return response


# @login_required(login_url=settings.LOGIN_URL)
# @user_passes_test(email_check)
# def EmployeeExportPdfAll(request):
#     """Users Export Pdf all"""
#     template_name = (
#         "employees/reports/export_pdfall." + app_settings.TEMPLATE_EXTENSION
#     )
#     data = Employee.objects.all()
#     pdf_name = "employees_list.pdf"
#     time = datetime.date.today()
#     return render_to_pdf(
#         template_name,
#         {
#             "app_data": Sites.objects.all(),
#             "employee": data,
#             "time": time,
#             "doc_name": "Employees List",
#         },
#         pdf_name,
#     )


# class EmployeeEditView(UpdateView):
#     model = Employee
#     form_class = EmployeeForm
#     template_name = 'employees/employee_edit.html'
#     success_url = reverse_lazy('employee_list')  # Redirect to the employee list page after saving

#     def form_valid(self, form):
#         """
#         Override this method to perform additional actions if needed when the form is valid.
#         """
#         form.save()
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         """
#         Override this method to handle what happens when the form is invalid.
#         """
#         return super().form_invalid(form)
    

# class EmployeeListView(ListView):
#     """View and filter Employees by hire date."""

#     template_name = "employees/list." + app_settings.TEMPLATE_EXTENSION
#     model = Employee
#     context_object_name = "employees"
#     form_class = DateForm
#     login_url = reverse_lazy("account_login")

#     def get_context_data(self, **kwargs):
#         """Provide default context for template rendering."""
#         context = super().get_context_data(**kwargs)
#         context.update({
#             "form": self.form_class(),
#             "pagename": "Employee List",
#             "app_data": Sites.objects.all(),
#             "page_title": app_settings.PAGE_TITLE,
#             "date": now().date(),
#         })
#         return context

#     def post(self, request, *args, **kwargs):
#         """Handle filtering by startdate and enddate."""
#         form = self.form_class(request.POST)
#         context = {
#             "form": form,
#             "app_data": Sites.objects.all(),
#             "pagename": "Employee List",
#             "page_title": app_settings.PAGE_TITLE,
#         }

#         if form.is_valid():
#             fromdate = form.cleaned_data.get("startdate")
#             enddate = form.cleaned_data.get("enddate")
#             query = self.model.objects.all()

#             # Correct field name for filtering (e.g., hire_date)
#             if fromdate:
#                 query = query.filter(hire_date__gte=fromdate)
#             if enddate:
#                 query = query.filter(hire_date__lte=enddate)

#             context["employees"] = query
#             messages.success(request, "Filter applied successfully!")
#         else:
#             context["employees"] = self.model.objects.all()
#             messages.error(request, "Invalid date range. Please try again.")

#         return render(request, self.template_name, context)



# class EmployeeCreateView(CreateView):
#     model = Employee
#     form_class = EmployeeForm
#     template_name = 'employees/form.html'
#     success_url = reverse_lazy('employee_list')


# class EmployeeDeleteView(DeleteView):
#     model = Employee
#     template_name = 'employees/confirm_delete.html'
#     success_url = reverse_lazy('employee_list')
