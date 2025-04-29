

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from services.models import DoorstepService
from sitesetting.models import Sites
from django.utils import timezone
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from io import BytesIO
import qrcode
import base64
from django.core.files.base import ContentFile
from PIL import Image
import os
from django.core.mail import BadHeaderError
import logging
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseForbidden
from django.views.generic import DetailView, CreateView, ListView, UpdateView,View,FormView,TemplateView

logger = logging.getLogger(__name__)
logger = logging.getLogger('custom')

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hmac
import hashlib
from django.urls import reverse_lazy,reverse
from django.conf import settings
import razorpay
from decimal import Decimal, InvalidOperation
# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

from datetime import datetime, timedelta
from django.core.signing import Signer, BadSignature

from django.utils.timezone import now

from django.core.signing import Signer

import random
from datetime import timedelta
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib import messages

from django.utils.dateparse import parse_datetime
from .forms import RepairServiceForm, OTPVerificationForm,RepairStatusForm,BookingForm,ReviewForm,RepairServiceForm, OTPVerificationForm,BookingTrackForm
from .models import ( DoorstepService, Booking, Payment,RepairService,Review,
                     Device, DeviceBrand, DeviceModel, DeviceProblem)
from django.http import JsonResponse

import requests
import json
from geopy.distance import geodesic  # Install using `pip install geopy`
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class BookingSuccessView(TemplateView):
    template_name = "bookings/service_booking_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Sample booking details (replace with actual logic)
        context["booking_id"] = self.request.GET.get("booking_id", "UNKNOWN")
        context["customer_name"] = self.request.GET.get("customer_name", "Guest")
        context["service_name"] = self.request.GET.get("service_name", "Service")
        context["amount_paid"] = self.request.GET.get("amount_paid", "0.00")
        context["redirect_url"] = reverse("service-list")  # Change to the appropriate URL name

        return context
    

class TrackBookingView(View):
    template_name = 'bookings/track_booking.html'

    def get(self, request):
        # Instantiate an empty form for GET requests
        form = BookingTrackForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Bind form with POST data
        form = BookingTrackForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            booking_id = form.cleaned_data['booking_id']
            try:
                # Fetch the booking by ID
                booking = Booking.objects.get(booking_id=booking_id)
                context['booking'] = booking  # Add booking to context
                context['status'] = booking.status  # Add booking status to context

                # Add success message with status
                success_message = (
                    f"Booking ID {booking_id} found successfully. "
                    f"Status: {booking.status}."
                )
                messages.success(request, success_message)
            except Booking.DoesNotExist:
                # Add error message if booking is not found
                error_message = f"No booking found with ID {booking_id}."
                messages.error(request, error_message)
                context['error'] = error_message
        else:
            # Add error message for invalid form input
            error_message = "Please enter a valid booking ID."
            messages.error(request, error_message)
            context['error'] = error_message

        # Render the template with the context
        return render(request, self.template_name, context)



    
class TrackingServiceView(TemplateView):
    template_name = "bookings/services_tracking.html"

