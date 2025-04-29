from django import forms
from .models import Employee

from sitesetting.models import (Sites,AboutCompany,Faq,Brands)
from django.forms import TextInput,FileInput, EmailInput

class EmployeeForm(forms.ModelForm):
    """Form for creating and updating Employee records with widgets and placeholders."""

    class Meta:
        model = Employee
        fields = [
            'name', 'email', 'phone', 'address', 
            'id_proof', 'photo', 'current_location_lat', 
            'current_location_lon',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter address',
                'rows': 3
            }),
            'id_proof': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'current_location_lat': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter latitude (e.g., 12.345678)'
            }),
            'current_location_lon': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter longitude (e.g., 98.765432)'
            }),
    
        }


class DateForm(forms.Form):
    """date filter"""

    startdate = forms.DateField( widget=forms.TextInput(attrs={
    'label':'From',
    'class':'form-control',
    'type':'date',
    'style': 'width: 200px;'
    
    }))
    enddate = forms.DateField( widget=forms.TextInput(attrs={
    'label':'From',
    'class':'form-control',
    'type':'date',
    'style': 'width: 200px;'
    
    }))
    
