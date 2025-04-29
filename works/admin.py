from django.contrib import admin
from .models import WorkSheet, DeviceChecklist

class DeviceChecklistInline(admin.TabularInline):
    model = DeviceChecklist
    extra = 1  # Number of empty rows to display

class WorkSheetAdmin(admin.ModelAdmin):
    inlines = [DeviceChecklistInline]
    list_display = [ 'work_id','name','email','mobile','device_name','device_problem','status', 'created_at']  # Customize based on your WorkSheet fields
    search_fields = ['name']

admin.site.register(WorkSheet, WorkSheetAdmin)

@admin.register(DeviceChecklist)
class DeviceChecklistAdmin(admin.ModelAdmin):
    list_display = ['worksheet', 'component_name', 'is_working']
    list_filter = ['component_name', 'is_working']
    search_fields = ['worksheet__customer_name', 'component_name']


