from django.contrib import admin
from .models import  Booking, Payment,DeviceBrand,Device, DeviceModel, DeviceProblem,RepairService



@admin.register(RepairService)
class RepairServiceAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name', 
        'email', 
        'mobile', 
        'city', 
        'device', 
        'device_brand', 
        'device_model', 
        'device_problem', 
        'otp_verified', 
        'created_at',
    )
    list_filter = ('city', 'device_brand', 'otp_verified', 'created_at')
    search_fields = ('customer_name', 'email', 'mobile', 'device__name', 'device_problem__description')
    ordering = ('-created_at',)  # Show the newest entries first
    readonly_fields = ('created_at',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DeviceBrand)
class DeviceBrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ("name", "device_brand")
    list_filter = ("device_brand",)
    search_fields = ("name", "device__name")

@admin.register(DeviceProblem)
class DeviceProblemAdmin(admin.ModelAdmin):
    list_display = ("description", "device_model")
    list_filter = ("device_model",)
    search_fields = ("description", "device__name")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'booking_id','customer_email', 'customer_phone', 'service', 'distance', 'status',"assigned_employee", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("service__name", "user__username")
    autocomplete_fields = ("user", "assigned_employee")
    date_hierarchy = "created_at"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "razorpay_order_id", "payment_status", "amount_paid", "created_at")
    list_filter = ("payment_status", "created_at")
    search_fields = ("razorpay_order_id", "booking__id")
    date_hierarchy = "created_at"
