# forms.py
from django import forms
from .models import Invoice
from django.core.validators import MinValueValidator
import json

class InvoiceUpdateForm(forms.ModelForm):
    product_details = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
        help_text="Enter product details as JSON"
    )

    class Meta:
        model = Invoice
        fields = [
            'customer_name',
            'mobile',
            'email',
            'address',
            'due_date',
            'product_details',
            'subtotal',
            'tax_amount',
            'discount_amount',
            'total_amount',
            'notes',
            'terms',
            'payment_status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert JSON to string for editing
        if self.instance and self.instance.product_details:
            self.fields['product_details'].initial = json.dumps(self.instance.product_details, indent=2)

    def clean_product_details(self):
        data = self.cleaned_data.get('product_details')
        try:
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format in product details.")


class InvoiceForm(forms.ModelForm):
    invoice_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Invoice
        # exclude = ['subtotal', 'tax_amount', 'discount_amount', 'total_amount']
        fields = [
            'customer_name',
            'mobile',
            'email',
            'address',
            'invoice_date',
            'due_date',
            'product_details',
            'subtotal',
            'tax_amount',
            'discount_amount',
            'total_amount',
            'notes',
            'terms',
            'payment_status',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'product_details': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'terms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values (shown on form load)
        self.fields['notes'].initial = "We appreciate your prompt payment. If you have any questions, feel free to contact us."
        self.fields['terms'].initial = "Payment is due within 7 days. A late fee may apply to overdue balances."
