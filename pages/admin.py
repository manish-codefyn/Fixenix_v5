from django.contrib import admin
from .models import FeedBack, ContactUs, EstimateRequests,PartnerApplication


@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name', 'phone', 'interest_reason', 'created_at')
    search_fields = ('name', 'email', 'company_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    # Optional: Customize form fields display on the admin page
    fields = ('name', 'email', 'phone', 'company_name', 'interest_reason')

    # Optional: Display error messages in the admin panel when saving the model
    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('email', 'rating')
    search_fields = ('email', 'rating')
    ordering = ('email',)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(EstimateRequests)
class EstimateRequestsAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'device_name', 'created_at')
    search_fields = ('name', 'mobile', 'email', 'device_name', 'device_problem')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

