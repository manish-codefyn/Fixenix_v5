from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from .models import DoorstepService

class DoorstepServiceForm(forms.ModelForm):
    class Meta:
        model = DoorstepService
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'

        # Add a layout if desired
        self.helper.layout = Layout(
            Row(
                Column('service_name', css_class='form-group col-md-6'),
                Column('image', css_class='form-group col-md-6'),
            ),
            Row(
                Column('price', css_class='form-group col-md-6'),
                Column('offer_price', css_class='form-group col-md-6'),
            ),
        )

        # Add submit button
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-success'))
