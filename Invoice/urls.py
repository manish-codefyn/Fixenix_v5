from django.urls import path

from Invoice.views import (
    InvoiceList,
    InvoiceCreateView,
    InvoiceDetail,
    InvoiceUpdate,
    InvoiceT,
    InvoiceExportPdfbyId,
    invoiceExportPdfAll,
    invoiceExportPdfByDate,
)

urlpatterns = [
    path("Invoice/", InvoiceList.as_view(), name="invoice_list"),
    path("Invoice/t", InvoiceT.as_view(), name="invoice_t"),
    path("Invoice/create", InvoiceCreateView.as_view(), name="invoice_create"),
    path("Invoice/<uuid:pk>", InvoiceDetail.as_view(), name="invoice"),
    path("Invoice/pdf/all", invoiceExportPdfAll, name="invoice_list_pdf"),
    path("Invoice/pdf/by/date", invoiceExportPdfByDate, name="invoice_list_pdf_by_date"),
    path("Invoice/<uuid:pk>/update", InvoiceUpdate.as_view(), name="invoice_update", ),
    path("Invoice/<uuid:pk>/pdf",InvoiceExportPdfbyId,name="invoice_pdf",),
]
