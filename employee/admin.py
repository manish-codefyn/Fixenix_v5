from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "employee_id", 
        "email", 
        "phone", 
        "designation", 
        "department", 
        "experience", 
        "salary", 
        "created_at"
    )
    list_filter = ("designation", "department", "experience", "created_at")
    search_fields = ("name", "email", "phone", "employee_id")
    ordering = ("-created_at",)
    readonly_fields = ("employee_id", "created_at")

    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "email", "phone", "address", "photo", "id_proof")
        }),
        ("Job Details", {
            "fields": ("designation", "department", "experience", "salary", "employee_id")
        }),
        ("Location", {
            "fields": ("current_location_lat", "current_location_lon")
        }),
        ("System Information", {
            "fields": ("created_at",)
        }),
    )
