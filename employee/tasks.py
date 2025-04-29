from celery import shared_task
from .models import Employee



@shared_task
def update_employee_location(employee_id, lat, lon):
    """Update the employee's location."""
    try:
        employee = Employee.objects.get(id=employee_id)
        employee.current_location_lat = lat
        employee.current_location_lon = lon
        employee.save()
    except Employee.DoesNotExist:
        pass  # Log error



@shared_task
def trace_employee_and_update_delivery(delivery_id):
    """Trace the assigned employee's location and update the delivery."""
    from .models import Delivery

    try:
        delivery = Delivery.objects.get(id=delivery_id)
        employee = delivery.booking.assigned_employee

        if employee:
            delivery.current_location_lat = employee.current_location_lat
            delivery.current_location_lon = employee.current_location_lon
            delivery.save()
    except Delivery.DoesNotExist:
        pass  # Log error