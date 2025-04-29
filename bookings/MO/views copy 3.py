

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Payment,Review
from services.models import DoorstepService
from pages.models import Sites
import razorpay
from django.shortcuts import render

from .forms import BookingForm
from datetime import datetime
from django.utils import timezone
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from io import BytesIO
import os
from django.core.mail import BadHeaderError
import logging
from django.core.mail import send_mail
from django.http import HttpResponse

from django.views.generic import DetailView, CreateView, ListView, UpdateView,View,FormView,TemplateView

logger = logging.getLogger(__name__)
logger = logging.getLogger('custom')

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hmac
import hashlib
import random
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.urls import reverse_lazy
from django.conf import settings


from .forms import BookingForm,ReviewForm,RepairServiceForm, OTPVerificationForm
import razorpay
from decimal import Decimal
# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

from datetime import datetime, timedelta
from django.core.signing import Signer, BadSignature

from django.utils.timezone import now

from django.core.signing import Signer

import random
from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
from django.utils.dateparse import parse_datetime
from .forms import RepairServiceForm, OTPVerificationForm
from .models import DoorstepService, Booking, Payment,RepairService,DeviceModel, DeviceProblem,Device,DeviceBrand
from django.http import JsonResponse


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import timedelta
from django.utils.timezone import now
from .forms import RepairServiceForm,RepairStatusForm
from .models import Device, DeviceBrand, DeviceModel, DeviceProblem, RepairService



class RepairStatusCheckView(FormView):
    template_name = 'bookings/check_repair_status.html'
    form_class = RepairStatusForm
    success_url = reverse_lazy('repair_status_check')  # Replace with your desired redirect URL or view name

    def form_valid(self, form):
        # Get the form data
        request_id = form.cleaned_data['request_id']
        email = form.cleaned_data['email']
        
        # Simulating repair status logic
        status = f"Repair status for request ID {request_id} is pending."
        
        # Pass the status to the context
        context = self.get_context_data(form=form, status=status)
        return self.render_to_response(context)
    
    def form_invalid(self, form):
        # If the form is invalid, just render it back with errors
        return self.render_to_response(self.get_context_data(form=form))


class RepairServiceView(View):
    template_name = 'bookings/repair_service_form.html'

    def get(self, request, *args, **kwargs):
        form = RepairServiceForm()
        devices = Device.objects.all()
        return render(request, self.template_name, {'form': form, 'devices': devices})

    def post(self, request, *args, **kwargs):
        form = RepairServiceForm(request.POST)

        if form.is_valid():
            repair_instance = form.save(commit=False)

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Save OTP and expiry in session
            request.session['otp'] = otp
            request.session['otp_expiry'] = (now() + timedelta(minutes=5)).isoformat()

            # Manually serialize the form data by saving only the IDs (primary keys) of the related fields
            form_data = {
                'device': str(form.cleaned_data['device'].id),  # Convert UUID to string
                'device_brand': str(form.cleaned_data['device_brand'].id),  # Convert UUID to string
                'device_model': str(form.cleaned_data['device_model'].id),  # Convert UUID to string
                'device_problem': str(form.cleaned_data['device_problem'].id),  # Convert UUID to string
                'device_others_problem': form.cleaned_data['device_others_problem'],
                'customer_name': form.cleaned_data['customer_name'],
                'email': form.cleaned_data['email'],
                'mobile': form.cleaned_data['mobile'],
                'city': form.cleaned_data['city']
            }
            request.session['form_data'] = form_data

            # Retrieve the corresponding instances from the database using UUIDs
            device_instance = Device.objects.get(id=form.cleaned_data['device'].id)
            device_brand_instance = DeviceBrand.objects.get(id=form.cleaned_data['device_brand'].id)
            device_model_instance = DeviceModel.objects.get(id=form.cleaned_data['device_model'].id)
            device_problem_instance = DeviceProblem.objects.get(id=form.cleaned_data['device_problem'].id)

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
                form.add_error(None, f"Failed to send OTP email. Please try again later. Error: {e}")
                return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})

            # Redirect to OTP verification page
            return redirect('verify_otp')  # Replace with actual URL name for OTP verification

        else:
            # If form is not valid, render the form again with errors
            return render(request, self.template_name, {'form': form, 'devices': Device.objects.all()})






