from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from geopy.distance import geodesic  # Install using `pip install geopy`
import requests
import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('custom')

from datetime import datetime, timedelta


from django.utils.timezone import now

from employee.tasks import update_employee_location




def geocode_address(address):
    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": "AIzaSyDqWK4wUDODyPrHq1A89oFToiGHu1Uvbvo"
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return 0.0, 0.0  # Fallback values





# @receiver(post_save, sender=Booking)
# def create_delivery_for_booking(sender, instance, created, **kwargs):
#     if created:  # Only create a Delivery for new bookings
#         Delivery.objects.create(
#             booking=instance,
#             current_location_lat=0.0,  # Initial placeholder for employee's location
#             current_location_lon=0.0,
#             delivery_location_lat=instance.distance,  # Using Booking's distance for delivery lat (adjust based on your logic)
#             delivery_location_lon=0.0,  # Placeholder, update if you have a specific value
#             status="pending"  # Initial status
#         )
