from django.forms import ModelForm
from .models import Vehicle

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['year', 'type', 'price','engine', 'transmission', 'color', 'seats', 'doors', 'mileage', 'description'] 