class CalculateDistanceView(View):
    def post(self, request):
        try:
            # Parse request body
            body = json.loads(request.body)
            user_lat = body.get('user_lat')
            user_lng = body.get('user_lng')

            # Validate coordinates
            if not user_lat or not user_lng:
                return JsonResponse({"error": "Invalid coordinates provided."}, status=400)

            try:
                # Convert coordinates to floats
                user_location = (float(user_lat), float(user_lng))
            except ValueError:
                return JsonResponse({"error": "Coordinates must be valid numbers."}, status=400)

            # Fixed service location (latitude, longitude)
            service_location = (26.747917, 88.437392)  # Replace with actual service location

            # Calculate distance
            distance = geodesic(service_location, user_location).kilometers

            # Return the distance rounded to two decimal places
            return JsonResponse({"distance": round(distance, 2)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)



class BookingCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account_login")  # Redirect if user is not logged in

    def get(self, request, pk):
        # Retrieve the service and initialize the form
        service = get_object_or_404(DoorstepService, id=pk)
        form = BookingForm(initial={'service_name': service.service_name})
        return render(request, 'bookings/booking_form.html', {'service': service, 'form': form})


    def post(self, request, pk):
        # Retrieve the service and process the form
        service = get_object_or_404(DoorstepService, id=pk)
        form = BookingForm(request.POST)

        if form.is_valid():
            customer_name = form.cleaned_data.get('customer_name')
            customer_email = form.cleaned_data.get('customer_email')
            customer_phone = form.cleaned_data.get('customer_phone')
            address = form.cleaned_data.get('address')
            distance_value = request.POST.get('calculated_distance')  # Retrieve distance from frontend
            latitude = request.POST.get('latitude')  # Retrieve distance from frontend
            longitude = request.POST.get('longitude')  # Retrieve distance from frontend
               
            if not distance_value:
                logger.error("Distance value missing from POST data.")
                return JsonResponse({'error': 'Unable to calculate distance. Please enable location.'}, status=400)

            try:
                distance = Decimal(distance_value)  # Convert distance to Decimal
            except (ValueError, InvalidOperation) as e:
                logger.error(f"Invalid distance value: {distance_value} - Error: {e}")
                return JsonResponse({'error': 'Invalid distance value provided.'}, status=400)

            # Calculate price based on distance
            if distance <= 2:
                distance_price = Decimal('40.00')  # Rs. 40 for 2 km or less
            else:
                distance_price = Decimal('40.00') + (distance - Decimal('2.00')) * Decimal('20.00')  # Rs. 20 per km beyond 2 km

            # Calculate total price: Base service price + distance price
            # Check for offer price
            service_price = service.offer_price if service.offer_price else service.price

            # Calculate total price
            total_price = service_price + distance_price

            # Create booking instance
            booking = Booking.objects.create(
                service=service,
                user=request.user,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                address=address,
                distance=distance,
                price=total_price,
            )

            try:
                # Create Razorpay order
                order_data = {
                    "amount": int(total_price * 100),  # Convert to paise
                    "currency": "INR",
                    "receipt": str(booking.id),
                }
                razorpay_order = razorpay_client.order.create(order_data)
            except Exception as e:
                logger.error(f"Razorpay order creation failed: {e}")
                return JsonResponse({'error': 'Failed to process payment. Please try again later.'}, status=500)

            # Save payment history
            Payment.objects.create(
                booking=booking,
                razorpay_order_id=razorpay_order["id"],
                amount_paid=total_price,
            )

            # Prepare context for rendering payment page
            context = {
                'booking': booking,
                'order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': total_price,
                'service_price': service_price,
                'distance_price': distance_price,
            }
            return render(request, 'bookings/payment.html', context)

        logger.error("Booking form validation failed.")
        return render(request, 'bookings/booking_form.html', {'service': service, 'form': form})
 

class CheckRepairStatusView(View):
    template_name = "bookings/check_repair_status.html"


    def get(self, request):
        form = RepairStatusForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RepairStatusForm(request.POST)
        status = None

        if form.is_valid():
            # Get data from the validated form
            request_id = form.cleaned_data['request_id']
            email = form.cleaned_data['email']

            # Fetch Repair Service record
            try:
                repair_service = RepairService.objects.get(request_id=request_id, email=email)
                status = f"Repair status for request ID {request_id} is {repair_service.status} ."
            except RepairService.DoesNotExist:
                status = "Invalid Request ID or Email. Please check your details."
        else:
            # Print form errors in the server log for debugging
            print(form.errors)  # This will print errors in the server log

            status = "There was an error with the form. Please check your input."

        return render(request, self.template_name, {'form': form, 'status': status})


class RepairServiceView(View):
    template_name = 'bookings/repair_service_form.html'

    def get(self, request, *args, **kwargs):
        form = RepairServiceForm()
        devices = Device.objects.all()
        return render(request, self.template_name, {'form': form, 'devices': devices})

    def post(self, request, *args, **kwargs):
        form = RepairServiceForm(request.POST)

        if form.is_valid():
            try:
                repair_instance = form.save(commit=False)

                # Generate OTP
                otp = random.randint(100000, 999999)

                # Save OTP and expiry in session
                request.session['otp'] = otp
                request.session['otp_expiry'] = (now() + timedelta(minutes=5)).isoformat()

                # Serialize form data and save it in session
                form_data = {
                    'device': str(form.cleaned_data['device'].id),
                    'device_brand': str(form.cleaned_data['device_brand'].id),
                    'device_model': str(form.cleaned_data['device_model'].id),
                    'device_problem': str(form.cleaned_data['device_problem'].id),
                    'device_others_problem': form.cleaned_data['device_others_problem'],
                    'customer_name': form.cleaned_data['customer_name'],
                    'email': form.cleaned_data['email'],
                    'mobile': form.cleaned_data['mobile'],
                    'city': form.cleaned_data['city'],
                }
                request.session['form_data'] = form_data

                # Retrieve the corresponding instances from the database
                try:
                    device_instance = Device.objects.get(id=form.cleaned_data['device'].id)
                    device_brand_instance = DeviceBrand.objects.get(id=form.cleaned_data['device_brand'].id)
                    device_model_instance = DeviceModel.objects.get(id=form.cleaned_data['device_model'].id)
                    device_problem_instance = DeviceProblem.objects.get(id=form.cleaned_data['device_problem'].id)
                except (Device.DoesNotExist, DeviceBrand.DoesNotExist, DeviceModel.DoesNotExist, DeviceProblem.DoesNotExist) as e:
                    messages.error(request, f"Error retrieving device information: {e}")
                    return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})

                # Assign the instances to the repair_instance
                repair_instance.device_name = device_instance
                repair_instance.device_brand = device_brand_instance
                repair_instance.device_model = device_model_instance
                repair_instance.device_problem = device_problem_instance
                repair_instance.otp_verified = False  # Default to False

                # Save the repair instance
                repair_instance.save()

                # Send OTP email
                try:
                    send_mail(
                        subject="Verify Your Email - Repair Service",
                        message=f"Your OTP is {otp}. It is valid for 5 minutes.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[form.cleaned_data['email']],
                    )
                except Exception as e:
                    messages.error(request, f"Failed to send OTP email. Please try again later. Error: {e}")
                    return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})

                # Redirect to OTP verification page
                return redirect('rep-otp-verify')  # Replace with actual URL name for OTP verification

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})
        else:
            # Add form errors to messages
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")

            # Render the form again with error messages
            return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})


