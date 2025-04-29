from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booking',
        'employee_name',
        'status',
        'estimated_delivery_time',
        'timestamp',
    )
    list_filter = ('status', 'timestamp', 'estimated_delivery_time')
    search_fields = ('id', 'employee_name__name', 'booking__id')  # Assuming Employee has a 'name' field
    ordering = ('-timestamp',)
    readonly_fields = ('id', 'timestamp')  # Mark fields as read-only if needed
    fieldsets = (
        (None, {
            'fields': ('id', 'booking', 'employee_name', 'status')
        }),
        ('Delivery Details', {
            'fields': ('current_location_lat', 'current_location_lon', 'delivery_location_lat', 'delivery_location_lon')
        }),
        ('Timestamps', {
            'fields': ('estimated_delivery_time', 'timestamp')
        }),
    )
