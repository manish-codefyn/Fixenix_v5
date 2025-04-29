# time
from django.utils import timezone
import datetime
# revers and redirect
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# validation
from django.core.exceptions import ValidationError
# random number
import random
# requests
# settingd imports
from django.conf import settings
from . import app_setting
# mail
from django.core.mail import EmailMultiAlternatives  # form html send
from django.core.mail import send_mail
# template rendering
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# jason response
from django.http import JsonResponse
# appp imports views
from django.views.generic import TemplateView, CreateView, View, FormView, ListView,FormView
from django.views.generic.detail import SingleObjectMixin

from sitesetting.models import (
    Sites,
    Faq,
    AboutCompany,
  
)
# app import models
from .models import EstimateRequests, ContactUs, FeedBack,PartnerApplication
# app imoprt forms
from .form import EstimateRequestForm, ContactForm, FeedBackForm, OtpVerifyForm,PartnerApplicationForm,OTPForm
import json
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponse
import logging
from django.http import HttpResponseRedirect, JsonResponse

logger = logging.getLogger(__name__)

class FeedBackFormView(FormView):
    template_name = "pages/feedback." + app_setting.TEMPLATE_EXTENSION
    form_class = FeedBackForm
    PAGE_TITLE = "Feedback | Fixenix - Best Mobile Repair Services"
    extra_context = {"page_title": PAGE_TITLE}

    def get_success_url(self):
        return reverse("feedback")

    def form_valid(self, form):
        """
        Process valid form submission: save data, send confirmation email, and return response.
        """
        try:
            feedback = form.save(commit=True)  # Save feedback entry
            
            # Get email from form data
            email = form.cleaned_data["email"]
            
            # Prepare context for email
            context = {
                "title": "Feedback Received",
                "content": "Thank you for your valuable feedback!",
                "user_email": email,
                "feedback_message": form.cleaned_data.get("message", ""),
                "rating": form.cleaned_data.get("rating", ""),
                "date_submitted": feedback.created_at.strftime("%d %B, %Y") if hasattr(feedback, "created_at") else "",
            }
            
            # Send confirmation email
            from_mail = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
            template_name = "emails/feedback_confirmation." + app_setting.TEMPLATE_EXTENSION
            subject = "Thank you for Your Feedback!"
            
            try:
                SendHTMLMail(subject, context, template_name, email, from_mail)
                logger.info(f"Feedback confirmation email sent to {email}")
            except Exception as e:
                logger.error(f"Failed to send email to {email}: {str(e)}", exc_info=True)

            # Add a success message
            messages.success(self.request, "Thank you for your feedback! We appreciate your response.")

            # Check if request is AJAX
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "message": "Thank you for your feedback!",
                    "email": email
                }, status=200)

            return HttpResponseRedirect(self.get_success_url())

        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}", exc_info=True)

            # Add an error message
            messages.error(self.request, "An error occurred while submitting your feedback. Please try again.")

            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "An error occurred while processing your feedback."
                }, status=500)

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Handle invalid form submission and return JSON errors.
        """
        errors = {field: error[0] for field, error in form.errors.items()}
        logger.warning(f"Invalid feedback form submission. Errors: {errors}")
        messages.error(self.request, "An error occurred while submitting your feedback. Please try again.")
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": errors
            }, status=400)

        # If not AJAX, re-render the form with errors
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

    


def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Allow: /
Sitemap: https://example.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")



class PartnerWithUsView(FormView):
    template_name = 'pages/partner_with_us.html'
    form_class = PartnerApplicationForm

    def form_valid(self, form):
        # Save form data in session
        session_data = form.cleaned_data
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        otp_time = timezone.now().isoformat()  # Store ISO format time


        # Store form data and OTP in session
        self.request.session['partner_form_data'] = json.dumps(session_data)  # Store as JSON string
        self.request.session['otp'] = otp
        self.request.session['otp_time'] = otp_time
        # Send OTP to the email
        send_mail(
            'Your OTP for Email Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [session_data['email']],
            fail_silently=False,
        )

        # Redirect to OTP verification page
        return redirect('verify_email')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                # Business details for Schema markup
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/partner-og-image.png"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        # Open Graph meta tags
        context['og_title'] = "Partner With Us - Fixenix"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/partner-og-image.png")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Join Fixenix as a partner! Get expert support and expand your business with our network."

        return context
    
class RequestNewOtpView(View):
    def get(self, request):
        otp = random.randint(100000, 999999)
        otp_time = timezone.now().isoformat()  # Store ISO format time

        # Update session data
        request.session['otp'] = otp
        request.session['otp_time'] = otp_time

        # Ensure partner_form_data is retrieved correctly
        partner_form_data = request.session.get('partner_form_data', '{}')
        try:
            if isinstance(partner_form_data, str):
                partner_form_data = json.loads(partner_form_data)  # Parse JSON string
        except json.JSONDecodeError:
            partner_form_data = {}  # Reset on error

        email = partner_form_data.get('email')
        if email:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. It will expire in 5 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

        messages.success(request, 'A new OTP has been sent to your email address.')
        return redirect('verify_email')

class VerifyOtpView(View):
    def get(self, request):
        otp_time_str = request.session.get('otp_time')
        if otp_time_str:
            try:
                otp_time = timezone.datetime.fromisoformat(otp_time_str).replace(tzinfo=timezone.utc)
                if now() > otp_time + timedelta(minutes=5):  # Check if OTP is expired
                    request.session.pop('otp', None)
                    request.session.pop('otp_time', None)
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('request_new_otp')
            except Exception as e:
                request.session.pop('otp', None)
                request.session.pop('otp_time', None)
                messages.error(request, 'Invalid OTP session data. Please request a new one.')
                return redirect('request_new_otp')

        form = OTPForm()
        return render(request, 'pages/verify_otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)

        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_data = request.session.get('partner_form_data')

            if session_data:
                try:
                    if isinstance(session_data, str):
                        session_data = json.loads(session_data)

                    stored_otp = request.session.get('otp')
                    if entered_otp == str(stored_otp):
                        # Save form data to the database
                        new_application = PartnerApplication.objects.create(
                            name=session_data.get('name'),
                            email=session_data.get('email'),
                            phone=session_data.get('phone'),
                            company_name=session_data.get('company_name'),
                            message=session_data.get('message'),
                        )

                        # Prepare email content
                        subject = "Application Received - Fixenix"
                        message = f"Dear {new_application.name},\n\nThank you for applying to partner with us. We have received your application:\n\n" \
                                  f"Name: {new_application.name}\n" \
                                  f"Email: {new_application.email}\n" \
                                  f"Phone: {new_application.phone}\n" \
                                  f"Company Name: {new_application.company_name}\n" \
                                  f"Message: {new_application.message}\n\n" \
                                  f"We will get back to you soon.\n\nRegards,\nFixenix Team"
                        recipient_email = new_application.email
                        sender_email = settings.DEFAULT_FROM_EMAIL

                        # Include admin email in the recipient list
                        recipient_list = [recipient_email]
                        admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                        if admin_email:
                            recipient_list.append(admin_email)

                        # Send email
                        send_mail(subject, message, sender_email, recipient_list)

                        # Clear session data after successful submission
                        request.session.pop('partner_form_data', None)
                        request.session.pop('otp', None)
                        request.session.pop('otp_time', None)

                        messages.success(request, 'Your OTP is verified, and your application has been submitted!')
                        return redirect('partner_with_us')
                    else:
                        messages.error(request, 'Invalid OTP. Please try again.')
                except Exception as e:
                    print(f"Error processing session data: {e}")
                    request.session.pop('partner_form_data', None)
                    request.session.pop('otp', None)
                    request.session.pop('otp_time', None)
                    messages.error(request, 'An error occurred. Please fill out the form again.')
            else:
                messages.error(request, 'Session data is missing. Please fill the form again.')

        return render(request, 'pages/verify_otp.html', {'form': form})

        

class HomePageView(SuccessMessageMixin, View):
    """HomePage View"""

    template_name = "pages/index." + app_setting.TEMPLATE_EXTENSION
    model = EstimateRequests
    form_class = EstimateRequestForm
    import random

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
            "form": form,
            'title': 'Welcome to Fixenix - Best Mobile Repair in Siliguri',
            'description': 'Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!',
            },
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
       
                               # Business details for Schema markup
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/home-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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

        context['og_title'] = "Welcome to Fixenix - Best Mobile Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/home-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"

        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, to_mail):
        messages.success(self.request, f"Otp Has Sent to Your Email {to_mail}")
        return reverse("otp_verify")

    def form_valid(self, form):
        """if from data is valid"""

        if self.request.method == "POST":
            if form.is_valid():
                n = form.cleaned_data["name"]
                e = form.cleaned_data["email"]
                m = form.cleaned_data["mobile"]
                d = form.cleaned_data["device_name"]
                p = form.cleaned_data["device_problem"]
                self.request.session["name"] = n
                self.request.session["email"] = e
                self.request.session["mobile"] = m
                self.request.session["device_name"] = d
                self.request.session["device_problem"] = p
                from_mail = settings.EMAIL_HOST_USER
                to_mail = e
                # otp = otp_generate()
                otp = randomDigits(4)
                expiry = get_expiry()
                self.request.session["otp"] = otp
                self.request.session["time"] = str(expiry)
                template_name = "emails/emails." + app_setting.TEMPLATE_EXTENSION
                subject = "OTP for Final Submit"
                context = {
                    "title": "Email Verification Code",
                    "content": f"your OTP is {otp} .Dont share with anyone",
                }

                SendHTMLMail(subject, context, template_name, to_mail, from_mail)
                # self.request.session.set_expiry(100)
                return HttpResponseRedirect(self.get_success_url(to_mail))

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """

        errors = form.errors
        context = {
            "form": form,
            'title': 'Welcome to Fixenix - Best Mobile Repair in Siliguri',
            'keywords': 'Best mobile repairing in Siliguri, Mobile repair services Siliguri, Laptop repair Siliguri, Desktop repair Siliguri, CCTV installation Siliguri',
            'description': 'Fixenix offers the best mobile repairing services in Siliguri. We provide expert solutions for mobile, laptop, desktop, tablet, CCTV, and more. Trust us for quality repairs and reliable service.',
        }
        for error in errors:
            messages.error(self.request, f"Please Check {error}-& Try Again")
            return render(self.request, self.template_name, context)