def load_device_names(request):
    device_id = request.GET.get('device_id')  # Fetch the device_id from the query parameter

    if not device_id:
        return JsonResponse({"error": "Device ID is required."}, status=400)

    try:
        # Fetch the device based on device_id (Device model)
        device = Device.objects.get(id=device_id)

        # Fetch device brands based on the device_type (related to the Device model)
        device_brands = DeviceBrand.objects.filter(device_type=device).values('id', 'name')

        return JsonResponse(list(device_brands), safe=False)
    except Device.DoesNotExist:
        return JsonResponse({"error": "Device not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Function to load device models based on device
def load_device_models(request):
    brand_id = request.GET.get('brand_id')  # Fetch the DeviceBrand ID from the query parameter
    
    if not brand_id:
        return JsonResponse({"error": "Brand ID is required."}, status=400)
    
    try:
        # Filter models by DeviceBrand ID
        models = DeviceModel.objects.filter(device_brand__id=brand_id).values('id', 'name')
        return JsonResponse(list(models), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Function to load device problems based on device model
def load_device_problems(request):
    model_id = request.GET.get('model_id')  # Fetch the DeviceModel ID from the query parameter
    
    if not model_id:
        return JsonResponse({"error": "Model ID is required."}, status=400)
    
    try:
        # Filter problems by DeviceModel ID
        problems = DeviceProblem.objects.filter(device_model__id=model_id).values('id', 'description')
        return JsonResponse(list(problems), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



class VerifyOTPView(View):
    template_name = 'bookings/verify_otp.html'

    def get(self, request, *args, **kwargs):
        form = OTPVerificationForm()
        context = {
            'form': form,
            'otp_expiry': self.request.session.get('otp_expiry', now().isoformat())
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = self.request.session.get('otp')
            otp_expiry = parse_datetime(self.request.session.get('otp_expiry'))

            if otp_expiry and now() > otp_expiry:
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('resend_otp')

            if str(entered_otp) == str(session_otp):
                # Fetch form data from the session
                form_data = self.request.session.get('form_data')

                # Fetch DeviceType, Device, DeviceModel, and DeviceProblem instances
                device = Device.objects.get(id=form_data.get('device'))
                device_brand = DeviceBrand.objects.get(id=form_data.get('device_brand'))
                device_model = DeviceModel.objects.get(id=form_data.get('device_model'))
                device_problem = DeviceProblem.objects.get(id=form_data.get('device_problem'))

                # Create RepairService instance
                repair_service = RepairService(
                    device=device,
                    device_brand=device_brand,
                    device_model=device_model,
                    device_problem=device_problem,
                    device_others_problem=form_data.get('device_others_problem'),
                    customer_name=form_data.get('customer_name'),
                    email=form_data.get('email'),
                    mobile=form_data.get('mobile'),
                    city=form_data.get('city'),
                    otp_verified=True
                )
                repair_service.save()

                # Send email with request ID to user
                context = {
                    'customer_name': form_data.get('customer_name'),
                    'request_id': repair_service.request_id,
                    'company_name': 'Fixenix',  # Replace with your company name
                    'company_contact': '+917992351609',  # Replace with your contact number
                    'company_website': 'https://fixenix.com/',  # Replace with your website URL
                    'terms_conditions_link': 'https://fixenix.com/terms-conditions/'  # Replace with your terms & conditions link
                }

                subject = f'Your Repair Request ID - {repair_service.request_id}'
                message = render_to_string('emails/repair_status_update.html', context)
                from_email = settings.DEFAULT_FROM_EMAIL

                send_mail(
                    subject, 
                    message, 
                    from_email, 
                    [form_data.get('email')], 
                    html_message=message
                )

                # Clear session data
                self.request.session.pop('otp', None)
                self.request.session.pop('otp_expiry', None)
                self.request.session.pop('form_data', None)

                messages.success(request, "Booking successful! A confirmation email has been sent.")
                return redirect('repair_success')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('rep-otp-verify')

        return render(request, self.template_name, {'form': form})


class ResendOTPView(FormView):
    def get(self, request, *args, **kwargs):
        form_data = request.session.get('form_data')

        if not form_data:
            messages.error(request, "Session expired. Please start the process again.")
            return redirect('book_repair')

        # Generate a new OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['otp_expiry'] = (now() + timedelta(minutes=5)).isoformat()

        # Resend OTP email
        send_mail(
            subject="Your New OTP - Repair Service",
            message=f"Your new OTP is {otp}. It is valid for 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form_data['email']],
        )

        messages.success(request, "A new OTP has been sent to your email.")
        return redirect('rep-otp-verify')


class BookingSuccess(TemplateView):
    template_name = 'bookings/success.html'


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def RenderToPDF(template_src, context_dict={}, pdf_name={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    with open(pdf_name, "wb+") as output:
        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")), output, link_callback=fetch_resources
        )
    return output.name

@method_decorator(csrf_exempt, name="dispatch")
class PaymentSuccessView(View):
    def post(self, request):
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        try:
            # Fetch the Payment instance
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

            # Verify the signature
            generated_signature = hmac.new(
                settings.RAZORPAY_SECRET_KEY.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256,
            ).hexdigest()

            if generated_signature == razorpay_signature:
                # Mark payment as successful
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.payment_status = "paid"
                payment.save()

                # Mark booking as completed
                payment.booking.payment_completed = True
                payment.booking.save()

                # Generate and email the invoice
                self.generate_and_email_invoice(payment)

                context = {
                    "amount": payment.amount_paid,
                    "redirect_url": reverse_lazy("booking-success"),
                    }
                return render(request, "bookings/payment_success.html", context)
            else:
                # Mark payment as failed
                payment.payment_status = "failed"
                payment.save()
                return redirect("service-list")

        except Payment.DoesNotExist:
            # Payment not found; handle as needed
            return redirect("service-list")

    def generate_invoice(self, payment):
        """Generate PDF invoice using xhtml2pdf."""
        # Generate QR Code Data
        qr_data = {
            "booking_id": payment.booking.booking_id,
            "customer_name": payment.booking.customer_name,
            "amount_paid": str(payment.amount_paid),
            "payment_id": payment.razorpay_payment_id,
        }
        qr_code = self.generate_qr_code(qr_data)
        template_path = 'invoice/invoice.html'
        context = {
        "qr_code": qr_code,  # Add QR code image to the context
        'company_name': 'Fixenix',  # Replace with your company name
        'company_mobile': '+917992351609',  # Replace with your contact number
        'company_website': 'https://fixenix.com/',  # Replace with your website URL
        'company_email': 'info@fixenix.com',  # Replace with your website URL
        'company_address': 'Ward No-43,Prakash Nagar, Siliguri,West Bengal-734001',  # Replace with your website URL
        'payment': payment,
        'booking': payment.booking,
        'data': Sites.objects.all(),
        'customer_name': payment.booking.customer_name,
        'customer_email': payment.booking.customer_email,
        'customer_phone': payment.booking.customer_email,
        'booking_id': payment.booking.booking_id,
        'service_name': payment.booking.service.service_name,
        'address': payment.booking.address,
        'distance': payment.booking.distance,
        'price': payment.booking.price,
        'date': payment.booking.created_at,
        'payment_status': payment.payment_status,
        'amount_paid': payment.amount_paid,
        'payment_id': payment.razorpay_payment_id,
        'logo_url': self.request.build_absolute_uri(settings.STATIC_URL + 'codefyn-5.0/images/logo.png'),  # Absolute URL for logo
        'stamp_url': self.request.build_absolute_uri(settings.STATIC_URL + 'codefyn-5.0/images/fixsign.png'),  # Absolute URL for logo
        }

        template = get_template(template_path)
        html = template.render(context)

        # Create a PDF in memory
        pdf_buffer = BytesIO()
        pdf = pisa.CreatePDF(html, dest=pdf_buffer)
        if not pdf.err:
            pdf_buffer.seek(0)
            return pdf_buffer
        return None

    def generate_qr_code(self, data):
        """Generate a QR code as a base64 image string."""
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")  # Ensure PNG format
        buffer.seek(0)  # Reset buffer position

        # Encode the image as base64
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    def send_invoice_email(self, payment, invoice_pdf):
        """Send the generated invoice via email with a modern HTML template."""
        subject = f"New Booking Confirmed: {payment.booking.booking_id}"

       # Render the HTML template with the necessary context
        context = {
        'customer_name': payment.booking.customer_name,
        'booking_id': payment.booking.booking_id,
        'service_name': payment.booking.service.service_name,
        'address': payment.booking.address,
        'distance': payment.booking.distance,
        'price': payment.booking.price,
         }
        html_message = render_to_string('emails/invoice_email.html', context)

        recipient_email = payment.booking.customer_email
        copy_email = settings.ADMIN_EMAIL  # Replace with the email to send a copy to

        email = EmailMultiAlternatives(
        subject=subject,
        body="Please find your booking invoice attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
        bcc=[copy_email],  # Add a copy recipient here
    )
        email.attach_alternative(html_message, "text/html")

        # Attach the PDF as a file attachment
        email.attach(f"Invoice_{payment.booking.booking_id}.pdf", invoice_pdf.getvalue(), "application/pdf")
        invoice_pdf.close()  # Close the buffer after use

        return email.send()


    def generate_and_email_invoice(self, payment):
        """Generate invoice and send it via email."""
        invoice_pdf = self.generate_invoice(payment)
        if invoice_pdf:
            self.send_invoice_email(payment, invoice_pdf)


    def get(self, request):
        # Optionally handle GET requests
        return render(request, 'bookings/success.html')
    
# class BookingCreateView(LoginRequiredMixin, CreateView):
#     model = Booking
#     fields = []  # Form fields can be omitted as we'll handle data in the `form_valid` method
#     template_name = "bookings/booking_form.html"


#     def form_valid(self, form):
#         # Retrieve the service based on the primary key in the URL
#         service = DoorstepService.objects.get(id=self.kwargs["pk"])
#         user = self.request.user  # Get the currently logged-in user

#         # Create a new Booking object
#         booking = Booking.objects.create(service=service, user=user)

#         # Create Razorpay Order
#         order_data = {
#             "amount": int(service.price * 100),  # Convert to paise
#             "currency": "INR",
#             "receipt": str(booking.id),
#         }
#         razorpay_order = razorpay_client.order.create(order_data)

#         # Save Payment History
#         PaymentHistory.objects.create(
#             booking=booking,
#             razorpay_order_id=razorpay_order["id"],
#             amount_paid=service.price,
#         )

#         # Redirect to the payment page
#         return redirect("payment_page", pk=booking.id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["service"] = DoorstepService.objects.get(id=self.kwargs["pk"])
#         return context





class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ["completion_status", "assigned_employee"]
    template_name = "services/booking_update.html"
    success_url = reverse_lazy("booking_list")



class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'add_review.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the booking object
        self.booking = get_object_or_404(Booking, id=self.kwargs['booking_id'])

        # Check if the booking already has a review
        if hasattr(self.booking, 'review'):
            return HttpResponseForbidden("You have already reviewed this booking.")
        
        # Ensure the user is the owner of the booking
        if self.booking.user != request.user:
            return HttpResponseForbidden("You can only review your own bookings.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Assign the booking to the review before saving
        form.instance.booking = self.booking
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a success page (e.g., booking detail)
        return reverse_lazy('booking_detail', kwargs={'pk': self.booking.id})