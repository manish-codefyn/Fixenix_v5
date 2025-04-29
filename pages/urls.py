from django.urls import path

from pages.views import (
    HomePageView,
    AboutUs,
    FaqsView,
    TermsAndConditionsView,
    DisclamerView,
    OtpVerify,
    FeedBackFormView,
    SendHTMLMail,
    OtpReset,
    ContactFormView,
    PrivacyPolicy,
    PartnerWithUsView,
    VerifyOtpView,
    RequestNewOtpView,
    robots_txt,
    send_otp
)


urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", HomePageView.as_view(), name="index"),
    path("best-mobile-laptop-repair-siliguri/privacy-policy", PrivacyPolicy.as_view(), name="privacy_policy"),
    path("email-verification/", OtpVerify.as_view(), name="otp_verify"),
    path("otp-resend/", OtpReset, name="otp_reset"),
    path("best-mobile-laptop-repair-siliguri/about/", AboutUs.as_view(), name="aboutus"),
    path("contact/", ContactFormView.as_view(), name="contactus"),
    path("best-mobile-laptop-repair-siliguri/feedback/", FeedBackFormView.as_view(), name="feedback"),
    path("best-mobile-laptop-repair-siliguri/faqs/", FaqsView.as_view(), name="faqs"),
    path("best-mobile-laptop-repair-siliguri/disclamer/", DisclamerView.as_view(), name="disclaimer"),
    path('best-mobile-laptop-repair-siliguri/partner-with-us/', PartnerWithUsView.as_view(), name='partner_with_us'),

    path('send-otp/', send_otp, name='send_otp'),
    path('email-verify-otp/', VerifyOtpView.as_view(), name='verify_email'),
    path('request-new-otp/', RequestNewOtpView.as_view(), name='request_new_otp'),
    path("best-mobile-laptop-repair-siliguri-/terms-conditions/", TermsAndConditionsView.as_view(),
        name="terms_and_conditions",
    ),  # new
]
