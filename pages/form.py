from django.forms import ModelForm
from django import forms
from django.forms import TextInput, FileInput, EmailInput, Textarea, NumberInput
from .models import EstimateRequests, ContactUs, FeedBack,PartnerApplication
from django import forms
from captcha.fields import CaptchaField,CaptchaTextInput
import re
REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


class OTPForm(forms.Form):


    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-secondary rounded-3', 'placeholder': 'Enter OTP'}),
        label="Enter OTP",
    )
    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Type Captcha",
                "class": "form-captcha",
            }
        )
    )

class PartnerApplicationForm(forms.ModelForm):
    # captcha = CaptchaField(
    #     widget=CaptchaTextInput(
    #         attrs={
    #             "placeholder": "Type Captcha",
    #             "class": "form-captcha",
    #         }
    #     )
    # )
    otp = forms.CharField(max_length=6, required=False)  # Add OTP field
    class Meta:
        model = PartnerApplication
        fields = ['name', 'email', 'phone', 'company_name', 'interest_reason','agree_terms']

        # Adding custom widgets with classes and placeholders
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name'
            }),
            'interest_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What makes our partnership compelling for you?',
                'rows': 4
            }),
            'agree_terms': forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'required': 'required'
        })
        }


class FeedBackForm(ModelForm):
    """Feedback form"""

    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Type Captcha",
                "class": "form-captcha",
            }
        )
    )

    class Meta:
        model = FeedBack
        fields = ["email", "rating"]
        widgets = {
            "email": TextInput(
                attrs={
                    "class": "form-control ",
                    "style": "",
                    "placeholder": "Email",
                    "id": "floatingInput",
                }
            ),
            "rating": TextInput(
                attrs={
                    "class": "rate",
                    "style": "",
                    "placeholder": "rating",
                    "id": "floatingInput",
                    "type": "radio",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(REGEX, email):
            raise forms.ValidationError("Invalid email format")
        return email


class ContactForm(ModelForm):
    """contact form"""

    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Type Captcha",
                "class": "form-captcha",
            }
        )
    )

    class Meta:
        model = ContactUs
        fields = ["name", "email", "message"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    # "style": "padding-left:50px; color:blue; font-weight:500; ",
                    "placeholder": "Name",
                    # "id": "floatingInput",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    # "style": "padding-left:50px; color:blue; font-weight:500; ",
                    "placeholder": "Email",
                    # "id": "floatingInput",
                    "type": "email",
                }
            ),
            "message": Textarea(
                attrs={
                    "class": "form-control ",
                    "style": " height:120px;",
                    "placeholder": "message",
                    # "id": "floatingInput",
                }
            ),
        }
        # this function will be used for the validation

    def clean(self):
        # data from the form is fetched using super function
        super(ContactForm, self).clean()
        # extract the username and text field from the data
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        message = self.cleaned_data.get("message")

        # conditions to be met for the name length
        if len(name) < 5:
            self._errors["name"] = self.error_class(["Minimum 5 characters required"])
        if len(message) < 10:
            self._errors["message"] = self.error_class(
                ["Message Should Contain a minimum of 10 characters"]
            )
            # return any errors if found
        return self.cleaned_data


class OtpVerifyForm(forms.Form):
    """otp submit form"""

    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Type Captcha",
                "class": "form-captcha",
            }
        )
    )
    otp1 = forms.CharField(
        max_length=1,
        required=True,
        widget=NumberInput(
            attrs={
                "type": "",
                "class": "form-control",
                "placeholder": "*",
                "style": "padding-left:20px;",
            }
        ),
    )
    otp2 = forms.CharField(
        max_length=1,
        required=True,
        widget=NumberInput(
            attrs={
                "type": "",
                "class": "form-control",
                "placeholder": "*",
                "style": "padding-left:20px;",
            }
        ),
    )
    otp3 = forms.CharField(
        max_length=1,
        required=True,
        widget=NumberInput(
            attrs={
                "type": "",
                "class": "form-control",
                "placeholder": "*",
                "style": "padding-left:20px;",
            }
        ),
    )
    otp4 = forms.CharField(
        max_length=1,
        required=True,
        widget=NumberInput(
            attrs={
                "type": "",
                "class": "form-control",
                "placeholder": "*",
                "style": "padding-left:20px;",
            }
        ),
    )

    def clean(self):
        # data from the form is fetched using super function
        super(OtpVerifyForm, self).clean()
        otp1 = self.cleaned_data.get("otp1")
        otp2 = self.cleaned_data.get("otp2")
        otp3 = self.cleaned_data.get("otp3")
        otp4 = self.cleaned_data.get("otp4")

        # conditions to be met for the length
        if len(otp1) > 1:
            self._errors["otp1"] = self.error_class(["Only Single Digit"])
        if len(otp2) > 1:
            self._errors["otp2"] = self.error_class(["Only Single Digit"])
        if len(otp3) > 1:
            self._errors["otp3"] = self.error_class(["Only Single Digit"])
        if len(otp4) > 1:
            self._errors["otp4"] = self.error_class(["Only Single Digit"])


class EstimateRequestForm(ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = EstimateRequests
        fields = ["name", "email", "mobile", "device_name", "device_problem"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control shadow",
                    "style": "padding-left:40px; color:blue; font-weight:500; ",
                    "placeholder": "Name",
                    "id": "floatingInput",
                }
            ),
            "mobile": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:40px; color:blue; font-weight:500; ",
                    "placeholder": "Mobile No",
                    "type": "number",
                    "id": "floatingInput",
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:40px; color:blue; font-weight:500; ",
                    "placeholder": "Email",
                    "id": "floatingInput",
                }
            ),
            "device_name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:40px; color:blue; font-weight:500; ",
                    "placeholder": "Device Name & Model ",
                    "id": "floatingInput",
                }
            ),
            "device_problem": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:40px; color:blue; font-weight:500; ",
                    "placeholder": "Discribe Your Device Problem .....  ",
                    "id": "floatingInput",
                }
            ),
        }

    def clean(self):
        # data from the form is fetched using super function
        super(EstimateRequestForm, self).clean()
        # extract the username and text field from the data
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        mobile = self.cleaned_data.get("mobile")
        device_name = self.cleaned_data.get("device_name")
        device_problem = self.cleaned_data.get("device_problem")

        # conditions to be met for the name length
        if len(name) < 5:
            self._errors["name"] = self.error_class(["Minimum 5 characters required"])
        if len(mobile) > 10:
            self._errors["mobile"] = self.error_class(["Only 10 Digit required"])
        # if not len(mobile) < 10 :
        #     self._errors['mobile'] = self.error_class(['Only 10 Digit required'])
        if len(device_problem) < 15:
            self._errors["device_problem"] = self.error_class(
                ["Please Discribe Your Problem in more than 15 words"]
            )
