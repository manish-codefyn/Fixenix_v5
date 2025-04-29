from django.contrib import admin
from .models import DoorstepService

@admin.register(DoorstepService)
class DoorstepServiceAdmin(admin.ModelAdmin):
    list_display = (
        'service_name', 'is_available', 'is_premium', 'is_discountable', 'is_featured',
        'price', 'offer_price', 'rating', 'review_count', 'updated_at'
    )
    list_filter = ('is_available', 'is_premium', 'is_discountable', 'is_featured')
    search_fields = ('service_name',)
