from django import forms
from .models import Booking, Review,RepairService,Device, DeviceModel, DeviceProblem,DeviceBrand
from captcha.fields import CaptchaField, CaptchaTextInput


class BookingTrackForm(forms.Form):
    booking_id = forms.CharField(
        label="Booking ID",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Booking ID',
            'id': 'bookingId',
            'required': True
        })
    )

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

    ('MALL','Mallaguri'),
    ('BET', 'Betgara'),
    ('DAB', 'Dabgram'),
    ('FUL', 'Fulbari'),
    ('NAY', 'Nayapara'),
    ('NJP', 'New Jalpaiguri'),
    ('CHA', 'Champasari'),
    ('SAM', 'Samar Nagar'),
    ('DEV', 'Devi Danga'),
    ('SUK', 'Sukna'),
    ('PRD', 'Pradhannagar'),
    ('CHK', 'Checkpost'),
    ('BAG', 'Bagdogra'),
    ('MAT', 'Matigara'),
    ('SAL', 'Salugara'),
    ('PUN', 'Purnea More'),
    ('ISM', 'Iskcon Mandir Area'),
    ('SEV', 'Sevoke Road'),
    ('KAN', 'Kannyamore'),
    ('ASH', 'Ashighar'),
    ('MIL', 'Milan More'),
    ('BYP', 'Bypass More'),
    ('KAD', 'Kadamtala'),
    ('KHAP', 'Khaprail'),
    ('RAN', 'Rangapani'),
    ('IND', 'Indira Nagar'),
    ('MED', 'Medical More'),
    ('HIM', 'Himalaya More'),
    ('PAT', 'Patiram Jote'),
    ('ANA', 'Anandamoyee'),
    ('SUB', 'Subashpally'),
    ('DES', 'Deshbandhu Para'),
    ('VIN', 'Vivekananda Nagar'),
    ('SHE', 'Shibmandir'),
    ('JOT', 'Jotiakhali'),
    ('PAB', 'Pabna Colony'),
    ('SUR', 'Surya Sen Colony'),
    ('EHI', 'Eastern Housing'),
    ('AGP', 'Agrasen Road'),
    ('APS', 'Apurba Sen Road'),
    ('AIR', 'Airview More'),
    ('BAN', 'Bani Nagar'),
    ('BHA', 'Bhanunagar'),
    ('SHA', 'Shantinagar'),
    ('SAR', 'Saratpally'),
    ('TSR', 'T.S. Road'),
    ('KAL', 'Kalimandir'),
    ('RAB', 'Rabindra Nagar'),
    ('MON', 'Montivilla'),
    ('LAL', 'Lalkothi'),
    ('RNG', 'Rangapani Bazar'),
    ('BEL', 'Beltala More'),
    ('NRT', 'North Bharat Nagar'),
    ('RBT', 'Rabindra Pally'),
    ('SCP', 'Sankarpur'),
    ('NTP', 'Nimtala Para'),
    ('BAR', 'Baramasia'),
    ('HAL', 'Halal Market'),
    ('KUL', 'Kuleshwari'),
    ('KHO', 'Khoribari'),
    ('NAX', 'Naxalbari'),
    ('PHU', 'Phulbari Gate'),
    ('BARB', 'Bara Pathuram Jote'),
    ('BIR', 'Birpara'),
    ('TUK', 'Tukvar'),
    ('NEU', 'Neulgaon'),
    ('DUR', 'Durga Nagar'),
    ('BHAI', 'Bhairavnath Colony'),
    ('RAM', 'Ramkrishna Pally'),
    ('BAGH', 'Baghajatin Colony'),
    ('DEO', 'Deonagar'),
     ('BAI', 'Baikunthapur Forest'),
    ('GHO', 'Ghospukur'),
    ('BAT', 'Batasi'),
    ('JAT', 'Jatashankar'),
    ('KAM', 'Kamtapur'),
    ('GAY', 'Gayerkata More'),
    ('MEG', 'Meghnath Saha Nagar'),
    ('SAF', 'Safdar Ali Colony'),
    ('NAYM', 'Nayabasti'),
    ('GOL', 'Gole Market'),
    ('UDA', 'Uttarayon Township'),
    ('SHI', 'Shibmandir More'),
    ('BHAT', 'Bhaktinagar'),
    ('BID', 'Bidhan Market'),
    ('SAI', 'Sainikpuri'),
    ('GUR', 'Gurung Basti'),
    ('JAM', 'Jamidari More'),
    ('BHUT', 'Bhutki'),
    ('BAH', 'Bahundangi Border'),
    ('SHAK', 'Shaktigarh'),
    ('DAI', 'Daikyajote'),
    ('MILK', 'Milk Colony'),
    ('HEL', 'Helapakur'),
    ('CHH', 'Chhota Sevoke'),
    ('KALC', 'Kalimandir Colony'),
    ('PAK', 'Pakurtala'),
    ('TARA', 'Tarabandha'),
    ('KHO2', 'Kholachand Fari'),
    ('PRA', 'Pranami Mandir Area'),
    ('CHIN', 'Chinese Line'),
    ('NEWC', 'New Checkpost'),
    ('NAL', 'Nalpukuria'),
    ('TEN', 'Tenzing Norgay Area'),
    ('SHUK', 'Shuklajote'),
    ('DOM', 'Domohani'),
    ('TEL', 'Telipara'),
    ('BOL', 'Bol Bagan'),
    ('RAI', 'Railgate'),
    ('LOK', 'Loknath Colony'),
    ('GOD', 'Godhuli Bazar'),
    ('KAK', 'Kakarvitta Border'),
    ('NEO', 'Neotia Getwel Hospital Area'),
    ('TUR', 'Turingia More'),
    ('CHAP', 'Chapatoli'),
    ('BUD', 'Buddha Park'),
    ('GOS', 'Gosain Basti'),
    ('JOR', 'Jorpokhri'),
    ('JAN', 'Janata Nagar'),
    ('ABH', 'Abhay Nagar'),
    ('BHAK', 'Bhaktinagar Checkpost'),
    ('AIRV', 'Airview Complex'),
    ('NOK', 'Nokshalbari'),
    ('CHIT', 'Chitrey'),
    ('BIJ', 'Bijoy Nagar'),
     ('MAT', 'Matigara'),
    ('KUR', 'Kurseong Junction'),
    ('SAL', 'Salugara'),
    ('BAG', 'Bagdogra Bazar'),
    ('HAN', 'Hansqua'),
    ('CHUN', 'Chunabhatti'),
    ('IND', 'Indira Nagar'),
    ('SHA', 'Shantipara'),
    ('TEA', 'Tea Garden Area'),
    ('ASH', 'Ashighar'),
    ('JHO', 'Jhorabari'),
    ('LAL', 'Laltong Gaon'),
    ('BHATG', 'Bhatgaon'),
    ('RUP', 'Rupnarayanpur'),
    ('FULP', 'Fulbari Power Plant'),
    ('SEV', 'Sevoke Forest'),
    ('MUN', 'Mungpoo Road'),
    ('RAN', 'Rangapani'),
    ('TIL', 'Tilabari'),
    ('PHU', 'Phulbari More'),
    ('MOT', 'Motidhar'),
    ('GOS2', 'Gossaipur'),
    ('MIR', 'Mirik Road'),
    ('DHU', 'Dhupguri More'),
    ('GHO2', 'Ghogomali'),
    ('RAB', 'Rabindra Nagar'),
    ('MON', 'Montivilla Area'),
    ('BAR', 'Bariakhop'),
    ('MUNP', 'Munshipara'),
    ('ROH', 'Rohini Road'),
    ('BAS', 'Basugaon'),
    ('GAR', 'Garidhura'),
    ('JAI', 'Jaitak'),
    ('NAN', 'Nandokgaon'),
    ('FAR', 'Farabari'),
    ('MIRK', 'Mirik Tea Garden'),
    ('PAT', 'Patiram Jote'),
    ('BAIJ', 'Baijonathpur'),
    ('BIN', 'Binnaguri Road'),
    ('SIT', 'Sitong'),
    ('DUM', 'Dumriguri'),
    ('NEWM', 'New Market Siliguri'),
    ('MAHA', 'Mahakal Mandir Area'),
    ('ROYA', 'Royal Residency Area'),
    ('CHIR', 'Chiranjivi Nagar'),
    ('RAM', 'Ramkrishna Colony'),
    ('PANI', 'Panighatta'),
    ('CHEN', 'Chenga Khal'),
    ('PAL', 'Palpara'),
    ('NEHR', 'Nehru Road'),
    ('MED', 'Medical More'),
    ('NIVA', 'Nivedita Road Area'),
    ('OTH', 'Others')
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


class BookingForm(forms.ModelForm):
    calculated_distance = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'readonly': 'readonly',
            'id': 'calculated_distance',
            'placeholder': 'Distance will be calculated automatically',
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
            'id': 'id_service',
            'placeholder': 'Selected service name',
        }),
        required=False,
        label="Service"
    )
    customer_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Enter your full name',
        }),
        label="Name"
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Enter your email address',
        }),
        label="Email"
    )
    customer_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Enter your phone number',
        }),
        label="Phone"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control shadow-sm',
            'rows': 3,
            'placeholder': 'Enter your address',
        }),
        label="Address"
    )


    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email','customer_phone', 'address', 'calculated_distance', 'distance_value', 'service_name']


    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']