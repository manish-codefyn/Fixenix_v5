from django.forms import ModelForm
from  django import forms
from sitesetting.models import (Sites,AboutCompany,Faq,Brands)
from django.forms import TextInput,FileInput, EmailInput



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
    

    