def OtpReset(request):
    otp = randomDigits(4)
    expiry = get_expiry()
    request.session["otp"] = otp
    request.session["time"] = str(expiry)
    from_mail = settings.EMAIL_HOST_USER
    to_mail = request.session["email"]
    template_name = "emails/emails." + app_setting.TEMPLATE_EXTENSION
    subject = "OTP for Final Submit"
    context = {
        "title": "OTP For Email Varifiaction",
        "content": f"your OTP is {otp} .Dont share with anyone",
    }
    SendHTMLMail(subject, context, template_name, to_mail, from_mail)
    message = f"OTP  has Send to Your {to_mail}"
    messages.success(request, message)
    return HttpResponseRedirect(reverse_lazy("otp_verify"))


class OtpVerify(View):
    form_class = OtpVerifyForm
    template_name = "pages/otpverify." + app_setting.TEMPLATE_EXTENSION
    model = EstimateRequests

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        """otp submit"""
        a = form.cleaned_data["otp1"]
        b = form.cleaned_data["otp2"]
        c = form.cleaned_data["otp3"]
        d = form.cleaned_data["otp4"]
        list = [a, b, c, d]
        s = [str(i) for i in list]
        u_otp = int("".join(s))
        otp = self.request.session.get("otp")
        name = self.request.session["name"]
        mobile = self.request.session.get("mobile")
        device_name = self.request.session.get("device_name")
        device_problem = self.request.session.get("device_problem")
        email_address = self.request.session.get("email")
        expriry = self.request.session.get("time")
        _now = str(timezone.now())
        if int(otp) == int(u_otp) and (_now < expriry):
            EstimateRequests.objects.create(
                name=name,
                mobile=mobile,
                email=email_address,
                device_name=device_name,
                device_problem=device_problem,
            )
            from_mail = settings.EMAIL_HOST_USER
            to_mail = app_setting.EMAIL_CC
            template_name = "emails/jobsheet." + app_setting.TEMPLATE_EXTENSION
            subject = "New Estimate Requests"
            context = {
                "title": "Estimate Requests ",
                "name": name,
                "mobile": mobile,
                "email": email_address,
                "device_name": device_name,
                "device_problem": device_problem,
                "date": datetime.datetime.now(),
            }
            SendHTMLMail(subject, context, template_name, to_mail, from_mail)
            self.request.session.delete("otp")
            self.request.session.delete("name")
            self.request.session.delete("email")
            self.request.session.delete("mobile")
            self.request.session.delete("device_name")
            self.request.session.delete("device_problem")
            messages.success(self.request, "Request Successfully Submited ! Thank You")
            return JsonResponse({"messages": "success"}, status=200)
        else:
            if _now > expriry:
                error = "Otp Expired ! Try Again"
                messages.error(self.request, error)
                return JsonResponse({"errors": error}, status=400)

            error = f"Please Put Valid OTP "
            messages.error(self.request, error)
            return JsonResponse({"errors": error}, status=400)

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """

        errors = form.errors
        for error in errors:
            return JsonResponse({"errors": error}, status=400)


class ContactFormView(View):
    template_name = "pages/contact." + app_setting.TEMPLATE_EXTENSION
    form_class = ContactForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contex = {
            "form_contact": form,
            "page_title": "Contact",
            "title": "Contact Us - Best Mobile - Laptop - computer Repair in Siliguri",
        }

        return render(request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Thank You For Writting Us !")
        return reverse("contactus")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile - Laptop - computer - cctv  Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        context['title'] = "Contact Us - Best Mobile - Laptop - computer - cctv Repair in Siliguri",
        # Business details for Schema markup
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/contact-og-image.jpg"),
            "description": "Best Mobile - Laptop - computer - cctv Repair in Siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['og_title'] = "Contact Us - Best Mobile - Laptop - computer - cctv Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/contact-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile - Laptop - computer - cctv Repair in Siliguri - all types of mobile , laptop , computer, cctv repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"

        return context
    
    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        form.save()
        from_mail = settings.EMAIL_HOST_USER
        to_mail = app_setting.EMAIL_CC
        template_name = "emails/message." + app_setting.TEMPLATE_EXTENSION
        subject = "New Online Message"
        context = {
            "title": "Message",
            "name": name,
            "email": email,
            "msg": message,
            "date": datetime.datetime.now(),
        }
        SendHTMLMail(subject, context, template_name, to_mail, from_mail)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """

        errors = form.errors
        context = {
            "form_contact": form,
            "page_title": "Contact  | Fixenix - Best Mobile Repair Services",
            "errors": errors,
        }
        for error in errors:
            messages.error(self.request, f"Please Check - {error} & Try Again ")
            return render(self.request, self.template_name, context)




