from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_no', 'customer_name', 'email', 'mobile',
        'invoice_date', 'due_date', 'total_amount', 'payment_status'
    )
    list_filter = ('invoice_date', 'payment_status',)
    search_fields = ('invoice_no', 'customer_name', 'email', 'mobile')
    readonly_fields = ('invoice_no', 'created_at', 'updated_at')
    ordering = ('-invoice_date',)
    fieldsets = (
        (None, {
            'fields': (
                'invoice_no', 'customer_name', 'email', 'mobile', 'address',
                'invoice_date', 'due_date', 'payment_status'
            )
        }),
        ('Products & Financials', {
            'fields': (
                'product_details', 'subtotal', 'tax_amount',
                'discount_amount', 'total_amount'
            )
        }),
        ('Notes & Metadata', {
            'fields': ('notes', 'terms', 'created_at', 'updated_at')
        }),
    )
