from django import forms
from .models import Booking, Review,RepairService,Device, DeviceModel, DeviceProblem,DeviceBrand

from captcha.fields import CaptchaField, CaptchaTextInput


CITY_CHOICES = [
    ('MALL', 'Mallguri'),
    ('BET', 'Betgara'),
    ('DAB', 'Dabgram'),
    ('FUL', 'Fulbari'),
    ('NAY', 'Nayapara'),
    ('NJP', 'New Jalpaiguri'),
    ('CHA', 'Champasari'),
    ('SAM', 'Samar Nagar'),
    ('DEV', 'Devi Danga'),
    ('SUK', 'Sukna'),
]


class RepairServiceForm(forms.ModelForm):
    class Meta:
        model = RepairService
        fields = [
            'device', 'device_brand','device_model', 'device_problem', 
            'customer_name', 'email', 'mobile', 'city',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer Email',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer Mobile',
            }),
            'city': forms.Select(choices=CITY_CHOICES, attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate city choices dynamically

        # Device-related queryset logic (unchanged)
        self.fields['device'].queryset = Device.objects.none()
        self.fields['device_brand'].queryset = DeviceBrand.objects.all()
        self.fields['device_model'].queryset = DeviceModel.objects.none()
        self.fields['device_problem'].queryset = DeviceProblem.objects.none()

        if 'device' in self.data:
            try:
               device_id = self.data.get('device')  # Get device ID from the request data
               self.fields['device'].queryset = Device.objects.filter(id=device_id)  # Use 'id' instead of 'device_id'
            except (ValueError, TypeError):
               pass

        if 'device_brand' in self.data:
            try:
                brand_id = self.data.get('device_brand')
                self.fields['device_model'].queryset = DeviceModel.objects.filter(device_brand_id=brand_id)
            except (ValueError, TypeError):
                pass

        if 'device_model' in self.data:
            try:
                model_id = self.data.get('device_model')
                self.fields['device_problem'].queryset = DeviceProblem.objects.filter(device_model_id=model_id)
            except (ValueError, TypeError):
                pass



class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6, 
        label="Enter OTP", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter the 6-digit OTP'})
    )



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'address', 'service', 'distance']

    # Optional: Custom widget for distance field (range slider)
    distance = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 1}),
        initial=1
    )
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']