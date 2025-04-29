from django import forms
from .models import WorkSheet, DeviceChecklist
from django.utils import timezone

class WorkSheetFilterForm(forms.Form):
    startdate = forms.DateField(
        label="From",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'max': timezone.now().date()
        }),
        required=False
    )
    enddate = forms.DateField(
        label="To",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'max': timezone.now().date()
        }),
        required=False,
        initial=timezone.now().date()
    )

    
class WorkSheetForm(forms.ModelForm):
    class Meta:
        model = WorkSheet
        fields = [
            'name', 'mobile', 'email',
            'device_name', 'device_problem', 'problem_details',
            'estimated_cost', 'status'
        ]

class DeviceChecklistForm(forms.ModelForm):
    class Meta:
        model = DeviceChecklist
        fields = ['component_name', 'is_working']
        widgets = {
            'component_name': forms.Select(attrs={'class': 'form-select'}),
            'is_working': forms.Select(choices=DeviceChecklist.WORKING_CHOICES, attrs={'class': 'form-select'}),
        }

DeviceChecklistFormSet = forms.inlineformset_factory(
    WorkSheet,
    DeviceChecklist,
    form=DeviceChecklistForm,
    extra=5,  # You can increase/decrease how many components you want to show
    can_delete=False
)

# class WorkSheetForm(forms.ModelForm):
#     class Meta:
#         model = WorkSheet
#         fields = [
#             'name', 'mobile', 'email', 
#             'device_name', 'device_problem', 'problem_details',
#             'estimated_cost', 'actual_cost', 'status'
#         ]
#         widgets = {
#             'device_problem': forms.Textarea(attrs={'rows': 3}),
#             'problem_details': forms.Textarea(attrs={'rows': 5}),
#             'status': forms.Select(attrs={'class': 'form-select'}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})