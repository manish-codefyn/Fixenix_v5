from django.urls import path
from .pdf_email import EmailAttachementView
from .views import (
    WorkList,
    WorkCreate,
    WorkDetails,
    WorksExportPdfAll,
    WorksExportCsv,
    WorksExportPdfbyId,
    WorksExportPdfbyDate,
    WorksUpdate,
    WorkSheetCustomerCopySend,
)


urlpatterns = [
    path("Works/email", EmailAttachementView.as_view(), name="emailattachment"),
    path("Works/", WorkList.as_view(), name="work_sheet_list"),
    path("Works/<uuid:pk>", WorkDetails.as_view(), name="work_sheet"),
    path(
        "Works/<uuid:pk>/update", WorksUpdate.as_view(), name="work_sheet_update"
    ),
    path("Works/create", WorkCreate.as_view(), name="work_sheet_create"),
    path("Works/PDF", WorksExportPdfAll, name="work_sheet_export_pdf_all"),
    path(
        "Works/PDF/f", WorksExportPdfbyDate, name="work_sheet_export_pdf_filtered"
    ),
    path("Works/CSV", WorksExportCsv, name="work_sheet_exportcsv"),
    path(
        "Works/<uuid:pk>/pdf",
        WorksExportPdfbyId,
        name="work_sheet_export_pdf_byid",
    ),
    path(
        "Works/<uuid:pk>/send/worksheet",
        WorkSheetCustomerCopySend,
        name="work_sheet_customer_copy_send",
    ),
]
