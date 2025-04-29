from django.urls import path
from .views import DeliveryListView, UpdateDeliveryLocationView

urlpatterns = [
    path("delivery/", DeliveryListView.as_view(), name="delivery_list"),
    path("update-location/<uuid:delivery_id>/", UpdateDeliveryLocationView.as_view(), name="update_delivery_location"),
]
