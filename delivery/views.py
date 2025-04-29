from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from .models import Delivery
from .forms import DeliveryLocationForm

class DeliveryListView(View):
    """List all deliveries."""
    def get(self, request):
        deliveries = Delivery.objects.all()
        return render(request, "delivery/delivery_list.html", {"deliveries": deliveries})


class UpdateDeliveryLocationView(View):
    """Update delivery location."""
    def get(self, request, delivery_id):
        delivery = get_object_or_404(Delivery, id=delivery_id)
        form = DeliveryLocationForm()
        return render(request, "delivery/update_location_form.html", {"form": form, "delivery": delivery})

    def post(self, request, delivery_id):
        delivery = get_object_or_404(Delivery, id=delivery_id)
        form = DeliveryLocationForm(request.POST)
        if form.is_valid():
            delivery.current_location_lat = form.cleaned_data["current_location_lat"]
            delivery.current_location_lon = form.cleaned_data["current_location_lon"]
            delivery.status = "in_progress"
            delivery.save()
            return JsonResponse({"status": "success", "message": "Location updated."})
        return JsonResponse({"status": "error", "message": "Invalid form data."})
