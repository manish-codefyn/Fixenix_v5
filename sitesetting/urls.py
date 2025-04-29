from django.urls import path

from users.views import SignupPageView, UserAccountView

urlpatterns = [
   
    path("accounts/profile/", UserAccountView.as_view(), name="user-profile"),
    # staff sliders
]
