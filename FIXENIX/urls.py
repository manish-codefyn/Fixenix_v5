"""FIXENIX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # new
from django.conf import settings  # new
from django.conf.urls.static import static  # new

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Login Required for Admin Section Login
from django.contrib.auth.decorators import login_required

# OTP FOR AUTH
from django.contrib.auth.models import User
from pages.models import EstimateRequests, ContactUs, FeedBack
from works.models import WorkSheet
from sitesetting.models import (
    Sites,
    Brands,

    Faq,
    AboutCompany,

)
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

# Debug


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name="OTPAdmin")
admin_site.register(User)
admin_site.register(EstimateRequests)
admin_site.register(ContactUs)
admin_site.register(FeedBack)
admin_site.register(WorkSheet)
admin_site.register(Brands)
admin_site.register(Faq)
admin_site.register(Sites)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)


admin_site.login = login_required(
    admin_site.login
)  # for login requred for admin section


admin.site.site_header = "Fixenix Admin"
admin.site.site_title = "Fixenix Admin Portal"
admin.site.index_title = "Welcome to Fixenix"
urlpatterns = [
    # path("ilovepy-062742-codefyn/", admin.site.urls),
    path("admin/", admin.site.urls),
    # path("secure/admin/dont/", admin_site.urls),
    # usermanage
    # localapp
    path("", include("delivery.urls")),
    path('captcha/', include('captcha.urls')),
    path("", include("services.urls")),
    path("accounts/", include("allauth.urls")),  # new
    path('accounts/', include('allauth.socialaccount.urls')),
    path("", include("users.urls")),  # new
    path("", include("pages.urls")),
    path("", include("sitesetting.urls")),
    path("works/", include("works.urls")),
    path("", include("Invoice.urls")),
    path("", include("bookings.urls")),
    path("", include("chatbot.urls")),
    # path('', include('employee.urls')),
    path('', include('dashboard.urls')),  # Directly include dashboard URLs
    # path('captcha/', include('captcha.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # new
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
