from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View
from django.urls import reverse_lazy
from .models import WorkSheet
from works.form import WorkSheetForm,WorkSheetFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.core.serializers import serialize

from django.utils.dateparse import parse_date
from django.views.generic import CreateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import WorkSheet
from .form import WorkSheetForm, DeviceChecklistFormSet
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.shortcuts import get_object_or_404
from datetime import date
from .utils import render_to_pdf,qr_generate,download_temp_image,send_html_mail
from .models import WorkSheet, DeviceChecklist
from sitesetting.models import Sites  # Your app's settings model

def WorksExportPdfbyId(request, pk):
    """Export a PDF of a WorkSheet by ID including checklist items and QR code."""

    template_name = f"works/reports/export_pdfbyid.html"

    # Fetch WorkSheet instance
    work = get_object_or_404(WorkSheet, id=pk)

    # QR Code Generation
    qr_data = {
        "Customer Name": work.name,
        "Email": work.email,
        "Mobile": work.mobile,
        "Device": work.device_name,
        "Problem": work.device_problem,
        "Updated": work.updated_at,
        "Status": work.status,
        "Work ID": work.work_id,
    }
    qr_code_img = qr_generate(qr_data, size=2, version=2, border=0)

    # Site App Settings
    app_data = Sites.objects.first()

    # Checklist
    checklist_items = work.checklist_items.all()

    context = {
        "app": app_data,
        "logo": getattr(app_data.app_logo, 'url', None) if app_data else None,
        "stamp": getattr(app_data.app_stamp, 'url', None) if app_data else None,

        "work": work,
        "checklist": checklist_items,
        "qr_code": qr_code_img,
        "time": date.today(),
        "doc_name": "Work Sheet Report",
    }

    pdf_name = f"{work.name}_work_sheet.pdf"

    return render_to_pdf(template_name, context, pdf_name)


class WorkSheetListView(ListView):
    model = WorkSheet
    template_name = 'works/list.html'
    context_object_name = 'worksheets'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        startdate = self.request.GET.get('startdate')
        enddate = self.request.GET.get('enddate')

        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(work_id__icontains=search) |
                Q(device_name__icontains=search) |
                Q(device_problem__icontains=search)
            )
        if startdate and enddate:
            queryset = queryset.filter(created_at__date__range=[startdate, enddate])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = WorkSheet.STATUS_CHOICES
        context['form'] = WorkSheetFilterForm(self.request.GET or None)
        return context

class WorkSheetAjaxListView(View):
    def get(self, request):
        # DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        # Custom filters
        status = request.GET.get('status')
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')

        queryset = WorkSheet.objects.all()

        # Apply filters
        if status:
            queryset = queryset.filter(status=status)
        if startdate:
            queryset = queryset.filter(created_at__date__gte=startdate)
        if enddate:
            queryset = queryset.filter(created_at__date__lte=enddate)
        if search_value:
            queryset = queryset.filter(
                Q(name__icontains=search_value) |
                Q(work_id__icontains=search_value) |
                Q(device_name__icontains=search_value) |
                Q(device_problem__icontains=search_value)
            )

        # Counts
        total_records = WorkSheet.objects.count()
        filtered_records = queryset.count()

        # Pagination
        queryset = queryset.order_by('-created_at')[start:start + length]

        # Prepare data
        data = []
        for ws in queryset:
            data.append({
                "work_id": ws.work_id,
                "name": ws.name,
                "mobile": ws.mobile,
                "email": ws.email or "",
                "device_name": ws.device_name,
                "device_problem": ws.device_problem,
                "status": ws.status,
                "status_display": ws.get_status_display(),
                "slug": ws.slug,
            })

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data,
        }, encoder=DjangoJSONEncoder)


class WorkSheetCreateView(CreateView):
    model = WorkSheet
    form_class = WorkSheetForm
    template_name = 'works/create.html'
    success_url = reverse_lazy('work_sheet_list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = DeviceChecklistFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DeviceChecklistFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            worksheet = form.save()
            checklist_items = formset.save(commit=False)
            for item in checklist_items:
                item.worksheet = worksheet
                item.save()
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form, 'formset': formset})


class WorkSheetDetailView(DetailView):
    model = WorkSheet
    template_name = 'works/detail.html'
    context_object_name = 'worksheet'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'



class WorkSheetUpdateView(SuccessMessageMixin, UpdateView):
    model = WorkSheet
    form_class = WorkSheetForm
    template_name = 'works/update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = "Work sheet updated successfully!"
    
    def get_success_url(self):
        return reverse_lazy('work_sheet_detail', kwargs={'slug': self.object.slug})

class WorkSheetDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = WorkSheet
    template_name = 'works/delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('worksheet-list')
    success_message = "Work sheet deleted successfully!"




@require_POST
@login_required
def update_worksheet_status(request, pk):
    try:
        worksheet = WorkSheet.objects.get(pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(WorkSheet.STATUS_CHOICES):
            worksheet.status = new_status
            worksheet.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    except WorkSheet.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Worksheet not found'})