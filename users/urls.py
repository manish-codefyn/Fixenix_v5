from django.urls import path

from users.views import (
    SignupPageView,
    UserVerify,
    StaffVerify,
    UserCodeVerify,
    StaffCodeVerify,
    UserAccountView,
 
)
from . import bookings

urlpatterns = [


    path("user/dashboard/booking/list", bookings.UserBookingList.as_view(), name="user_booking_list"),
    path("user/bookings/<uuid:pk>/", bookings.UserBookingDetailView.as_view(), name="user_booking_detail"),
    path("user/bookings/<uuid:pk>/pdf", bookings.user_bookings_export_pdf_by_id, name="user_booking_pdf_byid"),
    path("user/bookings/<uuid:pk>/invoice/", bookings.InvoiceDownloadView.as_view(), name="invoice_download"),


    path("staff-verify/", StaffVerify.as_view(), name="staff_verify"),
    path("user-verify/", UserVerify.as_view(), name="user_verify"),
    path("user-verify/code-submit", UserCodeVerify.as_view(), name="user_code_verify"),
    path("user-verify/code-reset", UserVerify.as_view(), name="user_code_reset"),
    path("staff-verify/code-reset", StaffVerify.as_view(), name="staff_code_reset"),
    path(
        "staff-verify/code-submit", StaffCodeVerify.as_view(), name="staff_code_verify"
    ),



    path("user/account/", UserAccountView.as_view(), name="user_dashboard"),
    path("signup/", SignupPageView.as_view(), name="signup"),
    # path("login/1", CustomLoginView.as_view()),
]
