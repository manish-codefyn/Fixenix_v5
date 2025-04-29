from django import forms
from .models import Booking, Review,RepairService,Device, DeviceModel, DeviceProblem,DeviceBrand

from captcha.fields import CaptchaField, CaptchaTextInput





class RepairStatusForm(forms.Form):
    request_id = forms.CharField(
        label='Request ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Please Enter Your like REQ-D2563',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Please Enter Your registered Email',
            'required': 'required'
        })
    )


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
    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Type Captcha",
                 "class": "form-control",
            }
        )
    )
    class Meta:
        model = RepairService
        fields = [
            'device', 'device_brand', 'device_model', 'device_problem', 
            'device_others_problem', 'customer_name', 'email', 'mobile', 'city',
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
            'device_others_problem': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the issue if not listed above',
                'rows': 3,
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

        # Additional handling: device-related problems (any issues with the selected device model)
        if 'device_problem' in self.data:
            try:
                device_problem_ids = self.data.getlist('device_problem')  # Get selected device problems
                self.fields['device_problem'].queryset = DeviceProblem.objects.filter(id__in=device_problem_ids)
            except (ValueError, TypeError):
                pass




class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6, 
        label="Enter OTP", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter the 6-digit OTP'})
    )



from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    calculated_distance = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'readonly': 'readonly',
            'id': 'calculated_distance'
        }),
        required=False,
        label="Distance",
        help_text="Automatically calculated based on your location."
    )
    distance_value = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'distance_value'}),
        required=False
    )
    service_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'readonly': 'readonly',
            'id': 'id_service'
        }),
        required=False,
        label="Service"
    )

    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'address', 'calculated_distance', 'distance_value', 'service_name']

    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']