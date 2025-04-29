
from sitesetting.models import Sites, AboutCompany
from . import app_settings


from django.views.generic import CreateView, ListView, DetailView, UpdateView,TemplateView,View
from django.urls import reverse_lazy
from .models import DoorstepService
from .forms import DoorstepServiceForm
import json
from django.shortcuts import redirect
from django.contrib import messages


class DesktopRepairServicesView(TemplateView):
    """
   laptop
    """
    template_name = "services/desktop-repair.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Laptop Repair in siliguri - all types of mobile,lalptop repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/desktop-repair-og-image.jpg"),
            "description": "best laptop Repair in siliguri - all types of mobile,laptop repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
            "telephone": "+91-7992351609",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Check Post",
                "addressLocality": "Siliguri",
                "addressRegion": "West Bengal",
                "postalCode": "734001",
                "addressCountry": "IN"
            },
            "openingHours": "Mo-Sa 09:00-20:00",
            "sameAs": [
                "https://www.facebook.com/Fixenix.mobile/",
                "https://www.youtube.com/@FixenixMobileservices",
                "https://www.instagram.com/fixenix.official/",
         
            ]
        }

        # Pass Schema.org data as JSON string
        context['schema_org_data'] = json.dumps(schema_data, indent=4)     
        
        # Open Graph meta tags
        context['og_title'] = "Best desktop repair  Services in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/desktop-repair-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best desktop repair Services in Siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class LaptopRepairServicesView(TemplateView):
    """
   laptop
    """
    template_name = "services/laptop-repair.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Laptop Repair in siliguri - all types of mobile,lalptop repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/laptop-repair-og-image.jpg"),
            "description": "best laptop Repair in siliguri - all types of mobile,laptop repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
            "telephone": "+91-7992351609",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Check Post",
                "addressLocality": "Siliguri",
                "addressRegion": "West Bengal",
                "postalCode": "734001",
                "addressCountry": "IN"
            },
            "openingHours": "Mo-Sa 09:00-20:00",
            "sameAs": [
                "https://www.facebook.com/Fixenix.mobile/",
                "https://www.youtube.com/@FixenixMobileservices",
                "https://www.instagram.com/fixenix.official/",
         
            ]
        }

        # Pass Schema.org data as JSON string
        context['schema_org_data'] = json.dumps(schema_data, indent=4)     
        
        # Open Graph meta tags
        context['og_title'] = "Best laptop Repair Services in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/laptop-repair-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best laptop Repair Services in Siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class SmartphoneRepairServicesView(TemplateView):
    """
   smart phone
    """
    template_name = "services/smartphone.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/android-repair-og-image.jpg"),
            "description": "best Iphone Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
            "telephone": "+91-7992351609",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Check Post",
                "addressLocality": "Siliguri",
                "addressRegion": "West Bengal",
                "postalCode": "734001",
                "addressCountry": "IN"
            },
            "openingHours": "Mo-Sa 09:00-20:00",
            "sameAs": [
                "https://www.facebook.com/Fixenix.mobile/",
                "https://www.youtube.com/@FixenixMobileservices",
                "https://www.instagram.com/fixenix.official/",
         
            ]
        }

        # Pass Schema.org data as JSON string
        context['schema_org_data'] = json.dumps(schema_data, indent=4)     
        
        # Open Graph meta tags
        context['og_title'] = "Best Android-Smartphone Repair Services in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/android-repair-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Android-Smartphone Repair Services in Siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class IphoneRepairServicesView(TemplateView):
    """
    Iphone Repair
    """
    template_name = "services/iphone_repair.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/iphone-repair-og-image.jpg"),
            "description": "best Iphone Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
            "telephone": "+91-7992351609",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Check Post",
                "addressLocality": "Siliguri",
                "addressRegion": "West Bengal",
                "postalCode": "734001",
                "addressCountry": "IN"
            },
            "openingHours": "Mo-Sa 09:00-20:00",
            "sameAs": [
                "https://www.facebook.com/Fixenix.mobile/",
                "https://www.youtube.com/@FixenixMobileservices",
                "https://www.instagram.com/fixenix.official/",
         
            ]
        }

        # Pass Schema.org data as JSON string
        context['schema_org_data'] = json.dumps(schema_data, indent=4)     
        
        # Open Graph meta tags
        context['og_title'] = "Iphone - Best Iphone Repair Services in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/iphone-repair-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Iphone Repair Services in Siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"



class DoorstepServiceCreateView(CreateView):
    model = DoorstepService
    form_class = DoorstepServiceForm
    template_name = "services/service_form.html"
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        # Ensure the user is authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user  # Assign the logged-in user
            return super().form_valid(form)
        else:
            # Redirect to login if the user is not authenticated
            messages.error(self.request, "You need to be logged in to submit a service request.")
            return redirect('login')  # Adjust to your login URL name


# List all services for a user
class DoorstepServiceListView(ListView):
    model = DoorstepService
    template_name = "services/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        # Fetch all services
        services = super().get_queryset()
        
        # Calculate the discount percentage for each service
        for service in services:
            if service.offer_price:
                discount_percentage = ((service.price - service.offer_price) / service.price) * 100
                service.discount_percentage = round(discount_percentage, 1)  # Round to 1 decimal place
            else:
                service.discount_percentage = 0  # No discount if no offer price

        return services
    

class DoorstepServiceDetailView(DetailView):
    model = DoorstepService
    template_name = "services/service_detail.html"
    context_object_name = "service"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object  # The DoorstepService instance
        
        # Parse features into a list
        context["features"] = service.features.split("\n") if service.features else []
        
        # Calculate discount percentage if an offer price is available
        if service.offer_price:
            discount_percentage = ((service.price - service.offer_price) / service.price) * 100
            context["discount_percentage"] = round(discount_percentage, 1)  # Rounded to 1 decimal place
        else:
            context["discount_percentage"] = 0  # No discount if no offer price
        
        return context

# Update service request status (for staff/admins)
class DoorstepServiceUpdateView(UpdateView):
    model = DoorstepService
    fields = ['status']
    template_name = "services/service_update.html"
    success_url = reverse_lazy('service-list')



class DataRecoveryServices(TemplateView):
    """To View Computer And Laptop Services"""

    template_name = "services/data_recovery." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "Date Recovery",
    }


class ElectronicsServices(TemplateView):
    """To View Computer And Laptop Services"""

    template_name = "services/electronics." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "Electronics",
    }


class HardwareUpdateServices(TemplateView):
    """To View Computer And Laptop Services"""

    template_name = "services/hardware_update." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "Hardware Update",
    }


class CctvServices(TemplateView):
    """To View Computer And Laptop Services"""

    template_name = "services/cctv." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "CCTV",
    }


class ComputerLaptopServices(TemplateView):
    """To View Computer And Laptop Services"""
    template_name = "services/computer_services." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "Computer & Laptop",
    }


class MobileAndTabServices(TemplateView):

    """To View Mobile And Tab Services"""

    template_name = "services/mobile_services." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": "Mobile & Tab",
    }


