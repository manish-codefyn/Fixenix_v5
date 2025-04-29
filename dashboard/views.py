# dashboard/views.py
from django.views.generic import TemplateView
from bookings.models import Booking, Payment,Review,RepairService # Import your models
from employee.models import Employee
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from works.models import WorkSheet
from Invoice.models import Invoice
from sitesetting.models import Brands,Sites
from delivery.models import Delivery
from users.models import CustomUser
from pages.models import ContactUs,FeedBack

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the necessary statistics
        total_employees = Employee.objects.count()
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        completed_bookings = Booking.objects.filter(status='completed').count()

        # Payment statistics
        total_payments = Payment.objects.count()
        total_revenue = Payment.objects.filter(payment_status='paid').aggregate(total_revenue=Sum('amount_paid'))['total_revenue'] or 0.00
        pending_payments = Payment.objects.filter(payment_status='pending').count()
        failed_payments = Payment.objects.filter(payment_status='failed').count()

        # Additional statistics
        total_users = CustomUser.objects.count()
        total_works = WorkSheet.objects.count()
        total_invoices = Invoice.objects.count()
        total_brands = Brands.objects.count()
        total_feedback = FeedBack.objects.count()
        total_messages =ContactUs.objects.count()
        total_repairings = RepairService.objects.count()
        total_pending_repairings = RepairService.objects.filter(status='pending').count()
        total_completed_repairings = RepairService.objects.filter(status='completed').count()
        total_pending_works = WorkSheet.objects.filter(status='pending').count()
        total_completed_works = WorkSheet.objects.filter(status='completed').count()
        total_delivery_pending = Delivery.objects.filter(status='pending').count()

        # Add these values to context
        context['total_employees'] = total_employees
        context['total_bookings'] = total_bookings
        context['pending_bookings'] = pending_bookings
        context['completed_bookings'] = completed_bookings
        context['total_payments'] = total_payments
        context['total_revenue'] = total_revenue
        context['pending_payments'] = pending_payments
        context['failed_payments'] = failed_payments

        # Additional data
        context['total_users'] = total_users
        context['total_works'] = total_works
        context['total_invoices'] = total_invoices
        context['total_brands'] = total_brands
        context['total_feedback'] = total_feedback
        context['total_messages'] = total_messages
        context['total_repairings'] = total_repairings
        context['total_pending_repairings'] = total_pending_repairings
        context['total_completed_repairings'] = total_completed_repairings
        context['total_pending_works'] = total_pending_works
        context['total_completed_works'] = total_completed_works
        context['total_delivery_pending'] = total_delivery_pending
        context['app_data'] = Sites.objects.all

        return context



