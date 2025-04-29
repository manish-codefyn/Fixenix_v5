from django.forms import ModelForm
from  django import forms
from .models import WorkSheet
from django.forms import TextInput,FileInput,EmailInput,Select
# random number
import random

STATUS_CHOICES = (
    ('0', 'Pending'),
    ('1', 'Done'),
    ('2', 'Delivered'),
    ('3', 'Returned'),
)
def randomDigits(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    at = random.randint(lower, upper)
    return at
    
class StatusUpdateForm(forms.Form):
    status =  forms.MultipleChoiceField(choices = STATUS_CHOICES)


class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    attach = forms.FileField(widget=forms.ClearableFileInput())
    message = forms.CharField(widget = forms.Textarea)

class WorkSheetForm(ModelForm):
    
    class Meta:
        model = WorkSheet
        fields = [ 'name','email','mobile','device_name','device_problem','status']
        widgets = {

                'name': TextInput(attrs={
                'class': "form-control",
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'placeholder': 'Name',
                'id':'floatingInput',
                }),

                'mobile': TextInput(attrs={
                'class': "form-control",
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'placeholder': 'Mobile No',
                'type':'number',
                 'id':'floatingInput',
                }),

                'email': EmailInput(attrs={
                'class': "form-control",
                'type':  'email',
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'placeholder': 'Email',
                'id':'floatingInput',
                }),

                'device_name': TextInput(attrs={
                'class': "form-control",
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'placeholder': 'Device Name & Model ',
                'id':'floatingInput',
                }),

                'device_problem': TextInput(attrs={
                'class': "form-control",
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'placeholder': 'Discribe Your Device Problem .....  ',
                'id':'floatingInput',
                }), 
                'status': Select(attrs={
                'class': "form-control",
                'type': "select",
                'style': 'padding-left:10px; color:blue; font-weight:500; ',
                'id':'floatingInput',
                }),

        }
    
    # def clean(self):
    #     # data from the form is fetched using super function
    #     super(OnlineRequestForm, self).clean()
    #     # extract the username and text field from the data
    #     name = self.cleaned_data.get('name')
    #     email = self.cleaned_data.get('email')
    #     mobile = self.cleaned_data.get('mobile')
    #     device_name = self.cleaned_data.get('device_name')
    #     device_problem = self.cleaned_data.get('device_problem')
       
    #     # conditions to be met for the name length
    #     if len(name) < 5:
    #         self._errors['name'] = self.error_class(['Minimum 5 characters required'])
    #     if not len(mobile) > 10 :
    #         self._errors['mobile'] = self.error_class(['Only 10 Digit required'])
    #     # if not len(mobile) < 10 :
    #     #     self._errors['mobile'] = self.error_class(['Only 10 Digit required'])
    #     if len(device_problem) < 15:
    #         self._errors['device_problem'] = self.error_class(['Please Discribe Your Problem in more than 15 words'])