class PrivacyPolicy(TemplateView):
    PAGE_TITLE = "Privay Policy |  Fixenix - Best Mobile Repair in Siliguri"
    template_name = "pages/privacy_policy." + app_setting.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
    
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/privacypolicy-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['og_title'] = "PrivacyPolicy- Best Mobile Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/privacypolicy-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class AboutUs(TemplateView):
    PAGE_TITLE = "Welcome to Fixenix - Best Mobile Repair in Siliguri"
    template_name = "pages/about." + app_setting.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": PAGE_TITLE,
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
    
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/images/aboutus-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!",
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
        context['og_title'] = "About Us- Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/aboutus-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!."


def SendMail(SenderMail, message, RecieverEmail):
    subject = (f"Thank You For Writting Us!",)
    message = message
    from_email = SenderMail
    recipient_list = [RecieverEmail]
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


def SendOtp(email, message, e):
    subject = ("Otp",)
    message = message
    from_email = email
    recipient_list = [e]
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


class DisclamerView(TemplateView):
    template_name = "pages/disclamer." + app_setting.TEMPLATE_EXTENSION
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/images/disclamer-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['og_title'] = "Disclamer- Best Mobile Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/disclamer-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class TermsAndConditionsView(TemplateView):
    """
    Terms And Conditions
    """

    template_name = "pages/terms_conditions." + app_setting.TEMPLATE_EXTENSION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/images/terms-conditions-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['og_title'] = "Disclamer- Best Mobile Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/terms-conditions-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


