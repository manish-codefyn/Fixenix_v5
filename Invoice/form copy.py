from django.forms import ModelForm
from django import forms
from .models import Invoice
from django.forms import TextInput, FileInput, EmailInput, Select, Textarea


class InvoiceCreateForm(ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "name",
            "email",
            "mobile",
            "product_detail",
            "amount",
            "payment_status",
        ]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "placeholder": "Name",
                    "id": "floatingInput",
                }
            ),
            "mobile": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "placeholder": "Mobile No",
                    "type": "number",
                    "id": "floatingInput",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "placeholder": "Email",
                    "id": "floatingInput",
                }
            ),
            "product_detail": Textarea(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "placeholder": "Detail of Product or Repairing ",
                    "id": "floatingInput",
                }
            ),
            "amount": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "placeholder": "Price",
                    "id": "floatingInput",
                }
            ),
            "payment_status": Select(
                attrs={
                    "class": "form-control",
                    "type": "select",
                    "style": "padding-left:10px; color:blue; font-weight:500; ",
                    "id": "floatingInput",
                }
            ),
        }
