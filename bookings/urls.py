from django.urls import path
from .views import ( BookingCreateView,BookingListView, 
                    BookingUpdateView,PaymentSuccessView,TrackBookingView,
                    RepairServiceView, VerifyOTPView,BookingSuccess,ResendOTPView,CheckRepairStatusView,
                    load_device_models, load_device_problems,load_device_names,CalculateDistanceView ,TrackingServiceView,BookingSuccessView
                    )
from services.views import DoorstepServiceDetailView



urlpatterns = [

   

    path('ajax/load-device-names/', load_device_names, name='load-device-names'),
    path('ajax/load-device-models/', load_device_models, name='ajax_load_device_models'),
    path('ajax/load-device-problems/', load_device_problems, name='ajax_load_device_problems'),
    path('repair-status/', CheckRepairStatusView.as_view(), name='check_repair_status'),


    path('best-mobile-laptop-repair-siliguri-book/', RepairServiceView.as_view(), name='book_repair'),
    path('repair-email-verify/', VerifyOTPView.as_view(), name='rep-otp-verify'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('success/', BookingSuccess.as_view(), name='repair_success'),

    path("booking-success/", BookingSuccessView.as_view(), name="booking-success"),
    path("services/<uuid:pk>/book", BookingCreateView.as_view(), name="book_service"),
    path('calculate-distance/', CalculateDistanceView.as_view(), name='calculate_distance'),
    path('tracking/', TrackingServiceView.as_view(), name='tracking'),
    path('track-booking/', TrackBookingView.as_view(), name='track-booking'),
    path('bookings/<uuid:pk>/payment/verify/', PaymentSuccessView.as_view(), name='verify_payment'),
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path("bookings/<uuid:pk>/update/", BookingUpdateView.as_view(), name="update_booking"),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment_success'),
]