class FaqsView(ListView):
    """FAQs Views"""

    PAGE_TITLE = "FAQs | Fixenix - Best Mobile Repair in Siliguri"
    template_name = "pages/faqs." + app_setting.TEMPLATE_EXTENSION
    # paginate_by = 100  # if pagination is desired
    model = Faq
    context_object_name = "faq"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"
       
        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Fixenix",
            "url": self.request.build_absolute_uri(),
            "logo": self.request.build_absolute_uri("/static/codefyn-5.0/images/logo.png"),
            "image": self.request.build_absolute_uri("/static/codefyn-5.0/images/images/terms-conditions-og-image.jpg"),
            "description": "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!.",
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
        context['og_title'] = "Faq- Best Mobile Repair in Siliguri"
        context['og_type'] = "website"
        context['og_image'] = self.request.build_absolute_uri("/static/codefyn-5.0/images/terms-conditions-og-image.jpg")  # Generates full URL
        context['og_url'] = self.request.build_absolute_uri()
        context['og_url'] = self.request.build_absolute_uri()
        context['og_description'] = "Best Mobile Repair in siliguri - all types of mobile repair in Siliguri with Fixenix! We offer expert mobile screen replacement, battery replacement, motherboard repair, and more. Enroll in our professional mobile repairing courses and start your career today. Fast, reliable, and affordable service. Call Fixenix now!"


def SendHTMLMail(subject, context, template_name, to_mail, from_mail):
    """Html Send Through Email"""
    context = context
    subject = subject
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_mail, [to_mail])
    email.attach_alternative(html_content, "text/html")
    return email.send()


def randomDigits(digits):
    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    at = random.randint(lower, upper)
    return at


def get_expiry():
    now = timezone.now()
    expiry_seconds = 120
    expiry_time = timezone.timedelta(seconds=expiry_seconds)
    expiry = now + expiry_time
    return expiry
