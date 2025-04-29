from django.urls import path
from .views import DashboardView
from users.views import SignupPageView,UserAccountView


app_name = "dashboard"
from . import doorstep_services 
from . import estimate_requests 
from . import sites 
from . import users
from . import faq
from . import aboutcompany
from . import brand
from . import messages
from . import feedback
from . import payments
from . import bookings
from . import employees
from . import delivery
 

urlpatterns = [

    path('delivery/list', delivery.DeliveryListView.as_view(), name='delivery_list'),
    path('delivery/<uuid:pk>/', delivery.DeliveryDetailView.as_view(), name='deliveries'),
    path('delivery/pdf-all/', delivery.DeliveryExportPdfAll.as_view(), name='delivery_pdf_all'),
    path('delivery/<uuid:pk>/export-pdf/', delivery.delivery_export_pdf_by_id, name='delivery_export_pdf_by_id'),
    path('delivery/<uuid:pk>/update-status/', delivery.DeliveryStatusUpdateView.as_view(), name='delivery_status_update'),
    path('deliveries/export-csv/', delivery.DeliveriesExportCSVView.as_view(), name='deliveries_export_csv'),
    path('deliveries/export-pdf-by-date/', delivery.DeliveryExportPDFByDateView.as_view(), name='delivery_export_pdf_by_date'),
   

    path('employee/', employees.EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', employees.EmployeeCreateView.as_view(), name='employee_add'),
    path('employee/<uuid:pk>/', employees.EmployeeDetailView.as_view(), name='employees'),
    path('employee/<uuid:id>/export-pdf/', employees.employees_export_pdf_by_id, name='employee_export_pdf'),
    path('employee/<uuid:pk>/update/', employees.EmployeeEditView.as_view(), name='employee_edit'),
    path('employee-list/export/', employees.EmployeeExportPdfAll,name='export_employee_list'),
    path('employee/<uuid:pk>/delete/', employees.EmployeeDeleteView.as_view(), name='employee_delete'),  # UUID for PK
    path('employee/<uuid:pk>/id-card/', employees.EmployeeIDCardView.as_view(), name='employee_id_card'),


    path('payments/list', payments.PaymentsListView.as_view(), name='payments_list'),
    path('payments/<uuid:pk>/', payments.PaymentsDetailsViews.as_view(), name='payments'),
    path('payments/<uuid:pk>/update-status/', payments.PaymentStatusUpdateView.as_view(), name='update_payment_status'),
    path('payments/<uuid:pk>/generate-invoice', payments.GenerateInvoiceAndSendEmailView.as_view(), name='generate_invoice'),
    path('payments/<uuid:pk>/pdf', payments.payments_export_pdf_by_id, name='payments_export_pdf_by_id'),
    path('payments/pdf/', payments.PaymentsExportPdfAllView.as_view(), name='payments_export_pdf_all'),
    path('payments/pdf/by/date', payments.PaymentsExportPdfAllView.as_view(), name='payments_export_pdf_bydate'),
    path('payments/csv', payments.payments_export_csv, name='payments_export_csv'),


    path('Bookings/list', bookings.BookingsListView.as_view(), name='bookings_list'),
    path('bookings/<uuid:pk>/', bookings.BookingsDetailsViews.as_view(), name='bookings'),
    path('bookings/<uuid:pk>/update-status/', bookings.BookingStatusUpdateView.as_view(), name='update_booking_status'),
    path('bookings/<uuid:pk>/pdf', bookings.bookings_export_pdf_by_id, name='bookings_export_pdf_by_id'),
    path('bookings/pdf/', bookings.BookingsExportPdfAllView.as_view(), name='bookings_export_pdf_all'),
    path('bookings/pdf/by/date', bookings.BookingsExportPdfAllView.as_view(), name='bookings_export_pdf_bydate'),
    path('bookings/csv', bookings.bookings_export_csv, name='bookings_export_csv'),

    path("feedback/list/", feedback.FeedbackList.as_view(), name="feedback_list"),
    path("message/", messages.MessageList.as_view(), name="msg_list"),
        # staff brand
    path("brand/", brand.BrandList.as_view(), name="brand_list"),
    path("brand/<uuid:pk>", brand.BrandDetail.as_view(), name="brand"),
    path("brand/<uuid:pk>/update", brand.BrandUpdate.as_view(), name="brand_update"),
    path("brand/<uuid:pk>/delete", brand.BrandDelete.as_view(), name="brand_delete"),
    path("brand/create", brand.BrandCreate.as_view(), name="brand_create"),
    path("brand/PDFall", brand.BrandExportPdfAll, name="brand_export_pdf_all"),
    path("brand/CSV", brand.BrandExportCsv, name="brand_export_csv"),
    # staff AboutCompany
    path("aboutcompany", aboutcompany.AboutCompanyList.as_view(), name="aboutcompany_list"),
    path("aboutcompany/create",aboutcompany.AboutCompanyCreate.as_view(),name="aboutcompany_create",),
    path("aboutcompany/<uuid:pk>",aboutcompany.AboutCompanyDetail.as_view(), name="aboutcompany",),
    path("aboutcompany/<uuid:pk>/delete",aboutcompany.AboutCompanyDelete.as_view(), name="aboutcompany_delete",),
    path("aboutcompany/<uuid:pk>/update",aboutcompany.AboutCompanyUpdate.as_view(),name="aboutcompany_update",),
        # staff Faq
    path("faq", faq.FaqList.as_view(), name="faq_list"),
    path("faq/create", faq.FaqCreate.as_view(), name="faq_create"),
    path("faq/<uuid:pk>", faq.FaqDetail.as_view(), name="faq"),
    path("faq/<uuid:pk>/update", faq.FaqUpdate.as_view(), name="faq_update"),
    path("faq/<uuid:pk>/delete", faq.FaqDelete.as_view(), name="faq_delete"),
    # staff users section
    path("users", users.UsersList.as_view(), name="users_list"),
    path("users/exportpdfbydate", users.users_export_pdf_by_date, name="users_export_bydate"),
    path("users/pdf",users.UsersExportPdfAll, name="users_exportpdf_all"),
    path("users/csv", users.UsersExportCsv, name="users_exportcsv"),
    path("users/<uuid:pk>/pdf", users.user_export_pdf_by_id, name="users_exportpdf_byid"),
    path("users/<uuid:pk>", users.UsersDetail.as_view(), name="users"),
    # staff site setting  section
    path("sites/", sites.SitesList.as_view(), name="site_list"),
    path("sites/<uuid:pk>", sites.SitesDetail.as_view(), name="sites"),
    path("sites/<uuid:pk>/update", sites.SitesUpdate.as_view() , name="update_site"),
    path("sites/<uuid:pk>/delete", sites.SitesDelete.as_view(),  name="delete_site"),
    path("sites/Create", sites.SitesCreate.as_view(), name="sites_create"),


    path("EstimateRequests/",estimate_requests.EstimateRequestsListView.as_view(),name="estimate_requests_list",),
    path("EstimateRequests/<uuid:pk>", estimate_requests.EstimateRequestsDetails.as_view(), name="estimate_requests"),

    path("EstimateRequests/ExportPdfAll",estimate_requests.estimate_requests_export_pdf_all,name="estimate_requests_list_pdf_export",),
    path("EstimateRequests/ExportPdfFiltered",estimate_requests.estimate_requests_export_pdf_by_date,name="estimate_requests_list_pdf_export_bydate",),
    path("EstimateRequests/<uuid:pk>/pdf",estimate_requests.estimate_requests_export_pdf_by_id,name="estimate_requests_list_pdf_export_by_id",),
    path("EstimateRequests/Csv",estimate_requests.estimate_requests_export_csv,name="estimate_requests_list_export_csv",),

    path('doorstep-services/', doorstep_services.DoorstepServiceListView.as_view(), name='doorstep_service_list'),
    path('doorstep-services/create/', doorstep_services.DoorstepServiceCreateView.as_view(), name='doorstep_service_create'),
    path('doorstep-services/<uuid:pk>/update/', doorstep_services.DoorstepServiceUpdateView.as_view(), name='doorstep_service_update'),
    path('doorstep-services/<uuid:pk>/delete/', doorstep_services.DoorstepServiceDeleteView.as_view(), name='doorstep_service_delete'),
    path('doorstep-services/export-csv', doorstep_services.doorstep_services_export_csv, name='doorstep_service_export_csv'),
    path('doorstep-services/export-pdf', doorstep_services.doorstep_services_export_pdf_all, name='doorstep_service_export_pdf'),
    path('dashboard/', DashboardView.as_view(), name='index'),  # Dashboard view at /admin/dashboard/
   
]


