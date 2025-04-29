from django import forms

class DeliveryLocationForm(forms.Form):
    current_location_lat = forms.FloatField(label="Current Latitude", required=True)
    current_location_lon = forms.FloatField(label="Current Longitude", required=True)