from django.urls import path
from .views import (
    WorkSheetListView,
    WorkSheetDetailView,
    WorkSheetCreateView,
    WorkSheetUpdateView,
    WorkSheetDeleteView,
    update_worksheet_status,
     WorkSheetAjaxListView,
     WorksExportPdfbyId
)

# app_name = 'worksheet'

urlpatterns = [
    # List view
   
    path('list/', WorkSheetListView.as_view(), name='work_sheet_list'),
    path('create/', WorkSheetCreateView.as_view(), name='work_sheet_create'),
    path('worksheets/ajax/', WorkSheetAjaxListView.as_view(), name='worksheet_ajax_list'),
    path('<uuid:pk>/update-status/', update_worksheet_status, name='update-status'),
    path('<slug:slug>/update/', WorkSheetUpdateView.as_view(), name='work_sheet_update'),
    path('<uuid:pk>/pdf/', WorksExportPdfbyId, name='work_sheet_pdf'),
    path('<slug:slug>/delete/', WorkSheetDeleteView.as_view(), name='delete'),

    # Generic route last
    path('<slug:slug>/', WorkSheetDetailView.as_view(), name='work_sheet_detail'),
]