def load_device_names(request):
    device_id = request.GET.get('device_id')  # Fetch the device_id from the query parameter

    if not device_id:
        return JsonResponse({"error": "Device ID is required."}, status=400)

    try:
        # Fetch device brands based on the device_id
        devices = DeviceBrand.objects.filter(device_id=device_id).values('id', 'name')
        return JsonResponse(list(devices), safe=False)
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
        # Render OTP verification form with context
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

            # Check OTP expiry
            if otp_expiry and now() > otp_expiry:
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('resend_otp')

            # Validate OTP
            if str(entered_otp) == str(session_otp):
                # Fetch form data from the session
                form_data = self.request.session.get('form_data')

                # Fetch the DeviceType, Device, DeviceModel, and DeviceProblem instances using the UUIDs
                device_id = form_data.get('device')
                device = Device.objects.get(id=device_id)

                device_brand_id = form_data.get('device_brand')
                device_brand = DeviceBrand.objects.get(id=device_brand_id)

                device_model_id = form_data.get('device_model')
                device_model = DeviceModel.objects.get(id=device_model_id)

                device_problem_id = form_data.get('device_problem')
                device_problem = DeviceProblem.objects.get(id=device_problem_id)  # Fetch DeviceProblem instance

                # Now, create the RepairService instance with the correct instances
                repair_service = RepairService(
                    device=device,  # Assign the actual DeviceType instance
                    device_brand=device_brand,  # Assign the actual Device instance
                    device_model=device_model,  # Assign the actual DeviceModel instance
                    device_problem=device_problem,  # Assign the actual DeviceProblem instance
                 
                    device_others_problem=form_data.get('device_others_problem'),
                    customer_name=form_data.get('customer_name'),
                    email=form_data.get('email'),
                    mobile=form_data.get('mobile'),
                    city=form_data.get('city'),
                    otp_verified=True
                )
                repair_service.save()

                # Clear session data
                self.request.session.pop('otp', None)
                self.request.session.pop('otp_expiry', None)
                self.request.session.pop('form_data', None)

                messages.success(request, "Booking successful!")
                return redirect('repair_success')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('verify_otp')
        
        # If form is not valid, render it again with errors
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
        return redirect('verify_otp')


        


class BookingSuccess(TemplateView):
    template_name = 'bookings/success.html'



class TrackBookingView(LoginRequiredMixin,View):
    template_name = 'bookings/track_booking.html'

    def get(self, request):
        booking_id = request.GET.get('booking_id')  # Retrieve booking ID from GET parameters
        context = {}

        if booking_id:  # Check if a booking ID is provided
            booking = get_object_or_404(Booking, booking_id=booking_id)
            context['booking'] = booking

        return render(request, self.template_name, context)
    

class BookingCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account_login")  # Redirect if user is not logged in

    def get(self, request, pk):  # Use `pk` to match the URL parameter
        service = get_object_or_404(DoorstepService, id=pk)
        form = BookingForm(initial={'service': service})
        return render(request, 'bookings/booking_form.html', {'service': service, 'form': form})

    def post(self, request, pk):  # Use `pk` to match the URL parameter
        service = get_object_or_404(DoorstepService, id=pk)
        form = BookingForm(request.POST)

        if form.is_valid():
            # Get form data
            customer_name = form.cleaned_data.get('customer_name')
            customer_email = form.cleaned_data.get('customer_email')
            customer_phone = form.cleaned_data.get('customer_phone')
            address = form.cleaned_data.get('address')
            distance = form.cleaned_data.get('distance')

            # Calculate price based on distance
            if distance <= 2:
                distance_price = Decimal('40.00')  # Rs. 40 for 2 km or less
            else:
                distance_price = Decimal('40.00') + (Decimal(distance) - Decimal('2.00')) * Decimal('20.00')  # Rs. 20 for each km beyond 2 km

            # Calculate total price: Base service price + distance price
            total_price = service.price + distance_price

            # Create a new booking instance
            booking = Booking.objects.create(
                service=service,
                user=request.user,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                address=address,
                distance=distance,
                price=total_price,  # Set the total price (service price + distance price)
            )

            # Create Razorpay order
            order_data = {
                "amount": int(total_price * 100),  # Convert to paise
                "currency": "INR",
                "receipt": str(booking.id),
            }
            razorpay_order = razorpay_client.order.create(order_data)

            # Save payment history
            Payment.objects.create(
                booking=booking,
                razorpay_order_id=razorpay_order["id"],
                amount_paid=total_price,
            )

            # Prepare context for payment page
            context = {
                'booking': booking,
                'order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': total_price,  # Display price in INR
                'service_price': service.price,  # Display price in INR
                'distance_price': distance_price,  # Display price in INR
            }
            return render(request, 'bookings/payment.html', context)

        # If form is invalid, re-render the form with errors
        return render(request, 'bookings/booking_form.html', {'service': service, 'form': form})



    
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

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(View):
    def post(self, request):
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        try:
            # Fetch the Payment instance
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

            # Verify the signature
            generated_signature = hmac.new(
                settings.RAZORPAY_SECRET_KEY.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature == razorpay_signature:
                # Mark payment as completed and save
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.paid = True
                payment.save()
                
                # Mark booking as completed
                payment.booking.payment_completed = True
                payment.booking.save()

                # Generate and email the invoice
                self.generate_and_email_invoice(payment)

                # Render the success page
                context = {
                'amount': payment.amount_paid
                }
               
                return render(request, 'bookings/payment_success.html',context)
            else:
                # Signature mismatch; handle as needed
                return redirect('service-list')
        
        except Payment.DoesNotExist:
            # Payment not found; handle as needed
            return redirect('service-list')

    def generate_invoice(self, payment):
        """Generate PDF invoice using xhtml2pdf."""
        template_path = 'invoice/invoice.html'
        context = {
            'payment': payment,
            'booking': payment.booking,
            'data': Sites.objects.all(),
       
           
        }
        pdf_name = f"Invoice for your Booking #{payment.booking.id}.pdf"
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
        with open(pdf_name, "wb+") as output:
            pdf = pisa.pisaDocument(
               BytesIO(html.encode("UTF-8")), output, link_callback=fetch_resources
        )
        return output.name

    def send_invoice_email(self, payment, invoice_pdf):
        """Send the generated invoice via email."""
        email_subject = f"Invoice for your Booking #{payment.booking.id}"
        email_body = f"Dear {payment.booking.user.get_full_name()},\n\nPlease find your booking invoice attached."
        recipient_email = payment.booking.user.email
        copy_email = settings.ADMIN_EMAIL  # Replace with the email to send a copy to

        email = EmailMultiAlternatives(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
        bcc=[copy_email],  # Add a copy recipient here
    )
        email.attach_alternative( email_body, "text/html")
        email.attach_file(invoice_pdf)
        # email.attach(f"invoice_{payment.booking.id}.pdf", invoice_pdf, 'application/pdf')

        return email.send()


    def generate_and_email_invoice(self, payment):
        """Generate invoice and send it via email."""
        invoice_pdf = self.generate_invoice(payment)
        if invoice_pdf:
            self.send_invoice_email(payment, invoice_pdf)

    def get(self, request):
        # Optionally handle GET requests
        return render(request, 'booking/payment_success.html')
    
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