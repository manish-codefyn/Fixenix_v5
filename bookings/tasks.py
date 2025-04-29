from celery import shared_task
from .models import Delivery

@shared_task
def update_delivery_location(delivery_id, lat, lon):
    try:
        delivery = Delivery.objects.get(id=delivery_id)
        delivery.current_location_lat = lat
        delivery.current_location_lon = lon
        delivery.save()
    except Delivery.DoesNotExist:
        pass
